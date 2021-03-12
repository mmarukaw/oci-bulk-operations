import oci
from modules.common import *

client = oci.waas.WaasClient

def purge_address_lists(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['IP address lists']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_address_lists]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_address_list
    target.action_method   = client(config, signer=signer).delete_address_list
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

def purge_certificates(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['certificates']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_certificates]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_certificate
    target.action_method   = client(config, signer=signer).delete_certificate
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

def purge_custom_protection_rules(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['custom protection rules']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_custom_protection_rules]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_custom_protection_rule
    target.action_method   = client(config, signer=signer).delete_custom_protection_rule
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

def purge_waas_policies(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['waas policies']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_waas_policies]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_waas_policy
    target.action_method   = client(config, signer=signer).delete_waas_policy
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

