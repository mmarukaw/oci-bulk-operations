import oci
from modules.common import *

client = oci.core.BlockstorageClient

def purge_boot_volumes(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['boot volumes']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_boot_volumes]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_boot_volume
    target.action_method   = client(config, signer=signer).delete_boot_volume
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

def purge_boot_volume_backups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['boot volume backups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_boot_volume_backups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_boot_volume_backup
    target.action_method   = client(config, signer=signer).delete_boot_volume_backup
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

def purge_volumes(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['block volumes']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_volumes]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_volume
    target.action_method   = client(config, signer=signer).delete_volume
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

def purge_volume_backups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['block volume backups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_volume_backups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_volume_backup
    target.action_method   = client(config, signer=signer).delete_volume_backup
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

def purge_volume_backup_policies(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['block volume backup policies']
    target.action          = 'TERMINATE'
    #target.target_state    = 'TERMINATED'
    #target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_volume_backup_policies]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    #target.get_method      = client(config, signer=signer).get_volume_backup_policy
    target.action_method   = client(config, signer=signer).delete_volume_backup_policy
    target.action_args     = {}

    def filter_logic(resource):
        return True

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)

def purge_volume_groups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['block volume groups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_volume_groups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_volume_group
    target.action_method   = client(config, signer=signer).delete_volume_group
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

def purge_volume_group_backups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['block volume group backups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_volume_group_backups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_volume_group_backup
    target.action_method   = client(config, signer=signer).delete_volume_group_backup
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

