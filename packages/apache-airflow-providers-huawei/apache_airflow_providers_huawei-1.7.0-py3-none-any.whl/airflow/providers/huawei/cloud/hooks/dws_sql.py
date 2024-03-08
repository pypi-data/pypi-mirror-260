# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor, RealDictCursor
from typing import Type

from airflow.compat.functools import cached_property
from airflow.providers.common.sql.hooks.sql import DbApiHook


class DWSSqlHook(DbApiHook):
    """
    Execute statements against Huawei Cloud DWS, using dws_connector

    This hook requires the dws_conn_id connection.

    :param dws_conn_id: reference to
        :ref:`Huawei Cloud DWS connection id<howto/connection:dws>`.
    :param options: The command-line options passed in the connection request.
    """

    conn_name_attr = "dws_conn_id"
    default_conn_name = "dws_default"
    conn_type = "dws"
    hook_name = "Huawei Cloud DWS"
    supports_autocommit = True

    def __init__(self, *args, options: str | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.connection = kwargs.pop("connection", None)
        self.options = options

    @staticmethod
    def valid_cursor(raw_cursor: str) -> Type[DictCursor | RealDictCursor | NamedTupleCursor]:
        lower_cursor = raw_cursor.lower()

        if lower_cursor == "dictcursor":
            return psycopg2.extras.DictCursor
        elif lower_cursor == "realdictcursor":
            return psycopg2.extras.RealDictCursor
        elif lower_cursor == "namedtuplecursor":
            return psycopg2.extras.NamedTupleCursor
        else:
            raise ValueError(
                f"Invalid cursor passed {lower_cursor}, "
                f"choose from (dictcursor, realdictcursor, namedtuplecursor)"
            )

    @cached_property
    def conn(self):
        return self.connection or self.get_connection(getattr(self, self.conn_name_attr))

    def get_conn(self) -> psycopg2.connection:
        """Returns a GussDB(DWS) database connection."""

        conn_args = dict(
            host=self.conn.host,
            user=self.conn.login,
            password=self.conn.password,
            dbname=self.conn.schema,
            port=self.conn.port,
        )

        raw_cursor = self.conn.extra_dejson.get("cursor")
        if raw_cursor:
            conn_args["cursor_factory"] = self.valid_cursor(raw_cursor)

        client_encoding = self.conn.extra_dejson.get("client_encoding", "utf-8")
        if client_encoding:
            conn_args["client_encoding"] = client_encoding

        if self.options:
            conn_args["options"] = self.options

        return psycopg2.connect(**conn_args)

    @staticmethod
    def get_ui_field_behaviour() -> dict:
        """Returns custom UI field behaviour for Huawei Cloud DWS Connection."""
        return {
            "hidden_fields": [],
            "relabeling": {"login": "User", "schema": "Database"},
        }
