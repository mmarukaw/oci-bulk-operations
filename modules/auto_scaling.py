import oci
from modules.common import *

client = oci.autoscaling.AutoScalingClient

def purge_auto_scaling_configurations(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['autoscaling configurations']
    target.is_statefuls    = [False]
    target.action          = 'DELETE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_auto_scaling_configurations]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_auto_scaling_configuration
    target.action_method   = client(config, signer=signer).delete_auto_scaling_configuration
    target.action_args     = {}

    def filter_logic(resource):
        return True

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

