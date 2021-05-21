import oci
from modules.common import *

client_gw = oci.apigateway.GatewayClient
client_dp = oci.apigateway.DeploymentClient

def purge_deployments(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['api deployments']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client_dp(config, signer=signer).list_deployments]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client_dp(config, signer=signer).get_deployment
    target.action_method   = client_dp(config, signer=signer).delete_deployment
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

def purge_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['api gateways']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client_gw(config, signer=signer).list_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client_gw(config, signer=signer).get_gateway
    target.action_method   = client_gw(config, signer=signer).delete_gateway
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

