import oci
from modules.common import *

client = oci.database.DatabaseClient

def change_autonomous_db_licenses(config, signer, compartments):
    details = oci.database.models.UpdateAutonomousDatabaseDetails(license_model = 'BRING_YOUR_OWN_LICENSE')

    target = TargetResources()
    target.resource_names  = ['autonomous databases']
    target.action          = 'CHANGE_LICENSE_MODEL_TO_BYOL'
    target.target_state    = 'AVAILABLE'
    target.state_in_action = 'UPDATING'
    target.list_methods    = [client(config, signer=signer).list_autonomous_databases]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_autonomous_database
    target.action_method   = client(config, signer=signer).update_autonomous_database
    target.action_args     = {'update_autonomous_database_details' : details}

    def filter_logic(resource):
        if (resource.license_model == 'LICENSE_INCLUDED'):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def stop_autonomous_dbs(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['autonomous databases']
    target.action          = 'STOP'
    target.target_state    = 'STOPPED'
    target.state_in_action = 'STOPPING'
    target.list_methods    = [client(config, signer=signer).list_autonomous_databases]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_autonomous_database
    target.action_method   = client(config, signer=signer).stop_autonomous_database
    target.action_args     = {}

    def filter_logic(resource):
        if (resource.lifecycle_state == 'AVAILABLE') and (target.is_nightlystop_tagged(resource)):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def stop_db_systems(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['database systems', 'database nodes']
    target.action          = 'STOP'
    target.target_state    = 'STOPPED'
    target.state_in_action = 'STOPPING'
    target.list_methods    = [client(config, signer=signer).list_db_systems, client(config, signer=signer).list_db_nodes]
    target.list_args       = [None, None]
    target.dispname_keys   = ['display_name', 'hostname']
    target.parentid_keys   = [None, 'db_system_id']
    target.get_method      = client(config, signer=signer).get_db_node
    target.action_method   = client(config, signer=signer).db_node_action
    target.action_args     = {'action' : 'STOP'}

    def filter_logic_parent(resource):
        if (resource.lifecycle_state == 'AVAILABLE') and (target.is_nightlystop_tagged(resource)):
            return True
        else:
            return False

    def filter_logic_child(resource):
        if (resource.lifecycle_state == 'AVAILABLE'):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic_parent, filter_logic_child]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_autonomous_dbs(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['autonomous databases']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_autonomous_databases]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_autonomous_database
    target.action_method   = client(config, signer=signer).delete_autonomous_database
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

def purge_db_backups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['database backups']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_backups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_backup
    target.action_method   = client(config, signer=signer).delete_backup
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

def purge_db_systems(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['database systems']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_db_systems]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_db_system
    target.action_method   = client(config, signer=signer).terminate_db_system
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

