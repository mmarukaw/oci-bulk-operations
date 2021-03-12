import oci
from modules.common import *

client = oci.identity.IdentityClient

def purge_compartments(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['compartments']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_compartments]
    target.list_args       = [None]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_compartment
    target.action_method   = client(config, signer=signer).delete_compartment
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

def purge_policies(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['policies']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_policies]
    target.list_args       = [None]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_policy
    target.action_method   = client(config, signer=signer).delete_policy
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

