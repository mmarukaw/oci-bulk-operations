import oci
from modules.common import *

client = oci.object_storage.ObjectStorageClient

def get_namespace(config, signer):
    response = client(config, signer=signer).get_namespace()
    return response.data

def purge_preauthenticated_requests(config, signer, compartments):
    namespace = get_namespace(config, signer)

    target = TargetResources()
    target.resource_names  = ['buckets', 'preauthenticated requests']
    target.action          = 'DELETE'
    #target.target_state    = 'TERMINATED'
    #target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_buckets, client(config, signer=signer).list_preauthenticated_requests]
    target.list_args       = [{'namespace_name' : namespace}, {'namespace_name' : namespace}]
    target.dispname_keys   = ['name', 'name']
    target.parentid_keys   = [None, 'bucket_name']
    target.get_method      = client(config, signer=signer).get_preauthenticated_request
    target.action_method   = client(config, signer=signer).delete_preauthenticated_request
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        return True

    target.filter_logics   = [filter_logic_parent, filter_logic_child]

    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)


def purge_multipart_uploads(config, signer, compartments):
    namespace = get_namespace(config, signer)

    target = TargetResources()
    target.resource_names  = ['buckets', 'multipart uploads']
    target.action          = 'ABORT'
    #target.target_state    = 'TERMINATED'
    #target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_buckets, client(config, signer=signer).list_multipart_uploads]
    target.list_args       = [{'namespace_name' : namespace}, {'namespace_name' : namespace}]
    target.dispname_keys   = ['name', 'object']
    target.parentid_keys   = [None, 'bucket_name']
    #target.get_method      = client(config, signer=signer).
    target.action_method   = client(config, signer=signer).abort_multipart_upload
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        return True

    target.filter_logics   = [filter_logic_parent, filter_logic_child]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)


def purge_objects(config, signer, compartments):
    namespace = get_namespace(config, signer)

    target = TargetResources()
    target.resource_names  = ['buckets', 'objects and versions']
    target.action          = 'DELETE'
    #target.target_state    = 'TERMINATED'
    #target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_buckets, client(config, signer=signer).list_object_versions]
    target.list_args       = [{'namespace_name' : namespace}, {'namespace_name' : namespace}]
    target.dispname_keys   = ['name', 'name']
    target.parentid_keys   = [None, 'bucket_name']
    #target.get_method      = client(config, signer=signer).get_object
    target.action_method   = client(config, signer=signer).delete_object
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    def filter_logic_child(resource):
        return True

    target.filter_logics   = [filter_logic_parent, filter_logic_child]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)


def purge_buckets(config, signer, compartments):
    namespace = get_namespace(config, signer)

    target = TargetResources()
    target.resource_names  = ['buckets']
    target.action          = 'DELETE'
    #target.target_state    = 'TERMINATED'
    #target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_buckets]
    target.list_args       = [{'namespace_name' : namespace}]
    target.dispname_keys   = ['name']
    target.parentid_keys   = [None]
    #target.get_method      = client(config, signer=signer).get_bucket
    target.action_method   = client(config, signer=signer).delete_bucket
    target.action_args     = {}

    def filter_logic_parent(resource):
        return True

    target.filter_logics   = [filter_logic_parent]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    #target.wait_completion(target_resources)

