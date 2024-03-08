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
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from airflow.utils.context import Context

from airflow.compat.functools import cached_property
from airflow.exceptions import AirflowException
from airflow.providers.huawei.cloud.hooks.dli import DLIHook
from airflow.sensors.base import BaseSensorOperator


class DLISparkShowBatchStateSensor(BaseSensorOperator):
    """Sensor for checking the state of a DLI Spark job."""

    FAILURE_STATES = ("dead", )
    template_fields: Sequence[str] = ("job_id", "target_status",)
    template_ext: Sequence[str] = ()
    ui_color = "#66c3ff"

    def __init__(
        self,
        *,
        job_id: str,
        target_status: str = "success",
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.job_id = job_id
        self.target_status = target_status
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:
        state = self.get_hook.show_batch_state(job_id=self.job_id)
        self.log.info("Poking for status : %s for job %s.\t"
                      "Now job status: %s.\t",
                      self.target_status, self.job_id, state)

        if state == self.target_status:
            return True

        if state in self.FAILURE_STATES:
            raise AirflowException("DLI batch job sensor failed")
        return False

    @cached_property
    def get_hook(self) -> DLIHook:
        """Create and return a DLIHook"""
        return DLIHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class DLISqlShowJobStatusSensor(BaseSensorOperator):
    """Sensor for checking the state of a DLI SQL job."""

    FAILURE_STATES = ("FAILED", "CANCELLED")
    template_fields: Sequence[str] = ("job_id",)
    template_ext: Sequence[str] = ()
    ui_color = "#66c3ff"

    def __init__(
        self,
        *,
        job_id: str,
        target_status: str = "FINISHED",
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.job_id = job_id
        self.target_status = target_status
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:
        state = self.get_hook.show_sql_job_status(job_id=self.job_id)
        self.log.info("Poking for status : %s for job %s.\t"
                      "Now job status: %s.\t",
                      self.target_status, self.job_id, state)

        if state == self.target_status:
            return True

        if state in self.FAILURE_STATES:
            raise AirflowException("DLI sql job sensor failed")
        return False

    @cached_property
    def get_hook(self) -> DLIHook:
        """Create and return a DLIHook"""
        return DLIHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class DLIShowElasticResourcePoolStatusSensor(BaseSensorOperator):
    """Sensor for checking the state of a DLI elastic resource pool."""

    FAILURE_STATES = ("FAILED",)
    template_fields: Sequence[str] = ("elastic_resource_pool_name", "target_status",)
    template_ext: Sequence[str] = ()
    ui_color = "#66c3ff"

    def __init__(
        self,
        *,
        elastic_resource_pool_name: str,
        target_status: str = "AVAILABLE",
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.elastic_resource_pool_name = elastic_resource_pool_name
        self.target_status = target_status
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:
        response = self.get_hook.list_elastic_resource_pools(name=self.elastic_resource_pool_name)
        pools = response.elastic_resource_pools
        state = None
        for pool in pools:
            if pool.elastic_resource_pool_name == self.elastic_resource_pool_name:
                state = pool.status
        if not state:
            raise Exception(f"There is no elastic resource pool with name {self.elastic_resource_pool_name}")

        self.log.info("Poking for status : %s for elastic resource pool %s.\t"
                      "Now elastic resource pool status: %s.\t",
                      self.target_status, self.elastic_resource_pool_name, state)
        if state == self.target_status:
            return True

        if state in self.FAILURE_STATES:
            raise AirflowException("DLI elastic resource pool status sensor failed")
        return False

    @cached_property
    def get_hook(self) -> DLIHook:
        """Create and return a DLIHook"""
        return DLIHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )


class DLIShowEnhancedConnectionSensor(BaseSensorOperator):
    """Sensor for checking the state of a DLI enhanced connection."""

    FAILURE_STATES = ("FAILED",)
    template_fields: Sequence[str] = ("connection_id", "target_status",)
    template_ext: Sequence[str] = ()
    ui_color = "#66c3ff"

    def __init__(
        self,
        *,
        connection_id: str,
        target_status: str = "ACTIVE",
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.connection_id = connection_id
        self.target_status = target_status
        self.project_id = project_id
        self.region = region

    def poke(self, context: Context) -> bool:
        state = self.get_hook.show_enhanced_connection(connection_id=self.connection_id).status
        if not state:
            raise Exception(f"There is no enhanced connection with the id {self.connection_id}")

        self.log.info("Poking for status : %s for enhanced connection %s.\t"
                      "Now enhanced connection status: %s.\t",
                      self.target_status, self.connection_id, state)
        if state == self.target_status:
            return True

        if state in self.FAILURE_STATES:
            raise AirflowException("DLI enhanced connection status sensor failed")
        return False

    @cached_property
    def get_hook(self) -> DLIHook:
        """Create and return a DLIHook"""
        return DLIHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, project_id=self.project_id, region=self.region
        )
