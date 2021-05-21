import oci
from modules.common import *

client = oci.streaming.StreamAdminClient

def purge_streams(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['streams']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_streams]
    target.list_args       = [None]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_stream
    target.action_method   = client(config, signer=signer).delete_stream
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

def purge_stream_pools(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['stream pools']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_stream_pools]
    target.list_args       = [None]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_stream_pool
    target.action_method   = client(config, signer=signer).delete_stream_pool
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
