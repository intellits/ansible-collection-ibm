
ibm_cdn -- Configure IBM Cloud 'ibm_cdn' resource
=================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, update or destroy an IBM Cloud 'ibm_cdn' resource

This module does not support idempotency



Requirements
------------
The below requirements are needed on the host that executes this module.

- IBM-Cloud terraform-provider-ibm v1.13.1
- Terraform v0.12.20



Parameters
----------

  https_port (False, int, 443)
    HTTPS port number


  respect_headers (False, bool, True)
    respect headers info


  file_extension (False, str, None)
    File extension info


  origin_address (True, str, None)
    (Required for new resource) origin address info


  bucket_name (False, str, None)
    Bucket name


  header (False, str, None)
    Header info


  certificate_type (False, str, None)
    Certificate type


  cache_key_query_rule (False, str, include-all)
    query rule info


  performance_configuration (False, str, General web delivery)
    performance configuration info


  host_name (True, str, None)
    (Required for new resource) Host name


  cname (False, str, None)
    cname info


  vendor_name (False, str, akamai)
    Vendor name


  protocol (False, str, HTTP)
    Protocol name


  http_port (False, int, 80)
    HTTP port number


  path (False, str, /*)
    Path details


  origin_type (False, str, HOST_SERVER)
    Origin type info


  id (False, str, None)
    (Required when updating or destroying existing resource) IBM Cloud Resource ID.


  state (False, any, available)
    State of resource


  iaas_classic_username (False, any, None)
    (Required when generation = 1) The IBM Cloud Classic Infrastructure (SoftLayer) user name. This can also be provided via the environment variable 'IAAS_CLASSIC_USERNAME'.


  iaas_classic_api_key (False, any, None)
    (Required when generation = 1) The IBM Cloud Classic Infrastructure API key. This can also be provided via the environment variable 'IAAS_CLASSIC_API_KEY'.


  region (False, any, us-south)
    The IBM Cloud region where you want to create your resources. If this value is not specified, us-south is used by default. This can also be provided via the environment variable 'IC_REGION'.


  ibmcloud_api_key (True, any, None)
    The IBM Cloud API key to authenticate with the IBM Cloud platform. This can also be provided via the environment variable 'IC_API_KEY'.













Authors
~~~~~~~

- Jay Carman (@jaywcarman)

