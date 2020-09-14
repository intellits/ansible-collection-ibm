#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_is_instance_group_manager
short_description: Configure IBM Cloud 'ibm_is_instance_group_manager' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_is_instance_group_manager' resource
    - This module supports idempotency
requirements:
    - IBM-Cloud terraform-provider-ibm v1.12.0
    - Terraform v0.12.20

options:
    manager_type:
        description:
            - The type of instance group manager.
        required: False
        type: str
        default: autoscale
    max_membership_count:
        description:
            - (Required for new resource) The maximum number of members in a managed instance group
        required: True
        type: int
    min_membership_count:
        description:
            - The minimum number of members in a managed instance group
        required: False
        type: int
        default: 1
    name:
        description:
            - instance group manager name
        required: False
        type: str
    enable_manager:
        description:
            - enable instance group manager
        required: False
        type: bool
        default: True
    instance_group:
        description:
            - (Required for new resource) instance group ID
        required: True
        type: str
    aggregation_window:
        description:
            - The time window in seconds to aggregate metrics prior to evaluation
        required: False
        type: int
        default: 90
    cooldown:
        description:
            - The duration of time in seconds to pause further scale actions after scaling has taken place
        required: False
        type: int
        default: 300
    id:
        description:
            - (Required when updating or destroying existing resource) IBM Cloud Resource ID.
        required: False
        type: str
    state:
        description:
            - State of resource
        choices:
            - available
            - absent
        default: available
        required: False
    generation:
        description:
            - The generation of Virtual Private Cloud infrastructure
              that you want to use. Supported values are 1 for VPC
              generation 1, and 2 for VPC generation 2 infrastructure.
              If this value is not specified, 2 is used by default. This
              can also be provided via the environment variable
              'IC_GENERATION'.
        default: 2
        required: False
        type: int
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
        type: str
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True

author:
    - Jay Carman (@jaywcarman)
'''

# Top level parameter keys required by Terraform module
TL_REQUIRED_PARAMETERS = [
    ('max_membership_count', 'int'),
    ('instance_group', 'str'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'manager_type',
    'max_membership_count',
    'min_membership_count',
    'name',
    'enable_manager',
    'instance_group',
    'aggregation_window',
    'cooldown',
]

# Params for Data source
TL_REQUIRED_PARAMETERS_DS = [
    ('instance_group', 'str'),
    ('name', 'str'),
]

TL_ALL_PARAMETERS_DS = [
    'instance_group',
    'name',
]

TL_CONFLICTS_MAP = {
}

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    manager_type=dict(
        required=False,
        type='str'),
    max_membership_count=dict(
        required=False,
        type='int'),
    min_membership_count=dict(
        required=False,
        type='int'),
    name=dict(
        required=False,
        type='str'),
    enable_manager=dict(
        required=False,
        type='bool'),
    instance_group=dict(
        required=False,
        type='str'),
    aggregation_window=dict(
        required=False,
        type='int'),
    cooldown=dict(
        required=False,
        type='int'),
    id=dict(
        required=False,
        type='str'),
    state=dict(
        type='str',
        required=False,
        default='available',
        choices=(['available', 'absent'])),
    generation=dict(
        type='int',
        required=False,
        fallback=(env_fallback, ['IC_GENERATION']),
        default=2),
    region=dict(
        type='str',
        fallback=(env_fallback, ['IC_REGION']),
        default='us-south'),
    ibmcloud_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IC_API_KEY']),
        required=True)
)


def run_module():
    from ansible.module_utils.basic import AnsibleModule

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # New resource required arguments checks
    missing_args = []
    if module.params['id'] is None:
        for arg, _ in TL_REQUIRED_PARAMETERS:
            if module.params[arg] is None:
                missing_args.append(arg)
        if missing_args:
            module.fail_json(msg=(
                "missing required arguments: " + ", ".join(missing_args)))

    conflicts = {}
    if len(TL_CONFLICTS_MAP) != 0:
        for arg in TL_CONFLICTS_MAP:
            if module.params[arg]:
                for conflict in TL_CONFLICTS_MAP[arg]:
                    try:
                        if module.params[conflict]:
                            conflicts[arg] = conflict
                    except KeyError:
                        pass
    if len(conflicts):
        module.fail_json(msg=("conflicts exist: {}".format(conflicts)))

    # VPC required arguments checks
    if module.params['generation'] == 1:
        missing_args = []
        if module.params['iaas_classic_username'] is None:
            missing_args.append('iaas_classic_username')
        if module.params['iaas_classic_api_key'] is None:
            missing_args.append('iaas_classic_api_key')
        if missing_args:
            module.fail_json(msg=(
                "VPC generation=1 missing required arguments: " +
                ", ".join(missing_args)))
    elif module.params['generation'] == 2:
        if module.params['ibmcloud_api_key'] is None:
            module.fail_json(
                msg=("VPC generation=2 missing required argument: "
                     "ibmcloud_api_key"))

    result_ds = ibmcloud_terraform(
        resource_type='ibm_is_instance_group_manager',
        tf_type='data',
        parameters=module.params,
        ibm_provider_version='1.12.0',
        tl_required_params=TL_REQUIRED_PARAMETERS_DS,
        tl_all_params=TL_ALL_PARAMETERS_DS)

    if result_ds['rc'] != 0 or (result_ds['rc'] == 0 and (module.params['id'] is not None or module.params['state'] == 'absent')):
        result = ibmcloud_terraform(
            resource_type='ibm_is_instance_group_manager',
            tf_type='resource',
            parameters=module.params,
            ibm_provider_version='1.12.0',
            tl_required_params=TL_REQUIRED_PARAMETERS,
            tl_all_params=TL_ALL_PARAMETERS)
        if result['rc'] > 0:
            module.fail_json(
                msg=Terraform.parse_stderr(result['stderr']), **result)

        module.exit_json(**result)
    else:
        module.exit_json(**result_ds)


def main():
    run_module()


if __name__ == '__main__':
    main()
