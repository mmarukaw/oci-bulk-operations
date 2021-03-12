import oci
from modules.common import *

client = oci.core.ComputeManagementClient

def purge_instance_pools(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['instance pools']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_instance_pools]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_instance_pool
    target.action_method   = client(config, signer=signer).terminate_instance_pool
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.lifecycle_state not in ['TERMINATING', 'TERMINATED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)


def purge_instance_configurations(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['instance configurations']
    target.is_statefuls    = [False]
    target.action          = 'DELETE'
    #target.target_state    = None
    #target.state_in_action = None
    target.list_methods    = [client(config, signer=signer).list_instance_configurations]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_instance_configuration
    target.action_method   = client(config, signer=signer).delete_instance_configuration
    target.action_args     = {}

    def filter_logic(resource):
        return True

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)

