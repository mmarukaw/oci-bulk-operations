import oci
from modules.common import *

cpclient = oci.ons.NotificationControlPlaneClient
dpclient = oci.ons.NotificationDataPlaneClient

def purge_topics(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['topics']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [cpclient(config, signer=signer).list_topics]
    target.list_args       = [None]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    target.get_method      = cpclient(config, signer=signer).get_topic
    target.action_method   = cpclient(config, signer=signer).delete_topic
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)

def purge_subscriptions(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['subscriptions']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [dpclient(config, signer=signer).list_subscriptions]
    target.list_args       = [None]
    target.dispname_keys   = ['endpoint']
    target.parentid_keys   = [None]
    target.get_method      = dpclient(config, signer=signer).get_subscription
    target.action_method   = dpclient(config, signer=signer).delete_subscription
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
