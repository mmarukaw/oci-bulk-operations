import oci
from modules.common import *

identity = oci.identity.IdentityClient
client = oci.file_storage.FileStorageClient

def purge_exports(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['exports']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_exports]
    target.list_args       = [None]
    target.dispname_keys   = ['path']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_export
    target.action_method   = client(config, signer=signer).delete_export
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

def purge_file_systems(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['availability domains', 'file systems']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [identity(config, signer=signer).list_availability_domains, client(config, signer=signer).list_file_systems]
    target.list_args       = [None, None]
    target.dispname_keys   = ['name', 'display_name']
    target.parentid_keys   = [None, None]
    target.get_method      = client(config, signer=signer).get_file_system
    target.action_method   = client(config, signer=signer).delete_file_system
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic_parent, filter_logic_child]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_mount_targets(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['availability domains', 'mount targets']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [identity(config, signer=signer).list_availability_domains, client(config, signer=signer).list_mount_targets]
    target.list_args       = [None, None]
    target.dispname_keys   = ['name', 'display_name']
    target.parentid_keys   = [None, None]
    target.get_method      = client(config, signer=signer).get_mount_target
    target.action_method   = client(config, signer=signer).delete_mount_target
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic_parent, filter_logic_child]
    target_resources = target.list(compartments)
    #target.commit_action(target_resources)
    #target.wait_completion(target_resources)

def purge_snapshots(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['availability domains', 'file systems', 'snapshots']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [identity(config, signer=signer).list_availability_domains, 
                              client(config, signer=signer).list_file_systems, 
                              client(config, signer=signer).list_snapshots
                             ]
    target.list_args       = [None, None, None]
    target.dispname_keys   = ['name', 'display_name', 'id']
    target.parentid_keys   = [None, None, 'file_system_id']
    target.get_method      = client(config, signer=signer).get_snapshot
    target.action_method   = client(config, signer=signer).delete_snapshot
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        return True

    def filter_logic_grandchild(resource):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic_parent, filter_logic_child, filter_logic_grandchild]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)
