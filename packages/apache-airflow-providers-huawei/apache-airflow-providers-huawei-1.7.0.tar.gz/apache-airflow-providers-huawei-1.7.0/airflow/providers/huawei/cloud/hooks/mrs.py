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

import huaweicloudsdkmrs.v2 as MrsV2Sdk
import huaweicloudsdkmrs.v1 as MrsV1Sdk

from huaweicloudsdkmrs.v2.region.mrs_region import MrsRegion
from huaweicloudsdkcore.auth.credentials import BasicCredentials

from airflow.exceptions import AirflowException
from airflow.providers.huawei.cloud.hooks.base_huawei_cloud import HuaweiBaseHook


class MRSHook(HuaweiBaseHook):
    """Interact with Huawei Cloud MRS, using the huaweicloudsdkmrs library."""

    def get_mrs_client(self, version: str = 'v2') -> MrsV2Sdk.MrsClient | MrsV1Sdk.MrsClient:
        ak = self.conn.login
        sk = self.conn.password

        credentials = BasicCredentials(ak=ak, sk=sk, project_id=self.get_project_id())
        mrs_client = MrsV2Sdk.MrsClient
        if version == 'v1':
            mrs_client = MrsV1Sdk.MrsClient
        return (
            mrs_client.new_builder()
            .with_credentials(credentials)
            .with_region(MrsRegion.value_of(self.get_region()))
            .build()
        )

    def create_cluster(
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
    ) -> MrsV2Sdk.CreateClusterResponse:
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
        """
        try:
            region = self.get_region()
            node_groups = self._get_node_groups(node_groups)
            if charge_info:
                charge_info = self._get_charge_info(charge_info)
            else:
                charge_info = MrsV2Sdk.ChargeInfo(charge_mode="postPaid")
            if tags:
                tags = [MrsV2Sdk.Tag(tag['key'], tag['value']) for tag in tags]
            if external_datasources:
                external_datasources = self._get_external_datasources(external_datasources)
            if bootstrap_scripts:
                bootstrap_scripts = self._get_bootstrap_scripts(bootstrap_scripts)
            if component_configs:
                component_configs = self._get_component_configs(component_configs)

            request = MrsV2Sdk.CreateClusterRequest()
            request.body = MrsV2Sdk.CreateClusterReqV2(
                is_dec_project=is_dec_project,
                cluster_version=cluster_version,
                cluster_name=cluster_name,
                cluster_type=cluster_type,
                charge_info=charge_info,
                region=region,
                vpc_name=vpc_name,
                subnet_id=subnet_id,
                subnet_name=subnet_name,
                components=components,
                external_datasources=external_datasources,
                availability_zone=availability_zone,
                security_groups_id=security_groups_id,
                auto_create_default_security_group=auto_create_default_security_group,
                safe_mode=safe_mode,
                manager_admin_password=manager_admin_password,
                login_mode=login_mode,
                node_root_password=node_root_password,
                node_keypair_name=node_keypair_name,
                enterprise_project_id=enterprise_project_id,
                eip_address=eip_address,
                eip_id=eip_id,
                mrs_ecs_default_agency=mrs_ecs_default_agency,
                template_id=template_id,
                tags=tags,
                log_collection=log_collection,
                node_groups=node_groups,
                bootstrap_scripts=bootstrap_scripts,
                log_uri=log_uri,
                component_configs=component_configs,
            )
            return self.get_mrs_client().create_cluster(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f'Error when creating cluster({e}).')

    def create_cluster_run_job(
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
    ) -> MrsV2Sdk.RunJobFlowResponse:
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
        """
        try:
            region = self.get_region()
            if charge_info:
                charge_info = self._get_charge_info(charge_info)
            else:
                charge_info = MrsV2Sdk.ChargeInfo(charge_mode="postPaid")
            node_groups = self._get_node_groups(node_groups)
            if tags:
                tags = [MrsV2Sdk.Tag(tag['key'], tag['value']) for tag in tags]
            if external_datasources:
                external_datasources = self._get_external_datasources(external_datasources)
            if bootstrap_scripts:
                bootstrap_scripts = self._get_bootstrap_scripts(bootstrap_scripts)
            if component_configs:
                component_configs = self._get_component_configs(component_configs)
            steps = self._get_steps(steps)
            if delete_when_no_steps:
                self.log.info("The cluster is automatically deleted after all jobs are completed.")

            request = MrsV2Sdk.RunJobFlowRequest()
            request.body = MrsV2Sdk.RunJobFlowCommand(
                is_dec_project=is_dec_project,
                cluster_version=cluster_version,
                cluster_name=cluster_name,
                cluster_type=cluster_type,
                charge_info=charge_info,
                region=region,
                vpc_name=vpc_name,
                subnet_id=subnet_id,
                subnet_name=subnet_name,
                components=components,
                external_datasources=external_datasources,
                availability_zone=availability_zone,
                security_groups_id=security_groups_id,
                auto_create_default_security_group=auto_create_default_security_group,
                safe_mode=safe_mode,
                manager_admin_password=manager_admin_password,
                login_mode=login_mode,
                node_root_password=node_root_password,
                node_keypair_name=node_keypair_name,
                enterprise_project_id=enterprise_project_id,
                eip_address=eip_address,
                eip_id=eip_id,
                mrs_ecs_default_agency=mrs_ecs_default_agency,
                template_id=template_id,
                tags=tags,
                log_collection=log_collection,
                node_groups=node_groups,
                bootstrap_scripts=bootstrap_scripts,
                log_uri=log_uri,
                component_configs=component_configs,
                delete_when_no_steps=delete_when_no_steps,
                steps=steps,
            )
            return self.get_mrs_client().run_job_flow(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f'Error when creating cluster and running job({e}).')

    def delete_cluster(self, cluster_id: str) -> MrsV1Sdk.DeleteClusterResponse:
        """
        Delete a cluster.

        :param cluster_id: The cluster ID.
        """
        try:
            request = MrsV1Sdk.DeleteClusterRequest(cluster_id=cluster_id)
            return self.get_mrs_client(version='v1').delete_cluster(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when deleting cluster({e}).")

    def show_cluster_details(self, cluster_id: str) -> MrsV1Sdk.ShowClusterDetailsResponse:
        """
        Show cluster details.

        :param cluster_id: The cluster ID.
        """
        try:
            request = MrsV1Sdk.ShowClusterDetailsRequest(cluster_id=cluster_id)
            return self.get_mrs_client(version='v1').show_cluster_details(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when showing cluster details({e}).")

    def create_execute_job(
        self,
        job_type: str,
        job_name: str,
        cluster_id: str,
        arguments: list | None = None,
        properties: dict | None = None,
    ) -> MrsV2Sdk.CreateExecuteJobResponse:
        try:
            body = MrsV2Sdk.JobExecution(
                job_type=job_type,
                job_name=job_name,
                arguments=arguments,
                properties=properties,
            )
            request = MrsV2Sdk.CreateExecuteJobRequest(cluster_id=cluster_id, body=body)
            return self.get_mrs_client().create_execute_job(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when create and execute job details({e}).")

    def show_single_job_exe(self, job_id: str, cluster_id: str):
        try:
            request = MrsV2Sdk.ShowSingleJobExeRequest(job_id, cluster_id)
            return self.get_mrs_client().show_single_job_exe(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when show single job result: {e}")

    def stop_job(self, cluster_id: str, job_id: str) -> MrsV2Sdk.StopJobResponse:
        try:
            request = MrsV2Sdk.StopJobRequest(job_id, cluster_id)
            return self.get_mrs_client().stop_job(request)
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when stop job({e}).")

    @staticmethod
    def _get_charge_info(charge_info) -> MrsV2Sdk.ChargeInfo:
        return MrsV2Sdk.ChargeInfo(
            charge_mode=charge_info.get('charge_mode'),
            period_type=charge_info.get('period_type'),
            period_num=charge_info.get('period_num'),
            is_auto_pay=charge_info.get('is_auto_pay'),
        )

    @staticmethod
    def _get_job_execution(step) -> MrsV2Sdk.JobExecution:
        return MrsV2Sdk.JobExecution(
            job_type=step.get('job_type'),
            job_name=step.get('job_name'),
            arguments=step.get('arguments'),
            properties=step.get('properties'),
        )

    def _get_steps(self, steps) -> list[MrsV2Sdk.StepConfig]:
        steps = [
            MrsV2Sdk.StepConfig(self._get_job_execution(step))
            for step in steps
        ]
        return steps

    @staticmethod
    def _get_configs(configs) -> list[MrsV2Sdk.Config] | None:
        if configs:
            configs = [
                MrsV2Sdk.Config(
                    key=config.get('key'),
                    value=config.get('value'),
                    config_file_name=config.get('config_file_name'),
                )
                for config in configs
            ]
            return configs

    def _get_component_configs(self, component_configs) -> list[MrsV2Sdk.ComponentConfig]:
        component_configs = [
            MrsV2Sdk.ComponentConfig(
                component_name=component_config.get('component_name'),
                configs=self._get_configs(component_config.get('configs'))
            )
            for component_config in component_configs
        ]
        return component_configs

    @staticmethod
    def _get_resources_plans(resources_plans) -> list[MrsV2Sdk.ResourcesPlan] | None:
        resources_plans = [
            MrsV2Sdk.ResourcesPlan(
                period_type=resources_plan.get('period_type'),
                start_time=resources_plan.get('start_time'),
                end_time=resources_plan.get('end_time'),
                max_capacity=resources_plan.get('max_capacity'),
                effective_days=resources_plan.get('effective_days'),
            )
            for resources_plan in resources_plans
        ] if resources_plans else None
        return resources_plans

    @staticmethod
    def _get_trigger(trigger) -> MrsV2Sdk.Trigger:
        return MrsV2Sdk.Trigger(
            metric_name=trigger.get('metric_name'),
            metric_value=trigger.get('metric_value'),
            comparison_operator=trigger.get('comparison_operator'),
            evaluation_periods=trigger.get('evaluation_periods'),
        )

    def _get_rules(self, rules) -> list[MrsV2Sdk.Rule] | None:
        rules = [
            MrsV2Sdk.Rule(
                name=rule.get('name'),
                description=rule.get('description'),
                adjustment_type=rule.get('adjustment_type'),
                cool_down_minutes=rule.get('cool_down_minutes'),
                scaling_adjustment=rule.get('scaling_adjustment'),
                trigger=self._get_trigger(rule.get('trigger')),
            )
            for rule in rules
        ] if rules else None
        return rules

    @staticmethod
    def _get_exec_scripts(exec_scripts) -> list[MrsV2Sdk.ScaleScript] | None:
        exec_scripts = [
            MrsV2Sdk.ScaleScript(
                name=exec_script.get('name'),
                uri=exec_script.get('uri'),
                parameters=exec_script.get('parameters'),
                nodes=exec_script.get('nodes'),
                active_master=exec_script.get('active_master'),
                fail_action=exec_script.get('fail_action'),
                action_stage=exec_script.get('action_stage'),
            )
            for exec_script in exec_scripts
        ] if exec_scripts else None
        return exec_scripts

    def _get_auto_scaling_policy(self, auto_scaling_policy) -> MrsV2Sdk.AutoScalingPolicy | None:
        if auto_scaling_policy:
            return MrsV2Sdk.AutoScalingPolicy(
                auto_scaling_enable=auto_scaling_policy.get('auto_scaling_enable'),
                min_capacity=auto_scaling_policy.get('min_capacity'),
                max_capacity=auto_scaling_policy.get('max_capacity'),
                resources_plans=self._get_resources_plans(auto_scaling_policy.get('resources_plans')),
                rules=self._get_rules(auto_scaling_policy.get('rules')),
                exec_scripts=self._get_exec_scripts(auto_scaling_policy.get('exec_scripts')),
            )

    @staticmethod
    def _get_volume(volume) -> MrsV2Sdk.Volume | None:
        if volume:
            return MrsV2Sdk.Volume(
                type=volume.get('type'),
                size=volume.get('size'),
            )

    def _get_node_groups(self, node_groups) -> list[MrsV2Sdk.NodeGroupV2]:
        node_groups = [
            MrsV2Sdk.NodeGroupV2(
                group_name=node_group.get('group_name'),
                node_num=node_group.get('node_num'),
                node_size=node_group.get('node_size'),
                root_volume=self._get_volume(node_group.get('root_volume')),
                data_volume=self._get_volume(node_group.get('data_volume')),
                data_volume_count=node_group.get('data_volume_count'),
                charge_info=node_group.get('charge_info'),
                auto_scaling_policy=self._get_auto_scaling_policy(node_group.get('auto_scaling_policy')),
                assigned_roles=node_group.get('assigned_roles'),
            )
            for node_group in node_groups
        ]
        return node_groups

    @staticmethod
    def _get_external_datasources(external_datasources) -> list[MrsV2Sdk.ClusterDataConnectorMap]:
        external_datasources = [
            MrsV2Sdk.ClusterDataConnectorMap(
                map_id=external_datasource.get('map_id'),
                connector_id=external_datasource.get('connector_id'),
                component_name=external_datasource.get('component_name'),
                role_type=external_datasource.get('role_type'),
                source_type=external_datasource.get('source_type'),
                cluster_id=external_datasource.get('cluster_id'),
                status=external_datasource.get('status'),
            )
            for external_datasource in external_datasources
        ]
        return external_datasources

    @staticmethod
    def _get_bootstrap_scripts(bootstrap_scripts) -> list[MrsV2Sdk.BootstrapScript]:
        bootstrap_scripts = [
            MrsV2Sdk.BootstrapScript(
                name=bootstrap_script.get('name'),
                uri=bootstrap_script.get('uri'),
                parameters=bootstrap_script.get('parameters'),
                nodes=bootstrap_script.get('nodes'),
                active_master=bootstrap_script.get('active_master'),
                fail_action=bootstrap_script.get('fail_action'),
                before_component_start=bootstrap_script.get('before_component_start'),
                start_time=bootstrap_script.get('start_time'),
                state=bootstrap_script.get('state'),
                action_stages=bootstrap_script.get('action_stages'),
            )
            for bootstrap_script in bootstrap_scripts
        ]
        return bootstrap_scripts


class MRSAsyncHook(HuaweiBaseHook):
    async def get_mrs_client_async(self,
                                   version: str = 'v2') -> MrsV1Sdk.MrsAsyncClient | MrsV2Sdk.MrsAsyncClient:
        ak = self.conn.login
        sk = self.conn.password

        credentials = BasicCredentials(ak=ak, sk=sk, project_id=self.get_project_id())
        mrs_client_async = MrsV2Sdk.MrsAsyncClient
        if version == 'v1':
            mrs_client_async = MrsV1Sdk.MrsAsyncClient
        return (
            mrs_client_async.new_builder()
            .with_credentials(credentials)
            .with_region(MrsRegion.value_of(self.get_region()))
            .build()
        )

    async def show_single_job_exe(self, job_id, cluster_id):
        try:
            mrs_client_async = await self.get_mrs_client_async()

            request = MrsV2Sdk.ShowSingleJobExeRequest(job_id, cluster_id)
            response = mrs_client_async.show_single_job_exe_async(request)
            return response.result()
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when show single job result: {e}")

    async def show_cluster_details(self, cluster_id: str) -> MrsV1Sdk.ShowClusterDetailsResponse:
        try:
            mrs_client_async = await self.get_mrs_client_async(version='v1')

            request = MrsV1Sdk.ShowClusterDetailsRequest(cluster_id=cluster_id)
            response = mrs_client_async.show_cluster_details_async(request)
            return response.result()
        except Exception as e:
            self.log.error(e)
            raise AirflowException(f"Errors when showing cluster details({e}).")
