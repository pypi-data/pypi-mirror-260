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

import os.path
import huaweicloudsdkdli.v1 as DliSdk

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkdli.v1.region.dli_region import DliRegion

from airflow.exceptions import AirflowException
from airflow.providers.huawei.cloud.hooks.base_huawei_cloud import HuaweiBaseHook


class DLIHook(HuaweiBaseHook):
    """Interact with Huawei Cloud DLI, using the huaweicloudsdkdli library."""

    def create_queue(
        self,
        queue_name,
        platform,
        enterprise_project_id,
        elastic_resource_pool_name,
        feature,
        resource_mode,
        charging_mode,
        description,
        queue_type,
        list_tags_body,
        list_labels_body,
        cu_count,
    ) -> DliSdk.CreateQueueResponse:
        """
        Create a queue in DLI

        :param queue_name: The name of the queue.
        :param platform: The platform of the queue.
        :param enterprise_project_id: The enterprise project ID of the queue.
        :param elastic_resource_pool_name: The elastic resource pool name of the queue.
        :param feature: The feature of the queue.
        :param resource_mode: The resource mode of the queue.
        :param charging_mode: The charging mode of the queue.
        :param description: The description of the queue.
        :param queue_type: The type of the queue.
        :param list_tags_body: The tags of the queue.
        :param list_labels_body: The labels of the queue.
        :param cu_count: The CU count of the queue.
        :return: The response of the queue creation.
        :rtype: DliSdk.CreateQueueResponse
        """
        if list_tags_body is not None and len(list_tags_body) > 10:
            raise AirflowException("You can add up to 10 tags.")
        try:
            return self.get_dli_client().create_queue(
                self.create_queue_request(
                    elastic_resource_pool_name=elastic_resource_pool_name,
                    list_tags_body=list_tags_body,
                    feature=feature,
                    list_labels_body=list_labels_body,
                    resource_mode=resource_mode,
                    platform=platform,
                    enterprise_project_id=enterprise_project_id
                    if enterprise_project_id is not None
                    else self.get_enterprise_project_id_from_extra_data(),
                    charging_mode=charging_mode,
                    cu_count=cu_count,
                    description=description,
                    queue_type=queue_type,
                    queue_name=queue_name,
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when creating: {e}")

    def update_queue_cidr(self, queue_name, cidr_in_vpc) -> DliSdk.UpdateQueueCidrResponse:
        """
        Update the CIDR of a queue in DLI

        :param queue_name: The name of the queue.
        :param cidr_in_vpc: The CIDR of the queue.
        :return: The response of the queue update.
        :rtype: DliSdk.UpdateQueueCidrResponse
        """
        try:
            return self.get_dli_client().update_queue_cidr(
                self.update_queue_cidr_request(queue_name=queue_name, cidr_in_vpc=cidr_in_vpc)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when updating: {e}")

    def delete_queue(self, queue_name) -> DliSdk.DeleteQueueResponse:
        """
        Delete a queue in DLI

        :param queue_name: The name of the queue.
        :return: The response of the queue deletion.
        :rtype: DliSdk.DeleteQueueResponse
        """
        try:
            return self.get_dli_client().delete_queue(self.delete_queue_request(queue_name))
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when deleting: {e}")

    def list_queues(
        self, queue_type, tags, return_billing_info, return_permission_info
    ) -> DliSdk.ListQueuesResponse:
        """
        List queues in DLI

        :param queue_type: The type of the queue.
        :param tags: The tags of the queue.
        :param return_billing_info: Whether to return billing information.
        :param return_permission_info: Whether to return permission information.
        :return: The response of the queue listing.
        :rtype: DliSdk.ListQueuesResponse
        """
        try:
            return self.get_dli_client().list_queues(
                self.list_queues_request(
                    queue_type=queue_type,
                    tags=tags,
                    return_billing_info=return_billing_info,
                    return_permission_info=return_permission_info,
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when listing: {e}")

    def create_batch_job(
        self,
        queue_name,
        file,
        class_name,
        obs_bucket,
        catalog_name,
        image,
        max_retry_times,
        auto_recovery,
        spark_version,
        feature,
        num_executors,
        executor_cores,
        executor_memory,
        driver_cores,
        driver_memory,
        name,
        list_conf_body,
        list_groups_body,
        list_resources_body,
        list_modules_body,
        list_files_body,
        list_python_files_body,
        list_jars_body,
        sc_type,
        list_args_body,
        cluster_name,
    ) -> DliSdk.CreateBatchJobResponse:
        """
        Create a batch job in DLI

        :param queue_name: The name of the queue.
        :param file: OBS path of the batch job file.
        :param class_name: The class name of the batch job.
        :param obs_bucket: The OBS bucket of the batch job.
        :param catalog_name: The catalog name of the batch job.
        :param image: The image of the batch job.
        :param max_retry_times: The maximum retry times of the batch job.
        :param auto_recovery: Whether to enable auto recovery.
        :param spark_version: The Spark version of the batch job.
        :param feature: The feature of the batch job.
        :param num_executors: The number of executors of the batch job.
        :param executor_cores: The number of cores of the executor.
        :param executor_memory: The memory of the executor.
        :param driver_cores: The number of cores of the driver.
        :param driver_memory: The memory of the driver.
        :param name: The name of the batch job.
        :param list_conf_body: The configuration of the batch job.
        :param list_groups_body: The groups of the batch job.
        :param list_resources_body: The resources of the batch job.
        :param list_modules_body: The modules of the batch job.
        :param list_files_body: The files of the batch job.
        :param list_python_files_body: The Python files of the batch job.
        :param list_jars_body: The JAR files of the batch job.
        :param sc_type: The type of the Spark context.
        :param list_args_body: The arguments of the batch job.
        :param cluster_name: The name of the cluster.
        :return: The response of the batch job creation.
        :rtype: DliSdk.CreateBatchJobResponse
        """
        try:
            return self.get_dli_client().create_batch_job(
                self.create_batch_job_request(
                    queue_name=queue_name,
                    file=file,
                    class_name=class_name,
                    obs_bucket=obs_bucket,
                    catalog_name=catalog_name,
                    image=image,
                    max_retry_times=max_retry_times,
                    auto_recovery=auto_recovery,
                    spark_version=spark_version,
                    feature=feature,
                    num_executors=num_executors,
                    executor_cores=executor_cores,
                    executor_memory=executor_memory,
                    driver_cores=driver_cores,
                    driver_memory=driver_memory,
                    name=name,
                    list_conf_body=list_conf_body,
                    list_groups_body=list_groups_body,
                    list_resources_body=list_resources_body,
                    list_modules_body=list_modules_body,
                    list_files_body=list_files_body,
                    list_python_files_body=list_python_files_body,
                    list_jars_body=list_jars_body,
                    sc_type=sc_type,
                    list_args_body=list_args_body,
                    cluster_name=cluster_name,
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when crating batch job: {e}")

    def upload_files(self, paths, group) -> DliSdk.UploadFilesResponse:
        """
        Upload files to DLI

        :param paths: The paths of the files to be uploaded.
        :param group: The group of the files to be uploaded.
        :return: The response of the file upload.
        :rtype: DliSdk.UploadFilesResponse
        """
        try:
            return self.get_dli_client().upload_files(self.upload_files_request(paths=paths, group=group))
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when uploading files: {e}")

    def create_sql_job(
        self, sql_query, database_name, queue_name, list_conf_body, list_tags_body
    ) -> DliSdk.CreateSqlJobResponse:
        """
        Submit SQL job in DLI

        :param sql_query: The SQL query of the job.
        :param database_name: The database name of the job.
        :param queue_name: The queue name of the job.
        :param list_conf_body: The configuration of the job.
        :param list_tags_body: The tags of the job.
        :return: The response of the job run.
        :rtype: DliSdk.RunJobResponse
        """
        try:
            if os.path.isfile(sql_query):
                sql_file = open(sql_query)
                sql_query = sql_file.read()
                sql_file.close()

            return self.get_dli_client().create_sql_job(
                self.create_sql_job_request(
                    sql_query=sql_query,
                    database_name=database_name,
                    list_conf_body=list_conf_body,
                    list_tags_body=list_tags_body,
                    queue_name=queue_name,
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when running: {e}")

    def get_job_result(self, job_id, queue_name) -> DliSdk.PreviewJobResultResponse:
        """
        View the job execution result after a job is executed using SQL query statements.

        :param job_id: Job ID
        :param queue_name: Name of the queue to which a job to be submitted belongs.
        :return: The response of the job result.
        :rtype: DliSdk.PreviewJobResultResponse
        """
        try:
            return self.get_dli_client().preview_job_result(
                self.get_job_result_request(job_id, queue_name))
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when get job result: {e}")

    def show_batch_state(self, job_id) -> str:
        """
        Get the state of a batch job

        :param job_id: The ID of the batch job.
        :return: The state of the batch job.
        :rtype: str
        """
        try:
            return self.get_dli_client().show_batch_state(self.show_batch_state_request(job_id)).state
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when get batch state: {e}")

    def show_sql_job_status(self, job_id) -> str:
        """
        Get the status of a job

        :param job_id: The ID of the job.
        :return: The status of the job.
        :rtype: str
        """
        try:
            return self.get_dli_client().show_sql_job_status(self.show_sql_job_status_request(job_id)).status
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when get job status: {e}")

    def cancel_sql_job(self, job_id) -> DliSdk.CancelSqlJobResponse:
        """
        Cancel sql job

        :param job_id: The ID of the job.
        :return: The status of the job.
        :rtype: str
        """
        try:
            return self.get_dli_client().cancel_sql_job(self.cancel_sql_job_request(job_id))
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when cancel sql job result: {e}")

    def cancel_batch_job(self, job_id) -> DliSdk.CancelBatchJobResponse:
        """
        Cancel batch job

        :param job_id: The ID of the job.
        :return: The status of the job.
        :rtype: str
        """
        try:
            return self.get_dli_client().cancel_batch_job(self.cancel_batch_job_request(job_id))
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when cancel sql job result: {e}")

    def create_elastic_resource_pool(
        self,
        max_cu: int,
        min_cu: int,
        elastic_resource_pool_name: str,
        description: str | None = None,
        cidr_in_vpc: str = "172.16.0.0/12",
        charging_mode: int = 1,
        enterprise_project_id: str | None = None,
        tags: list[dict] | None = None,
    ) -> DliSdk.CreateElasticResourcePoolResponse:
        """
        Create an elastic resource pool

        :param elastic_resource_pool_name: The name of elastic resource pool.
        :param description: Description. The value can contain a maximum of 256 characters.
        :param cidr_in_vpc: VPC CIDR associated with the virtual cluster.
            If it is not specified, the default value 172.16.0.0/12 is used.
        :param max_cu: Maximum number of CUs.
            The value of this parameter must be greater than or equal to the sum of maximum CUs allowed
            for any queue in the resource pool, and greater than min_cu. The minimum value is 64.
        :param min_cu: Minimum number of CUs.
            The value of this parameter must be greater than or equal to the sum of the minimum CUs allowed
            for each queue in the resource pool. The minimum value is 64.
        :param charging_mode: Billing mode. The default value is 1, which indicates the pay-per-use billing mode.
        :param enterprise_project_id: Enterprise ID. If this parameter is left blank, the default value 0 is used.
        :param tags: Queue tags for identifying cloud resources. A tag consists of a key and a value.
        :return: The response of the elastic resource pool creation.
        :rtype: DliSdk.CreateElasticResourcePoolResponse
        """
        try:
            return self.get_dli_client().create_elastic_resource_pool(
                self.create_elastic_resource_pool_request(
                    elastic_resource_pool_name=elastic_resource_pool_name,
                    description=description,
                    cidr_in_vpc=cidr_in_vpc,
                    max_cu=max_cu,
                    charging_mode=charging_mode,
                    min_cu=min_cu,
                    enterprise_project_id=enterprise_project_id,
                    tags=tags,
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when create elastic resource pool: {e}")

    def list_elastic_resource_pools(
        self, limit=None, name=None, offset=None, status=None, tags=None
    ) -> DliSdk.ListElasticResourcePoolsResponse:
        """
        List all elastic resource pools

        :param name: Fuzzy match based on the elastic resource pool name.
        :param limit: Page size. The default value is 100.
        :param offset: Offset. The default value is 0.
        :param status: Status of the elastic resource pool.
            Possible values are as follows: AVAILABLE, SCALING, CREATING, FAILED
        :param tags: Query results are filtered by tag.
        :return: The response of the elastic resource pool creation.
        :rtype: DliSdk.ListElasticResourcePoolsResponse
        """
        try:
            return self.get_dli_client().list_elastic_resource_pools(
                self.list_elastic_resource_pools_request(limit, name, offset, status, tags)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when list elastic resource pools: {e}")

    def delete_elastic_resource_pool(
        self, elastic_resource_pool_name: str
    ) -> DliSdk.DeleteElasticResourcePoolResponse:
        """
        Delete an elastic resource pool.

        :param elastic_resource_pool_name: Fuzzy match based on the elastic resource pool name.
        :return: The response for deleting an elastic resource pool.
        :rtype: DliSdk.DeleteElasticResourcePoolResponse
        """
        try:
            return self.get_dli_client().delete_elastic_resource_pool(
                self.delete_elastic_resource_pool_request(elastic_resource_pool_name)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when delete elastic resource pool: {e}")

    def associate_connection_queue(
        self,
        connection_id: str,
        elastic_resource_pools: list[str] | None = None,
    ) -> DliSdk.AssociateConnectionQueueResponse:
        """
        Bind an elastic resource pool to a created enhanced datasource connection.

        :param connection_id: Connection ID. Identifies the UUID of a datasource connection.
        :param elastic_resource_pools: Elastic resource pools you want to bind
            to the enhanced datasource connection.
        :return: The response for binding an elastic resource pool to enhanced datasource connection.
        :rtype: DliSdk.AssociateConnectionQueueResponse
        """
        try:
            return self.get_dli_client().associate_connection_queue(
                self.associate_connection_queue_request(connection_id, elastic_resource_pools)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when associate connection queue: {e}")

    def disassociate_connection_queue(
        self,
        connection_id: str,
        elastic_resource_pools: list[str] | None = None,
    ):
        """
        Unbind an elastic resource pool to a created enhanced datasource connection.

        :param connection_id: Connection ID. Identifies the UUID of a datasource connection.
        :param elastic_resource_pools: Elastic resource pools you want to bind
            to the enhanced datasource connection.
        :return: The response for unbinding an elastic resource pool to enhanced datasource connection.
        :rtype: DliSdk.AssociateConnectionQueueResponse
        """
        try:
            return self.get_dli_client().disassociate_connection_queue(
                self.disassociate_connection_queue_request(connection_id, elastic_resource_pools)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when disassociate connection queue: {e}")

    def list_elastic_resource_pool_queues(
        self,
        elastic_resource_pool_name: str,
        queue_name: str | None = None,
        limit: int | None = None,
        offset: int | None = None
    ) -> DliSdk.ListElasticResourcePoolQueuesResponse:
        """
        List all queues in an elastic resource pool.

        :param elastic_resource_pool_name: Elastic resource pool name.
        :param queue_name: You can filter data by queue name.
        :param limit: Page size. The default value is 100.
        :param offset: Offset. The default value is 0.
        :return: The response for listing queues in an elastic resource pool.
        :rtype: DliSdk.ListElasticResourcePoolQueuesResponse
        """
        try:
            return self.get_dli_client().list_elastic_resource_pool_queues(
                self.list_elastic_resource_pool_queues_request(
                    elastic_resource_pool_name, queue_name, limit, offset
                )
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when list elastic resource pool queues: {e}")

    def create_enhanced_connection(
        self,
        name: str,
        dest_vpc_id: str,
        dest_network_id: str,
        routetable_id: int | None = None,
        hosts: list | None = None,
        tags: list | None = None,
    ) -> DliSdk.CreateEnhancedConnectionResponse:
        """
        Create enhanced connection.

        :param name: Connection name.
        :param dest_vpc_id: The ID of the service VPC to be connected.
        :param dest_network_id: The subnet ID of the to-be-connected service.
        :param routetable_id: Route table associated with the subnet of the service.
        :param hosts: The user-defined host information.
        :param tags: Tags of datasource connections.
        :return: The response for creating an enhanced connection.
        :rtype: DliSdk.DeleteEnhancedConnectionResponse
        """
        try:
            request = self.create_enhanced_connection_request(
                name, dest_vpc_id, dest_network_id, routetable_id, hosts, tags
            )
            return self.get_dli_client().create_enhanced_connection(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when create enhanced connection: {e}")

    def list_enhanced_connections(
        self, limit=None, name=None, offset=None, status=None, tags=None
    ) -> DliSdk.ListEnhancedConnectionsResponse:
        """
        List all enhanced datasource connections.

        :param name: Connection name.
        :param limit: The maximum number of connections to be queried.
            The default value is 100. If limit is set to 0, all datasource connections are returned.
        :param offset: The offset of the query result. The default value is 0.
            Note that the connections are sorted by creation time.
        :param status: Connection status.
            The options are as follows: ACTIVE, DELETED
        :param tags: List of tag names. The value is k=v for a single tag.
            Multiple tags are separated by commas (,). Example: tag1=v1,tag2=v2.
        :return: The response for listing enhanced datasource connections.
        :rtype: DliSdk.ListEnhancedConnectionsResponse
        """
        try:
            return self.get_dli_client().list_enhanced_connections(
                self.list_enhanced_connections_request(limit, name, offset, status, tags)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when list enhanced connections: {e}")

    def delete_enhanced_connection(self, connection_id: str) -> DliSdk.DeleteEnhancedConnectionResponse:
        """
        Delete enhanced connection.

        :param connection_id: Enhanced connection id.
        :return: The response for deleting an enhanced connection.
        :rtype: DliSdk.DeleteEnhancedConnectionResponse
        """
        try:
            return self.get_dli_client().delete_enhanced_connection(
                self.delete_enhanced_connection_request(connection_id)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when delete enhanced connections: {e}")

    def create_route_to_enhanced_connection(
        self, connection_id: str, name: str, cidr: str
    ) -> DliSdk.CreateEnhancedConnectionRoutesResponse:
        """
        Create route to enhanced connection.

        :param connection_id: Enhanced connection id.
        :param name: Route name.
        :param cidr: Route network range.
        :return: The response for creating route to enhanced connection.
        :rtype: DliSdk.CreateEnhancedConnectionRoutesResponse
        """
        try:
            return self.get_dli_client().create_enhanced_connection_routes(
                self.create_route_to_enhanced_connection_request(connection_id, name, cidr)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when create route to enhanced connection: {e}")

    def delete_route_from_enhanced_connection(
        self, connection_id: str, name: str
    ) -> DliSdk.DeleteEnhancedConnectionRoutesResponse:
        """
        Delete route from enhanced connection.

        :param connection_id: Enhanced connection id.
        :param name: Route name.
        :return: The response for deleting route from enhanced connection.
        :rtype: DliSdk.DeleteEnhancedConnectionRoutesResponse
        """
        try:
            return self.get_dli_client().delete_enhanced_connection_routes(
                self.delete_route_from_enhanced_connection_request(connection_id, name)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when delete route from enhanced connection: {e}")

    def show_enhanced_connection(self, connection_id: str) -> DliSdk.ShowEnhancedConnectionResponse:
        """
        Query enhanced connection.

        :param connection_id: Enhanced connection id.
        :return: The response for querying enhanced connection.
        :rtype: DliSdk.ShowEnhancedConnectionResponse
        """
        try:
            return self.get_dli_client().show_enhanced_connection(
                self.show_enhanced_connection_request(connection_id)
            )
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when query enhanced connection: {e}")

    def show_connectivity_of_queue(self, queue_name: str, address: str) -> str:
        """
        Sends an address connectivity test request to the specified queue
        and displays the connectivity test result.

        :param queue_name: Queue name.
        :param address: Test address. The format is IP address or domain name:port.
        :return: Indicates the connectivity test result.
        :rtype: str
        """
        try:
            dli_client = self.get_dli_client()
            response = dli_client.check_connection(
                self.create_connection_task_request(queue_name, address)
            )
            if not response.is_success:
                raise AirflowException("Create connection task execution failure.")
            task_response = dli_client.show_node_connectivity(
                self.show_node_connectivity_request(queue_name, response.task_id)
            )
            return task_response.connectivity
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when create address connectivity test request: {e}")

    def get_dli_client(self) -> DliSdk.DliClient:
        ak = self.conn.login
        sk = self.conn.password

        credentials = BasicCredentials(ak, sk, self.get_project_id())

        return (
            DliSdk.DliClient.new_builder()
            .with_credentials(credentials)
            .with_region(DliRegion.value_of(self.get_region()))
            .build()
        )

    @staticmethod
    def cancel_sql_job_request(job_id) -> DliSdk.CancelSqlJobRequest:
        return DliSdk.CancelSqlJobRequest(job_id)

    @staticmethod
    def cancel_batch_job_request(job_id) -> DliSdk.CancelBatchJobRequest:
        return DliSdk.CancelBatchJobRequest(job_id)

    @staticmethod
    def show_sql_job_status_request(job_id):
        return DliSdk.ShowSqlJobStatusRequest(job_id)

    @staticmethod
    def show_batch_state_request(job_id):
        return DliSdk.ShowBatchStateRequest(job_id)

    @staticmethod
    def create_sql_job_request(sql_query, database_name, queue_name, list_conf_body, list_tags_body):
        request = DliSdk.CreateSqlJobRequest()
        request.body = DliSdk.CreateSqlJobRequestBody(
            queue_name=queue_name,
            currentdb=database_name,
            sql=sql_query,
            tags=list_tags_body,
            conf=list_conf_body,
        )
        return request

    @staticmethod
    def upload_files_request(paths, group):
        request = DliSdk.UploadFilesRequest()
        request.body = DliSdk.UploadGroupPackageReq(group=group, paths=paths)
        return request

    @staticmethod
    def create_batch_job_request(
        queue_name,
        file,
        class_name,
        obs_bucket,
        catalog_name,
        image,
        max_retry_times,
        auto_recovery,
        spark_version,
        feature,
        num_executors,
        executor_cores,
        executor_memory,
        driver_cores,
        driver_memory,
        name,
        list_conf_body,
        list_groups_body,
        list_resources_body,
        list_modules_body,
        list_files_body,
        list_python_files_body,
        list_jars_body,
        sc_type,
        list_args_body,
        cluster_name,
    ) -> DliSdk.CreateBatchJobRequest:
        request = DliSdk.CreateBatchJobRequest()
        request.body = DliSdk.BatchJobInfo(
            queue=queue_name,
            file=file,
            class_name=class_name,
            obs_bucket=obs_bucket,
            catalog_name=catalog_name,
            image=image,
            max_retry_times=max_retry_times,
            auto_recovery=auto_recovery,
            spark_version=spark_version,
            feature=feature,
            num_executors=num_executors,
            executor_cores=executor_cores,
            executor_memory=executor_memory,
            driver_cores=driver_cores,
            driver_memory=driver_memory,
            name=name,
            conf=list_conf_body,
            groups=list_groups_body,
            resources=list_resources_body,
            modules=list_modules_body,
            files=list_files_body,
            py_files=list_python_files_body,
            jars=list_jars_body,
            sc_type=sc_type,
            args=list_args_body,
            cluster_name=cluster_name,
        )
        return request

    @staticmethod
    def list_queues_request(queue_type, tags, return_billing_info, return_permission_info):
        return DliSdk.ListQueuesRequest(
            queue_type=queue_type,
            tags=tags,
            with_charge_info=return_billing_info,
            with_priv=return_permission_info,
        )

    @staticmethod
    def delete_queue_request(queue_name):
        return DliSdk.DeleteQueueRequest(queue_name)

    @staticmethod
    def update_queue_cidr_request(queue_name, cidr_in_vpc):
        request = DliSdk.UpdateQueueCidrRequest()
        request.queue_name = queue_name
        request.body = DliSdk.UpdateQueueCidrReq(cidr_in_vpc=cidr_in_vpc)
        return request

    @staticmethod
    def create_queue_request(
        queue_name,
        platform,
        enterprise_project_id,
        elastic_resource_pool_name,
        feature,
        resource_mode,
        charging_mode,
        description,
        queue_type,
        list_tags_body,
        list_labels_body,
        cu_count,
    ):
        request = DliSdk.CreateQueueRequest()
        request.body = DliSdk.CreateQueueReq(
            elastic_resource_pool_name=elastic_resource_pool_name,
            tags=list_tags_body,
            feature=feature,
            labels=list_labels_body,
            resource_mode=resource_mode,
            platform=platform,
            enterprise_project_id=enterprise_project_id,
            charging_mode=charging_mode,
            cu_count=cu_count,
            description=description,
            queue_type=queue_type,
            queue_name=queue_name,
        )
        return request

    @staticmethod
    def get_job_result_request(job_id, queue_name):
        return DliSdk.PreviewJobResultRequest(job_id=job_id, queue_name=queue_name)

    @staticmethod
    def create_elastic_resource_pool_request(
        elastic_resource_pool_name,
        description,
        cidr_in_vpc,
        max_cu,
        charging_mode,
        min_cu,
        enterprise_project_id,
        tags
    ) -> DliSdk.CreateElasticResourcePoolRequest:
        request = DliSdk.CreateElasticResourcePoolRequest()

        tags = [DliSdk.TmsTag(key=tag["key"], value=tag["value"]) for tag in tags] if tags else None
        request.body = DliSdk.CreateElasticResourcePoolRequestBody(
            elastic_resource_pool_name=elastic_resource_pool_name,
            description=description,
            cidr_in_vpc=cidr_in_vpc,
            max_cu=max_cu,
            charging_mode=charging_mode,
            min_cu=min_cu,
            enterprise_project_id=enterprise_project_id,
            tags=tags,
        )
        return request

    @staticmethod
    def list_elastic_resource_pools_request(
        limit=None, name=None, offset=None, status=None, tags=None
    ) -> DliSdk.ListElasticResourcePoolsRequest:
        return DliSdk.ListElasticResourcePoolsRequest(limit, name, offset, status, tags)

    @staticmethod
    def delete_elastic_resource_pool_request(
        elastic_resource_pool_name
    ) -> DliSdk.DeleteElasticResourcePoolRequest:
        return DliSdk.DeleteElasticResourcePoolRequest(elastic_resource_pool_name)

    @staticmethod
    def associate_connection_queue_request(connection_id, elastic_resource_pools):
        request = DliSdk.AssociateConnectionQueueRequest()
        request.connection_id = connection_id
        request.body = DliSdk.AssociateConnectionQueueReq(elastic_resource_pools=elastic_resource_pools)
        return request

    @staticmethod
    def disassociate_connection_queue_request(
        connection_id, elastic_resource_pools
    ) -> DliSdk.DisassociateConnectionQueueRequest:
        return DliSdk.DisassociateConnectionQueueRequest(
            connection_id=connection_id,
            body=DliSdk.DisassociateConnectionQueueReq(elastic_resource_pools=elastic_resource_pools)
        )

    @staticmethod
    def list_enhanced_connections_request(
        limit, name, offset, status, tags
    ) -> DliSdk.ListEnhancedConnectionsRequest:
        return DliSdk.ListEnhancedConnectionsRequest(limit, name, offset, status, tags)

    @staticmethod
    def list_elastic_resource_pool_queues_request(
        elastic_resource_pool_name, queue_name, limit, offset
    ) -> DliSdk.ListElasticResourcePoolQueuesRequest:
        return DliSdk.ListElasticResourcePoolQueuesRequest(elastic_resource_pool_name, limit, offset)

    @staticmethod
    def delete_enhanced_connection_request(connection_id) -> DliSdk.DeleteEnhancedConnectionRequest:
        return DliSdk.DeleteEnhancedConnectionRequest(connection_id)

    @staticmethod
    def create_enhanced_connection_request(
        name, dest_vpc_id, dest_network_id, routetable_id, hosts, tags
    ) -> DliSdk.CreateEnhancedConnectionRequest:
        body = DliSdk.CreateEnhancedConnectionsReq(
            name=name, dest_vpc_id=dest_vpc_id, dest_network_id=dest_network_id,
            routetable_id=routetable_id, hosts=hosts, tags=tags
        )
        return DliSdk.CreateEnhancedConnectionRequest(body)

    @staticmethod
    def create_route_to_enhanced_connection_request(
        connection_id, name, cidr
    ) -> DliSdk.CreateEnhancedConnectionRoutesRequest:
        return DliSdk.CreateEnhancedConnectionRoutesRequest(
            connection_id=connection_id,
            body=DliSdk.CreateRouteRequestBody(name=name, cidr=cidr)
        )

    @staticmethod
    def delete_route_from_enhanced_connection_request(connection_id, name):
        return DliSdk.DeleteEnhancedConnectionRoutesRequest(connection_id, name)

    @staticmethod
    def show_enhanced_connection_request(connection_id) -> DliSdk.ShowEnhancedConnectionRequest:
        return DliSdk.ShowEnhancedConnectionRequest(connection_id)

    @staticmethod
    def create_connection_task_request(queue_name, address) -> DliSdk.CheckConnectionRequest:
        return DliSdk.CheckConnectionRequest(queue_name, DliSdk.VerityConnectivityReq(address))

    @staticmethod
    def show_node_connectivity_request(queue_name, task_id) -> DliSdk.ShowNodeConnectivityRequest:
        return DliSdk.ShowNodeConnectivityRequest(queue_name, task_id)


class DLIAsyncHook(HuaweiBaseHook):
    async def get_dli_client_async(self) -> DliSdk.DliAsyncClient:
        ak = self.conn.login
        sk = self.conn.password

        credentials = BasicCredentials(ak, sk, self.get_project_id())

        return (
            DliSdk.DliAsyncClient.new_builder()
            .with_credentials(credentials)
            .with_region(DliRegion.value_of(self.get_region()))
            .build()
        )

    async def show_batch_state(self, job_id) -> str:
        try:
            dli_client_async = await self.get_dli_client_async()

            request = DLIHook.show_batch_state_request(job_id)
            response = dli_client_async.show_batch_state_async(request)
            return response.result().state
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when get batch job result: {e}")

    async def show_sql_job_status(self, job_id) -> str:
        try:
            dli_client_async = await self.get_dli_client_async()

            request = DLIHook.show_sql_job_status_request(job_id)
            response = dli_client_async.show_sql_job_status_async(request)
            return response.result().status
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when get sql job result: {e}")

    async def show_elastic_resource_pool_status(self, name) -> str:
        try:
            dli_client_async = await self.get_dli_client_async()

            request = DLIHook.list_elastic_resource_pools_request(name=name)
            response = dli_client_async.list_elastic_resource_pools_async(request)
            pools = response.result().elastic_resource_pools
            for pool in pools:
                if pool.elastic_resource_pool_name == name:
                    return pool.status
            raise Exception(f"There is no elastic resource pool with the name {name} ")
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when show elastic resource pool status: {e}")
