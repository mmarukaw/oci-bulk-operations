import oci
from modules.common import *

client = oci.healthchecks.HealthChecksClient

def purge_http_monitors(config, signer, compartments, region_name):
    target = TargetResources()
    target.resource_names  = ['healthcheck http monitors']
    target.action          = 'DELETE'
    target.list_methods    = [client(config, signer=signer).list_http_monitors]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_http_monitor
    target.action_method   = client(config, signer=signer).delete_http_monitor
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.home_region == region_name):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_ping_monitors(config, signer, compartments, region_name):
    target = TargetResources()
    target.resource_names  = ['healthcheck ping monitors']
    target.action          = 'DELETE'
    target.list_methods    = [client(config, signer=signer).list_ping_monitors]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_ping_monitor
    target.action_method   = client(config, signer=signer).delete_ping_monitor
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.home_region == region_name):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)
