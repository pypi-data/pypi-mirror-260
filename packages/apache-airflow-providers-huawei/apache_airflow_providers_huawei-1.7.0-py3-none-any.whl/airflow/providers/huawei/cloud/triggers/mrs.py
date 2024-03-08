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
"""This module contains Huawei Cloud MRS triggers."""
from __future__ import annotations

import asyncio

from typing import Any, AsyncIterator
from airflow.providers.huawei.cloud.hooks.mrs import MRSAsyncHook
from airflow.triggers.base import BaseTrigger, TriggerEvent


class MRSCreateExecuteJobTrigger(BaseTrigger):
    """
    Huawei Cloud MRS trigger to check if job has been finished.

    :param job_id: The ID of an MRS job.
    :param cluster_id: The cluster ID.
    :param poll_interval: The time interval in seconds to check the state. Default: 10
    :param project_id: Google Cloud Project where the job is running
    :param region: The Cloud MRS region in which to handle the request.
    :param huaweicloud_conn_id: Optional, the connection ID used to connect to Google Cloud Platform.
    """

    def __init__(
        self,
        job_id: str,
        cluster_id: str,
        poll_interval: int | None = 10,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
    ):
        super().__init__()
        self.job_id = job_id
        self.cluster_id = cluster_id
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.region = region
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow.providers.huawei.cloud.triggers.mrs.MRSCreateExecuteJobTrigger",
            {
                "job_id": self.job_id,
                "cluster_id": self.cluster_id,
                "poll_interval": self.poll_interval,
                "project_id": self.project_id,
                "region": self.region,
                "huaweicloud_conn_id": self.huaweicloud_conn_id,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        hook = MRSAsyncHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            project_id=self.project_id,
            region=self.region,
        )
        while True:
            try:
                response = await hook.show_single_job_exe(self.job_id, self.cluster_id)
                job_result = response.job_detail.job_result
                job_state = response.job_detail.job_state
                job_progress = response.job_detail.job_progress
                self.log.info(f"The current job status is {job_state}.\t"
                              f"Job result: {job_result}.\t"
                              f"The progress of job execution: {job_progress}.")

                if job_state == "FINISHED":
                    yield TriggerEvent(
                        {
                            "job_id": self.job_id,
                            "status": "success",
                            "message": "Job finished"
                        }
                    )
                    return
                elif job_state == "FAILED":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"Job {self.job_id} failed"
                        }
                    )
                    return
                elif job_state == "KILLED":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"Job {self.job_id} killed"
                        }
                    )
                    return
                else:
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                yield TriggerEvent({"status": "error", "message": str(e)})
                return


class MRSCreateClusterTrigger(BaseTrigger):
    """
    Huawei Cloud MRS trigger to check if cluster has been running.

    :param cluster_id: The cluster ID.
    :param poll_interval: The time interval in seconds to check the state. Default: 10
    :param project_id: Google Cloud Project where the job is running
    :param region: The Cloud MRS region in which to handle the request.
    :param huaweicloud_conn_id: Optional, the connection ID used to connect to Google Cloud Platform.
    """

    def __init__(
        self,
        cluster_id: str,
        poll_interval: int | None = 10,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
    ):
        super().__init__()
        self.cluster_id = cluster_id
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.region = region
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow.providers.huawei.cloud.triggers.mrs.MRSCreateClusterTrigger",
            {
                "cluster_id": self.cluster_id,
                "poll_interval": self.poll_interval,
                "project_id": self.project_id,
                "region": self.region,
                "huaweicloud_conn_id": self.huaweicloud_conn_id,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        hook = MRSAsyncHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            project_id=self.project_id,
            region=self.region,
        )
        while True:
            try:
                response = await hook.show_cluster_details(self.cluster_id)
                cluster_state = response.cluster.cluster_state
                stage_desc = response.cluster.stage_desc
                self.log.info(f"The current cluster status is {cluster_state}.\t"
                              f"The progress of create cluster: {stage_desc}.")

                if cluster_state == "running":
                    yield TriggerEvent(
                        {
                            "cluster_id": self.cluster_id,
                            "status": "success",
                            "message": "The cluster is running"
                        }
                    )
                    return
                elif cluster_state == "failed":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"The cluster {self.cluster_id} is failed"
                        }
                    )
                    return
                elif cluster_state == "abnormal":
                    yield TriggerEvent(
                        {
                            "status": "error",
                            "message": f"The cluster {self.cluster_id} is abnormal"
                        }
                    )
                    return
                else:
                    await asyncio.sleep(self.poll_interval)
            except Exception as e:
                yield TriggerEvent({"status": "error", "message": str(e)})
                return
