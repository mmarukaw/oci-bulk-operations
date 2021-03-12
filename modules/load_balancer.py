import oci
from modules.common import *

client = oci.load_balancer.LoadBalancerClient

def purge_load_balancers(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['load balancers']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_load_balancers]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_load_balancer
    target.action_method   = client(config, signer=signer).delete_load_balancer
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

