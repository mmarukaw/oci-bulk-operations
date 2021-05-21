import oci
from modules.common import *

client = oci.logging.LoggingManagementClient

def purge_log_groups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['log groups']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_log_groups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_log_group
    target.action_method   = client(config, signer=signer).delete_log_group
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

