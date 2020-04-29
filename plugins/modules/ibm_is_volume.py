#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_is_volume
short_description: Configure IBM Cloud 'ibm_is_volume' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_is_volume' resource

requirements:
    - IBM-Cloud terraform-provider-ibm v1.5.0
    - Terraform v0.12.20

options:
    encryption_key:
        description:
            - Volume encryption key info
        required: False
        type: str
    capacity:
        description:
            - Vloume capacity value
        required: False
        type: int
        default: 100
    tags:
        description:
            - Tags for the volume instance
        required: False
        type: list
        elements: str
    crn:
        description:
            - CRN value for the volume instance
        required: False
        type: str
    status:
        description:
            - Volume status
        required: False
        type: str
    resource_crn:
        description:
            - The crn of the resource
        required: False
        type: str
    zone:
        description:
            - (Required for new resource) Zone name
        required: False
        type: str
    resource_group:
        description:
            - Resource group name
        required: False
        type: str
    iops:
        description:
            - IOPS value for the Volume
        required: False
        type: int
    resource_controller_url:
        description:
            - The URL of the IBM Cloud dashboard that can be used to explore and view details about this instance
        required: False
        type: str
    name:
        description:
            - (Required for new resource) Volume name
        required: False
        type: str
    profile:
        description:
            - (Required for new resource) Vloume profile name
        required: False
        type: str
    resource_name:
        description:
            - The name of the resource
        required: False
        type: str
    resource_status:
        description:
            - The status of the resource
        required: False
        type: str
    resource_group_name:
        description:
            - The resource group name in which resource is provisioned
        required: False
        type: str
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
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
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
    ('zone', 'str'),
    ('name', 'str'),
    ('profile', 'str'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'encryption_key',
    'capacity',
    'tags',
    'crn',
    'status',
    'resource_crn',
    'zone',
    'resource_group',
    'iops',
    'resource_controller_url',
    'name',
    'profile',
    'resource_name',
    'resource_status',
    'resource_group_name',
]

# define available arguments/parameters a user can pass to the module
from ansible.module_utils.basic import env_fallback
module_args = dict(
    encryption_key=dict(
        required=False,
        type='str'),
    capacity=dict(
        default=100,
        type='int'),
    tags=dict(
        required=False,
        elements='',
        type='list'),
    crn=dict(
        required=False,
        type='str'),
    status=dict(
        required=False,
        type='str'),
    resource_crn=dict(
        required=False,
        type='str'),
    zone=dict(
        required=False,
        type='str'),
    resource_group=dict(
        required=False,
        type='str'),
    iops=dict(
        required=False,
        type='int'),
    resource_controller_url=dict(
        required=False,
        type='str'),
    name=dict(
        required=False,
        type='str'),
    profile=dict(
        required=False,
        type='str'),
    resource_name=dict(
        required=False,
        type='str'),
    resource_status=dict(
        required=False,
        type='str'),
    resource_group_name=dict(
        required=False,
        type='str'),
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
    import ansible.module_utils.ibmcloud as ibmcloud

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

    result = ibmcloud.ibmcloud_terraform(
        resource_type='ibm_is_volume',
        tf_type='resource',
        parameters=module.params,
        ibm_provider_version='1.5.0',
        tl_required_params=TL_REQUIRED_PARAMETERS,
        tl_all_params=TL_ALL_PARAMETERS)

    if result['rc'] > 0:
        module.fail_json(
            msg=ibmcloud.Terraform.parse_stderr(result['stderr']), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
