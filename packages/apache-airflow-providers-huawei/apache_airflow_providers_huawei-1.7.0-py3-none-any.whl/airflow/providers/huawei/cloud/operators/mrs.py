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
"""This module contains Huawei Cloud CDM operators."""
from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, Any

from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.exceptions import AirflowException
from airflow.compat.functools import cached_property
from airflow.providers.huawei.cloud.hooks.mrs import MRSHook
from airflow.providers.huawei.cloud.triggers.mrs import MRSCreateExecuteJobTrigger, MRSCreateClusterTrigger

if TYPE_CHECKING:
    pass


class MRSCreateClusterOperator(BaseOperator):
    """
    Create an MRS cluster.

    :param cluster_version: Cluster version. Possible values:

        - MRS 1.9.2
        - MRS 3.1.0
    :param cluster_name: Cluster name. It must be unique.A cluster name can contain only 1 to 64
        characters.Only letters, numbers, hyphens (-), and underscores (_) are allowed.
    :param cluster_type:Cluster type. Possible values:

        - ANALYSIS: analysis cluster
        - STREAMING: streaming cluster
        - MIXED: hybrid cluster
        - CUSTOM: custom cluster, which is supported only by MRS 3.x.
    :param safe_mode: Running mode of an MRS cluster.

        - SIMPLE: normal cluster. In a normal cluster, Kerberos authentication is disabled, and users can
          use all functions provided by the cluster.
        - KERBEROS: security cluster. In a security cluster, Kerberos authentication is enabled, and
          common users cannot use the file management and job management functions of an MRS cluster or
          view cluster resource usage and the job records of Hadoop and Spark. To use more cluster
          functions, the users must contact the Manager administrator to assign more permissions.
    :param manager_admin_password: Password of the MRS Manager administrator.
        The password must meet the following requirements:

            - Must contain 8 to 26 characters.
            - Must contain at least four of the following: uppercase letters, lowercase letters, digits,
              and special characters (!@$%^-_=+[{}]:,./?), but must not contain spaces.
            - Cannot be the username or the username spelled backwards.
    :param login_mode: Node login mode.

        - PASSWORD: password-based login. If this value is selected, node_root_password cannot be left
          blank.
        - KEYPAIR: specifies the key pair used for login. If this value is selected, node_keypair_name
          cannot be left blank.
    :param vpc_name: Name of the VPC where the subnet locates. Perform the following operations to obtain
        the VPC name from the VPC management console:

        - Log in to the management console.
        - Click Virtual Private Cloud and select Virtual Private Cloud from the left list. On the Virtual
          Private Cloud page, obtain the VPC name from the list.
    :param subnet_id: Subnet ID
    :param components: List of component names, which are separated by commas (,).
    :param availability_zone: AZ name. Multi-AZ clusters are not supported.
    :param node_groups: Information about the node groups in the cluster.
    :param is_dec_project: Specifies whether the resource is dedicated to the cloud.
        The default value is false.
    :param charge_info: The billing type.
    :param subnet_name: Subnet name.
    :param external_datasources: External datasource connection when Hive and Ranger components are deployed.
    :param security_groups_id: Security group ID of the cluster.

        - If this parameter is left blank, MRS automatically creates a security group, whose name starts
          with mrs_{cluster_name}.
        - If this parameter is not left blank, a fixed security group is used to create a cluster. The
          transferred ID must be the security group ID owned by the current tenant. The security group
          must include an inbound rule in which all protocols and all ports are allowed and the source
          is the IP address of the specified node on the management plane.
        - Multiple security group ids are supported, separated by commas (,).
    :param auto_create_default_security_group: Specifies whether to create the MRS Cluster default
        security group. The default value is false. If this parameter is set to true, a default security
        group is created for the cluster regardless of whether security_groups_id is specified.
    :param node_root_password: Password of user root for logging in to a cluster node. A password must
        meet the following requirements:

        - Must be 8 to 26 characters long.
        - Must contain at least four of the following: uppercase letters, lowercase letters, digits, and
          special characters (!@$%^-_=+[{}]:,./?), but must not contain spaces.
        - Cannot be the username or the username spelled backwards.
    :param node_keypair_name: Name of a key pair You can use a key pair to log in to the Master node
        in the cluster.
    :param enterprise_project_id: Enterprise project ID。When creating a cluster, associate the enterprise
        project ID with the cluster.The default value is 0, indicating the default enterprise project.
        To obtain the enterprise project ID, see the id value in the enterprise_project field data
        structure table in section Querying the Enterprise Project List of the Enterprise Management
        API Reference.
    :param eip_address: An EIP bound to an MRS cluster can be used to access MRS Manager. The EIP must
        have been created and must be in the same region as the cluster.
    :param eip_id: ID of the bound EIP. This parameter is mandatory when eip_address is configured. To
        obtain the EIP ID, log in to the VPC console, choose Network > Elastic IP and Bandwidth > Elastic
        IP, click the EIP to be bound, and obtain the ID in the Basic Information area.
    :param mrs_ecs_default_agency: Name of the agency bound to a cluster node by default. The value is
        fixed to MRS_ECS_DEFAULT_AGENCY. An agency allows ECS or BMS to manage MRS resources. You can
        configure an agency of the ECS type to automatically obtain the AK/SK to access OBS. The
        MRS_ECS_DEFAULT_AGENCY agency has the OBS OperateAccess permission of OBS and the CES FullAccess
        (for users who have enabled fine-grained policies), CES Administrator, and KMS Administrator
        permissions in the region where the cluster is located.
    :param template_id: Template used for node deployment when the cluster type is CUSTOM.

        - mgmt_control_combined_v2: template for jointly deploying the management and control nodes.
          The management and control roles are co-deployed on the Master node, and data instances are
          deployed in the same node group. This deployment mode applies to scenarios where the number
          of control nodes is less than 100, reducing costs.
        - mgmt_control_separated_v2: The management and control roles are deployed on different master
          nodes, and data instances are deployed in the same node group. This deployment mode is
          applicable to a cluster with 100 to 500 nodes and delivers better performance in
          high-concurrency load scenarios.
        - mgmt_control_data_separated_v2: The management role and control role are deployed on different
          Master nodes, and data instances are deployed in different node groups. This deployment mode
          is applicable to a cluster with more than 500 nodes. Components can be deployed separately,
          which can be used for a larger cluster scale.
    :param tags: Cluster tag For more parameter description.
        A maximum of 10 tags can be added to a cluster, and the tag name (key) must be unique.
    :param log_collection: Specifies whether to collect logs when cluster creation fails.
        The default value is 1, indicating that OBS buckets will be created and only used to collect logs
        that record MRS cluster creation failures. Possible values:

        - 0: Do not collect.
        - 1: Collect.
    :param bootstrap_scripts: Bootstrap action script information.
    :param log_uri: Path where cluster logs are dumped to the OBS. After the log dump function is enabled,
        log uploading requires the read and write permission of the OBS path.  Configure the
        MRS_ECS_DEFULT_AGENCY default delegate or a custom delegate with the read and write permission of
        the OBS path. This parameter applies only to cluster versions that support the 'Cluster Log Dump
        OBS' feature.
    :param component_configs: User-defined configuration for cluster components. This parameter applies
        only to cluster versions that support the Customize Component Configuration Create Cluster feature.
    :param project_id: Project ID.
    :param region: The MRS region.
        By default, the value is obtained from connection corresponding to huaweicloud_conn_id.
        Be associated with project_id.
    :param huaweicloud_conn_id: The Airflow connection used for MRS credentials.
        If this is None or empty then the default obs behaviour is used. If running Airflow in a distributed
        manner and huaweicloud_conn_id is None or empty, then default obs configuration would be used (and
        must be maintained on each worker node).
    :param deferrable: Run operator in the deferrable mode. Default: False
    :param poll_interval: The time interval in seconds to check the state. Default: 10
        This parameter is valid if deferrable is True.
    """

    template_fields: Sequence[str] = (
        "cluster_name",
        "components",
        "node_groups",
        "tags",
    )
    ui_color = "#f0eee4"

    def __init__(
        self,
        cluster_version: str,
        cluster_name: str,
        cluster_type: str,
        safe_mode: str,
        manager_admin_password: str,
        login_mode: str,
        vpc_name: str,
        subnet_id: str,
        components: str,
        availability_zone: str,
        node_groups: list[dict],
        is_dec_project: bool = False,
        charge_info: dict | None = None,
        subnet_name: str | None = None,
        external_datasources: list[dict] | None = None,
        security_groups_id: str | None = None,
        auto_create_default_security_group: bool = False,
        node_root_password: str | None = None,
        node_keypair_name: str | None = None,
        enterprise_project_id: str | None = None,
        eip_address: str | None = None,
        eip_id: str | None = None,
        mrs_ecs_default_agency: str | None = None,
        template_id: str | None = None,
        tags: list[dict] | None = None,
        log_collection: int = 1,
        bootstrap_scripts: list[dict] | None = None,
        log_uri: str | None = None,
        component_configs: list[dict] | None = None,
        project_id: str | None = None,
        poll_interval: int | None = 10,
        deferrable: bool = False,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.is_dec_project = is_dec_project
        self.cluster_version = cluster_version
        self.cluster_name = cluster_name
        self.cluster_type = cluster_type
        self.charge_info = charge_info
        self.vpc_name = vpc_name
        self.subnet_id = subnet_id
        self.subnet_name = subnet_name
        self.components = components
        self.external_datasources = external_datasources
        self.availability_zone = availability_zone
        self.security_groups_id = security_groups_id
        self.auto_create_default_security_group = auto_create_default_security_group
        self.safe_mode = safe_mode
        self.manager_admin_password = manager_admin_password
        self.login_mode = login_mode
        self.node_root_password = node_root_password
        self.node_keypair_name = node_keypair_name
        self.enterprise_project_id = enterprise_project_id
        self.eip_address = eip_address
        self.eip_id = eip_id
        self.mrs_ecs_default_agency = mrs_ecs_default_agency
        self.template_id = template_id
        self.tags = tags
        self.log_collection = log_collection
        self.node_groups = node_groups
        self.bootstrap_scripts = bootstrap_scripts
        self.log_uri = log_uri
        self.component_configs = component_configs
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.deferrable = deferrable
        self.poll_interval = poll_interval
        self.cluster_id = None

    @cached_property
    def hook(self) -> MRSHook:
        hook = MRSHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            region=self.region,
            project_id=self.project_id
        )
        return hook

    def execute(self, context: Context):
        response = self.hook.create_cluster(
            is_dec_project=self.is_dec_project,
            cluster_version=self.cluster_version,
            cluster_name=self.cluster_name,
            cluster_type=self.cluster_type,
            charge_info=self.charge_info,
            vpc_name=self.vpc_name,
            subnet_id=self.subnet_id,
            subnet_name=self.subnet_name,
            components=self.components,
            external_datasources=self.external_datasources,
            availability_zone=self.availability_zone,
            security_groups_id=self.security_groups_id,
            auto_create_default_security_group=self.auto_create_default_security_group,
            safe_mode=self.safe_mode,
            manager_admin_password=self.manager_admin_password,
            login_mode=self.login_mode,
            node_root_password=self.node_root_password,
            node_keypair_name=self.node_keypair_name,
            enterprise_project_id=self.enterprise_project_id,
            eip_address=self.eip_address,
            eip_id=self.eip_id,
            mrs_ecs_default_agency=self.mrs_ecs_default_agency,
            template_id=self.template_id,
            tags=self.tags,
            log_collection=self.log_collection,
            node_groups=self.node_groups,
            bootstrap_scripts=self.bootstrap_scripts,
            log_uri=self.log_uri,
            component_configs=self.component_configs,
        )

        context["ti"].xcom_push(key="return_value", value=response.to_json_object())

        if not self.deferrable:
            return

        self.cluster_id = response.cluster_id
        self.defer(
            trigger=MRSCreateClusterTrigger(
                cluster_id=self.cluster_id,
                poll_interval=self.poll_interval,
                project_id=self.project_id,
                region=self.region,
                huaweicloud_conn_id=self.huaweicloud_conn_id,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context: Context, event: dict[str, Any]):
        if event["status"] == "error":
            raise AirflowException(event["message"])

        self.log.info("Task %s completed with response: %s", self.task_id, event["message"])


class MRSCreateClusterRunJobOperator(BaseOperator):
    """
    Create an MRS cluster and run job.

    :param steps: The jobs list.
    :param cluster_version: Cluster version. Possible values:

        - MRS 1.9.2
        - MRS 3.1.0
    :param cluster_name: Cluster name. It must be unique.A cluster name can contain only 1 to 64
        characters.Only letters, numbers, hyphens (-), and underscores (_) are allowed.
    :param cluster_type:Cluster type. Possible values:

        - ANALYSIS: analysis cluster
        - STREAMING: streaming cluster
        - MIXED: hybrid cluster
        - CUSTOM: custom cluster, which is supported only by MRS 3.x.
    :param safe_mode: Running mode of an MRS cluster.

        - SIMPLE: normal cluster. In a normal cluster, Kerberos authentication is disabled, and users can
          use all functions provided by the cluster.
        - KERBEROS: security cluster. In a security cluster, Kerberos authentication is enabled, and
          common users cannot use the file management and job management functions of an MRS cluster or
          view cluster resource usage and the job records of Hadoop and Spark. To use more cluster
          functions, the users must contact the Manager administrator to assign more permissions.
    :param manager_admin_password: Password of the MRS Manager administrator.
        The password must meet the following requirements:

            - Must contain 8 to 26 characters.
            - Must contain at least four of the following: uppercase letters, lowercase letters, digits,
              and special characters (!@$%^-_=+[{}]:,./?), but must not contain spaces.
            - Cannot be the username or the username spelled backwards.
    :param login_mode: Node login mode.

        - PASSWORD: password-based login. If this value is selected, node_root_password cannot be left
          blank.
        - KEYPAIR: specifies the key pair used for login. If this value is selected, node_keypair_name
          cannot be left blank.
    :param vpc_name: Name of the VPC where the subnet locates. Perform the following operations to obtain
        the VPC name from the VPC management console:

        - Log in to the management console.
        - Click Virtual Private Cloud and select Virtual Private Cloud from the left list. On the Virtual
          Private Cloud page, obtain the VPC name from the list.
    :param subnet_id: Subnet ID
    :param components: List of component names, which are separated by commas (,).
    :param availability_zone: AZ name. Multi-AZ clusters are not supported.
    :param node_groups: Information about the node groups in the cluster.
    :param is_dec_project: Specifies whether the resource is dedicated to the cloud.
        The default value is false.
    :param charge_info: The billing type.
    :param subnet_name: Subnet name.
    :param external_datasources: External datasource connection when Hive and Ranger components are deployed.
    :param security_groups_id: Security group ID of the cluster.

        - If this parameter is left blank, MRS automatically creates a security group, whose name starts
          with mrs_{cluster_name}.
        - If this parameter is not left blank, a fixed security group is used to create a cluster. The
          transferred ID must be the security group ID owned by the current tenant. The security group
          must include an inbound rule in which all protocols and all ports are allowed and the source
          is the IP address of the specified node on the management plane.
        - Multiple security group ids are supported, separated by commas (,).
    :param auto_create_default_security_group: Specifies whether to create the MRS Cluster default
        security group. The default value is false. If this parameter is set to true, a default security
        group is created for the cluster regardless of whether security_groups_id is specified.
    :param node_root_password: Password of user root for logging in to a cluster node. A password must
        meet the following requirements:

        - Must be 8 to 26 characters long.
        - Must contain at least four of the following: uppercase letters, lowercase letters, digits, and
          special characters (!@$%^-_=+[{}]:,./?), but must not contain spaces.
        - Cannot be the username or the username spelled backwards.
    :param node_keypair_name: Name of a key pair You can use a key pair to log in to the Master node
        in the cluster.
    :param enterprise_project_id: Enterprise project ID。When creating a cluster, associate the enterprise
        project ID with the cluster.The default value is 0, indicating the default enterprise project.
        To obtain the enterprise project ID, see the id value in the enterprise_project field data
        structure table in section Querying the Enterprise Project List of the Enterprise Management
        API Reference.
    :param eip_address: An EIP bound to an MRS cluster can be used to access MRS Manager. The EIP must
        have been created and must be in the same region as the cluster.
    :param eip_id: ID of the bound EIP. This parameter is mandatory when eip_address is configured. To
        obtain the EIP ID, log in to the VPC console, choose Network > Elastic IP and Bandwidth > Elastic
        IP, click the EIP to be bound, and obtain the ID in the Basic Information area.
    :param mrs_ecs_default_agency: Name of the agency bound to a cluster node by default. The value is
        fixed to MRS_ECS_DEFAULT_AGENCY. An agency allows ECS or BMS to manage MRS resources. You can
        configure an agency of the ECS type to automatically obtain the AK/SK to access OBS. The
        MRS_ECS_DEFAULT_AGENCY agency has the OBS OperateAccess permission of OBS and the CES FullAccess
        (for users who have enabled fine-grained policies), CES Administrator, and KMS Administrator
        permissions in the region where the cluster is located.
    :param template_id: Template used for node deployment when the cluster type is CUSTOM.

        - mgmt_control_combined_v2: template for jointly deploying the management and control nodes.
          The management and control roles are co-deployed on the Master node, and data instances are
          deployed in the same node group. This deployment mode applies to scenarios where the number
          of control nodes is less than 100, reducing costs.
        - mgmt_control_separated_v2: The management and control roles are deployed on different master
          nodes, and data instances are deployed in the same node group. This deployment mode is
          applicable to a cluster with 100 to 500 nodes and delivers better performance in
          high-concurrency load scenarios.
        - mgmt_control_data_separated_v2: The management role and control role are deployed on different
          Master nodes, and data instances are deployed in different node groups. This deployment mode
          is applicable to a cluster with more than 500 nodes. Components can be deployed separately,
          which can be used for a larger cluster scale.
    :param tags: Cluster tag For more parameter description.
        A maximum of 10 tags can be added to a cluster, and the tag name (key) must be unique.
    :param log_collection: Specifies whether to collect logs when cluster creation fails.
        The default value is 1, indicating that OBS buckets will be created and only used to collect logs
        that record MRS cluster creation failures. Possible values:

        - 0: Do not collect.
        - 1: Collect.
    :param bootstrap_scripts: Bootstrap action script information.
    :param log_uri: Path where cluster logs are dumped to the OBS. After the log dump function is enabled,
        log uploading requires the read and write permission of the OBS path.  Configure the
        MRS_ECS_DEFULT_AGENCY default delegate or a custom delegate with the read and write permission of
        the OBS path. This parameter applies only to cluster versions that support the 'Cluster Log Dump
        OBS' feature.
    :param component_configs: User-defined configuration for cluster components. This parameter applies
        only to cluster versions that support the Customize Component Configuration Create Cluster feature.
    :param delete_when_no_steps: Whether to automatically delete the cluster after the job is complete.
        The default value is false.
    :param project_id: Project ID.
    :param region: The MRS region.
        By default, the value is obtained from connection corresponding to huaweicloud_conn_id.
        Be associated with project_id.
    :param huaweicloud_conn_id: The Airflow connection used for MRS credentials.
        If this is None or empty then the default obs behaviour is used. If running Airflow in a distributed
        manner and huaweicloud_conn_id is None or empty, then default obs configuration would be used (and
        must be maintained on each worker node).
    """

    template_fields: Sequence[str] = (
        "steps",
        "cluster_name",
        "components",
        "tags",
    )
    ui_color = "#f0eee4"

    def __init__(
        self,
        steps: list[dict],
        cluster_version: str,
        cluster_name: str,
        cluster_type: str,
        safe_mode: str,
        manager_admin_password: str,
        login_mode: str,
        vpc_name: str,
        subnet_id: str,
        components: str,
        availability_zone: str,
        node_groups: list[dict],
        is_dec_project: bool = False,
        charge_info: dict | None = None,
        subnet_name: str | None = None,
        external_datasources: list[dict] | None = None,
        security_groups_id: str | None = None,
        auto_create_default_security_group: bool = False,
        node_root_password: str | None = None,
        node_keypair_name: str | None = None,
        enterprise_project_id: str | None = None,
        eip_address: str | None = None,
        eip_id: str | None = None,
        mrs_ecs_default_agency: str | None = None,
        template_id: str | None = None,
        tags: list[dict] | None = None,
        log_collection: int = 1,
        bootstrap_scripts: list[dict] | None = None,
        log_uri: str | None = None,
        component_configs: list[dict] | None = None,
        delete_when_no_steps: bool | None = False,
        project_id: str | None = None,
        region: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.steps = steps
        self.is_dec_project = is_dec_project
        self.cluster_version = cluster_version
        self.cluster_name = cluster_name
        self.cluster_type = cluster_type
        self.charge_info = charge_info
        self.vpc_name = vpc_name
        self.subnet_id = subnet_id
        self.subnet_name = subnet_name
        self.components = components
        self.external_datasources = external_datasources
        self.availability_zone = availability_zone
        self.security_groups_id = security_groups_id
        self.auto_create_default_security_group = auto_create_default_security_group
        self.safe_mode = safe_mode
        self.manager_admin_password = manager_admin_password
        self.login_mode = login_mode
        self.node_root_password = node_root_password
        self.node_keypair_name = node_keypair_name
        self.enterprise_project_id = enterprise_project_id
        self.eip_address = eip_address
        self.eip_id = eip_id
        self.mrs_ecs_default_agency = mrs_ecs_default_agency
        self.template_id = template_id
        self.tags = tags
        self.log_collection = log_collection
        self.node_groups = node_groups
        self.bootstrap_scripts = bootstrap_scripts
        self.log_uri = log_uri
        self.component_configs = component_configs
        self.delete_when_no_steps = delete_when_no_steps
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def execute(self, context: Context):
        mrs_hook = MRSHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )

        return mrs_hook.create_cluster_run_job(
            steps=self.steps,
            is_dec_project=self.is_dec_project,
            cluster_version=self.cluster_version,
            cluster_name=self.cluster_name,
            cluster_type=self.cluster_type,
            charge_info=self.charge_info,
            vpc_name=self.vpc_name,
            subnet_id=self.subnet_id,
            subnet_name=self.subnet_name,
            components=self.components,
            external_datasources=self.external_datasources,
            availability_zone=self.availability_zone,
            security_groups_id=self.security_groups_id,
            auto_create_default_security_group=self.auto_create_default_security_group,
            safe_mode=self.safe_mode,
            manager_admin_password=self.manager_admin_password,
            login_mode=self.login_mode,
            node_root_password=self.node_root_password,
            node_keypair_name=self.node_keypair_name,
            enterprise_project_id=self.enterprise_project_id,
            eip_address=self.eip_address,
            eip_id=self.eip_id,
            mrs_ecs_default_agency=self.mrs_ecs_default_agency,
            template_id=self.template_id,
            tags=self.tags,
            log_collection=self.log_collection,
            node_groups=self.node_groups,
            bootstrap_scripts=self.bootstrap_scripts,
            log_uri=self.log_uri,
            component_configs=self.component_configs,
            delete_when_no_steps=self.delete_when_no_steps,
        ).to_json_object()


class MRSDeleteClusterOperator(BaseOperator):
    """
    Delete a cluster.

    :param cluster_id: The cluster ID.
    """

    template_fields: Sequence[str] = ("cluster_id",)
    ui_color = "#f0eee4"

    def __init__(
        self,
        cluster_id: str,
        region: str | None = None,
        project_id: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.cluster_id = cluster_id
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id

    def execute(self, context: Context):
        mrs_hook = MRSHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id, region=self.region, project_id=self.project_id
        )
        return mrs_hook.delete_cluster(cluster_id=self.cluster_id).to_json_object()


class MRSCreateExecuteJobOperator(BaseOperator):
    """
    Add and submit a job in an MRS Cluster.

    :param job_type: Type of job.
    :param cluster_id: The cluster ID.
    :param job_name: Job name.
    :param arguments: Key parameter for program execution.
    :param properties: Program system parameter.
    :param project_id: Project ID.
    :param region: The MRS region.
        By default, the value is obtained from connection corresponding to huaweicloud_conn_id.
        Be associated with project_id.
    :param huaweicloud_conn_id: The Airflow connection used for MRS credentials.
        If this is None or empty then the default obs behaviour is used. If running Airflow in a distributed
        manner and huaweicloud_conn_id is None or empty, then default obs configuration would be used (and
        must be maintained on each worker node).
    :param deferrable: Run operator in the deferrable mode. Default: False
    :param poll_interval: The time interval in seconds to check the state. Default: 10
        This parameter is valid if deferrable is True.
    """

    template_fields: Sequence[str] = ("job_type", "job_name", "cluster_id", "arguments", "properties")
    ui_color = "#f0eee4"

    def __init__(
        self,
        job_type: str,
        job_name: str,
        cluster_id: str,
        arguments: list | None = None,
        properties: dict | None = None,
        poll_interval: int | None = 10,
        deferrable: bool = False,
        region: str | None = None,
        project_id: str | None = None,
        huaweicloud_conn_id: str = "huaweicloud_default",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.job_type = job_type
        self.job_name = job_name
        self.cluster_id = cluster_id
        self.arguments = arguments
        self.properties = properties
        self.poll_interval = poll_interval
        self.deferrable = deferrable
        self.region = region
        self.project_id = project_id
        self.huaweicloud_conn_id = huaweicloud_conn_id
        self.job_id = None

    @cached_property
    def hook(self) -> MRSHook:
        hook = MRSHook(
            huaweicloud_conn_id=self.huaweicloud_conn_id,
            region=self.region,
            project_id=self.project_id
        )
        return hook

    def execute(self, context: Context):
        response = self.hook.create_execute_job(
            job_type=self.job_type,
            job_name=self.job_name,
            cluster_id=self.cluster_id,
            arguments=self.arguments,
            properties=self.properties,
        )

        context["ti"].xcom_push(key="return_value", value=response.to_json_object().get("job_submit_result"))

        if not self.deferrable:
            return

        self.job_id = response.job_submit_result.job_id

        self.defer(
            trigger=MRSCreateExecuteJobTrigger(
                job_id=self.job_id,
                cluster_id=self.cluster_id,
                poll_interval=self.poll_interval,
                project_id=self.project_id,
                region=self.region,
                huaweicloud_conn_id=self.huaweicloud_conn_id,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context: Context, event: dict[str, Any]):
        if event["status"] == "error":
            raise AirflowException(event["message"])

        self.log.info("Task %s completed with response: %s", self.task_id, event["message"])

    def on_kill(self) -> None:
        self.log.info("On kill.")
        for ti in self.get_task_instances():
            if ti.state == "running":
                self.job_id = ti.xcom_pull(task_ids=ti.task_id, key="return_value").get("job_id")

        if self.job_id is not None:
            self.log.info("stop job %s", self.job_id)
            self.hook.stop_job(self.cluster_id, self.job_id)
