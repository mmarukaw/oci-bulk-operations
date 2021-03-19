import oci
from modules.common import *

client = oci.core.ComputeClient

def stop_compute_instances(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['compute instances']
    target.action          = 'STOP'
    target.target_state    = 'STOPPED'
    target.state_in_action = 'STOPPING'
    target.list_methods    = [client(config, signer=signer).list_instances]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_instance
    target.action_method   = client(config, signer=signer).instance_action
    target.action_args     = {'action' : 'STOP'}

    def filter_logic(resource):
        if (resource.lifecycle_state == 'RUNNING') and (target.is_nightlystop_tagged(resource)):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_dedicated_vm_hosts(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['dedicated vm hosts']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_dedicated_vm_hosts]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_dedicated_vm_host
    target.action_method   = client(config, signer=signer).delete_dedicated_vm_host
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

def purge_images(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['images']
    target.action          = 'DELETE'
    target.target_state    = 'DELETED'
    target.state_in_action = 'DELETING'
    target.list_methods    = [client(config, signer=signer).list_images]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_image
    target.action_method   = client(config, signer=signer).delete_image
    target.action_args     = {}

    def filter_logic(resource):
        #if (resource.lifecycle_state not in ['DELETING', 'DELETED']):
        if (resource.lifecycle_state not in ['DELETING', 'DELETED']) and \
           not (resource.display_name.startswith(('Windows-Server-',
                                                  'Oracle-Linux-',
                                                  'Oracle-Autonomous-Linux-',
                                                  'CentOS-',
                                                  'Canonical-Ubuntu-'))):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_compute_instances(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['compute instances']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_instances]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_instance
    target.action_method   = client(config, signer=signer).terminate_instance
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

