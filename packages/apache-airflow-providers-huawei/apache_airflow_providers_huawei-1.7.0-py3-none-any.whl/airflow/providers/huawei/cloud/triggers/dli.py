#
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
"""This module contains Huawei Cloud DLI triggers."""
from __future__ import annotations

import asyncio

from typing import Any, AsyncIterator
from airflow.providers.huawei.cloud.hooks.dli import DLIAsyncHook
from airflow.triggers.base import BaseTrigger, TriggerEvent


class DLIRunSqlJobTrigger(BaseTrigger):
    """Huawei Cloud DLI trigger to check if SQL job has been finished.

    :param job_id: The SQL job id.
    :param project_id: Specifies the project ID.
    :param poll_interval: The time interval in seconds to check the state. Default: 10
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for SMN credentials.
    """

    def __init__(
        self,
        job_id: str,
        poll_interval: int | None = 10,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
    ):
        super().__init__()

        self.job_id = job_id
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.region = region
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow.providers.huawei.cloud.triggers.dli.DLIRunSqlJobTrigger",
            {
                "job_id": self.job_id,
                "poll_interval": self.poll_interval,
                "project_id": self.project_id,
                "region": self.region,
                "huaweicloud_conn_id": self.huaweicloud_conn_id,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        hook = DLIAsyncHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            project_id=self.project_id,
            region=self.region,
        )
        while True:
            try:
                status = await hook.show_sql_job_status(self.job_id)
                self.log.info(f"The current job status is {status}")

                if status == "FINISHED":
                    yield TriggerEvent(
                        {
                            "job_id": self.job_id,
                            "status": "success",
                            "message": "Job finished"
                        }
                    )
                    return
                elif status == "FAILED":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"Job {self.job_id} failed"
                        }
                    )
                    return
                elif status == "CANCELLED":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"Job {self.job_id} cancelled"
                        }
                    )
                    return
                else:
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                yield TriggerEvent({"status": "error", "message": str(e)})
                return


class DLISparkCreateBatchJobTrigger(BaseTrigger):
    """Huawei Cloud DLI trigger to check if Spark Batch job has been finished.

    :param job_id: The SQL job id.
    :param project_id: Specifies the project ID.
    :param poll_interval: The time interval in seconds to check the state. Default: 10
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for SMN credentials.
    """

    def __init__(
        self,
        job_id: str,
        poll_interval: int | None = 10,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
    ):
        super().__init__()

        self.job_id = job_id
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.region = region
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow.providers.huawei.cloud.triggers.dli.DLISparkCreateBatchJobTrigger",
            {
                "job_id": self.job_id,
                "poll_interval": self.poll_interval,
                "project_id": self.project_id,
                "region": self.region,
                "huaweicloud_conn_id": self.huaweicloud_conn_id,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        hook = DLIAsyncHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            project_id=self.project_id,
            region=self.region,
        )
        while True:
            try:
                status = await hook.show_batch_state(self.job_id)
                self.log.info(f"The current batch processing job status is {status}")

                if status == "success":
                    yield TriggerEvent(
                        {
                            "job_id": self.job_id,
                            "status": "success",
                            "message": "The batch processing job is successfully executed."
                        }
                    )
                    return
                elif status == "dead":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"The batch processing job {self.job_id} has exited."
                        }
                    )
                    return
                else:
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                yield TriggerEvent({"status": "error", "message": str(e)})
                return


class DLICreateElasticResourcePoolTrigger(BaseTrigger):
    """Huawei Cloud DLI trigger to check if create elastic resource pool has been finished.

    :param elastic_resource_pool_name: The elastic resource pool name.
    :param project_id: Specifies the project ID.
    :param poll_interval: The time interval in seconds to check the state. Default: 10
    :param region: Regions where the API is available.
    :param huaweicloud_conn_id: The Airflow connection used for SMN credentials.
    """

    def __init__(
        self,
        elastic_resource_pool_name: str,
        poll_interval: int | None = 10,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
    ):
        super().__init__()

        self.elastic_resource_pool_name = elastic_resource_pool_name
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.region = region
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow.providers.huawei.cloud.triggers.dli.DLICreateElasticResourcePoolTrigger",
            {
                "elastic_resource_pool_name": self.elastic_resource_pool_name,
                "poll_interval": self.poll_interval,
                "project_id": self.project_id,
                "region": self.region,
                "huaweicloud_conn_id": self.huaweicloud_conn_id,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        hook = DLIAsyncHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            project_id=self.project_id,
            region=self.region,
        )
        while True:
            try:
                status = await hook.show_elastic_resource_pool_status(self.elastic_resource_pool_name)
                self.log.info(f"The current status of the elastic resource pool is {status}")

                if status == "AVAILABLE":
                    yield TriggerEvent(
                        {
                            "elastic_resource_pool_name": self.elastic_resource_pool_name,
                            "status": "success",
                            "message": "The elastic resource pool is AVAILABLE."
                        }
                    )
                    return
                elif status == "FAILED":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"Elastic resource pool {self.elastic_resource_pool_name} has FAILED."
                        }
                    )
                    return
                else:
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                yield TriggerEvent({"status": "error", "message": str(e)})
                return
