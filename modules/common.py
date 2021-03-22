import oci
import time
import copy
import itertools
import inspect
from inspect import signature

check_interval = 10
timeout        = 18000000

class TargetResources:
    def __init__(self):
        self.resource_names  = []
        self.action          = ''
        self.target_state    = ''
        self.state_in_action = ''
        self.list_methods    = []
        self.list_args       = [{}]
        self.dispname_keys   = []
        self.parentid_keys   = []
        self.get_method      = ''
        self.action_method   = ''
        self.action_args     = {}

    def list(self, compartments):
        all_targets =[compartments]
        for i, (resname, method, args, dnamekey, pidkey, flogic) \
                in enumerate(zip(self.resource_names,
                                 self.list_methods,
                                 self.list_args,
                                 self.dispname_keys,
                                 self.parentid_keys,
                                 self.filter_logics)):
            #print("---------------------")
            #print("resource loop count {}".format(i))
            #print("resource name {}".format(resname))
            #print(all_targets[i])

            if i == len(self.resource_names) - 1:
                print("\nListing all {}... (* is marked for {})".format(resname, self.action))
            targets = []
            for parent in all_targets[i]:
                kwargs = {}
                #print("--parent--")
                #print(parent)
                if i == 0:
                    kwargs['compartment_id'] = parent.id
                else:
                    # もし呼び出すメソッドのパラメータに compartment_id が存在すれば、親リソースの compartment_id をセットする
                    if signature(method).parameters.get('compartment_id'):
                        kwargs['compartment_id'] = parent.compartment_id

                    # もし呼び出すメソッドのパラメータに availability_domain が存在すれば、親リソースの name をセットする
                    if signature(method).parameters.get('availability_domain'):
                        kwargs['availability_domain'] = parent.name

                    # もし呼び出すメソッドに pidkey と一致するパラメータが存在すれば、親リソースの id または name をセットする
                    if signature(method).parameters.get(pidkey):
                        if hasattr(parent, 'id'):
                            kwargs[pidkey] = getattr(parent, 'id')
                        elif hasattr(parent, 'name'):
                            kwargs[pidkey] = getattr(parent, 'name')
                        else:
                            print("no id nor name attribute found in target")
                
                if args is not None: kwargs.update(args)
                #print("--kwargs--")
                #print(kwargs)

                for listed_resource in list_resources(method, **kwargs):
                    for k, v in kwargs.items():
                        setattr(listed_resource, k, v)

                    msg = "    found " + getattr(listed_resource, dnamekey)

                    if flogic(listed_resource):
                        targets.append(listed_resource)
                        msg = msg + "(*)"

                    if hasattr(parent, 'name'):
                        msg = msg + " in " + parent.name

                    if hasattr(listed_resource, 'lifecycle_state'):
                        msg = msg + " (Status: " + listed_resource.lifecycle_state + ")"

                    if i == len(self.resource_names) - 1:
                        print(msg)

            #print("--targets--")
            #print(targets)

            all_targets.append(targets)
        return all_targets[-1]

    def is_nightlystop_tagged(self, resource):
        go = False
        if ('control' in resource.defined_tags) and ('nightly_stop' in resource.defined_tags['control']):
            if (resource.defined_tags['control']['nightly_stop'].upper() != 'FALSE'):
                go = True
        else:
            go = True
        return go

    def commit_action(self, target_resources):
        if len(target_resources) != 0:
            print('\nCommitting {} action for * marked {}...'.format(self.action, self.resource_names[-1]))
        else:
            print('No marked {}. Skipping.'.format(self.resource_names[-1]))
        count = 0
        action_list = copy.copy(target_resources)
        while len(action_list) > 0:
            for i, resource in enumerate(action_list):
                try:
                    resource_action(self.action_method, resource, **self.action_args)
                except oci.exceptions.ServiceError as e:
                    if e.status == 429:
                        print("--->Info - Status 429 has returned.  The API seems to be throttled.  Will wait 60 seconds then retry...")
                        time.sleep(60)
                        pass
                    else:
                        print("--->ERROR - Action failed: {}".format(e))
                        action_list.pop(i)
                        pass
                else:
                    print('    acting on {}... done.'.format(getattr(resource, self.dispname_keys[-1])))
                    action_list.pop(i)
            count += 1
            if (count * check_interval) > timeout:
                print("--->ERROR - Timed out.")
                break

    def wait_completion(self, target_resources):
        if len(target_resources) != 0:
            print('\nWaiting for {} actions to complete...'.format(self.action))
        count = 0
        while len(target_resources) > 0:
            for i, resource in enumerate(target_resources):
                try:
                    target = get_resource(self.get_method, resource.id)
                except oci.exceptions.ServiceError as e:
                    if e.status == 404:
                        print("    Target resource not found. Probably already deleted: {}".format(getattr(resource, self.dispname_keys[-1])))
                        target_resources.pop(i)
                        pass
                    else:
                        print("--->ERROR - Action failed: {}".format(e))
                        target_resources.pop(i)
                        pass
                else:
                    if target.lifecycle_state == self.target_state:
                        target_resources.pop(i)
                        print("    Completed: {} ({})".format(getattr(resource, self.dispname_keys[-1]), target.lifecycle_state))
                    elif target.lifecycle_state == self.state_in_action:
                        if (count * check_interval) > timeout:
                            target_resources.pop(i)
                            print("--->ERROR - Timed out: {} ({})".format(getattr(resource, self.dispname_keys[-1]), target.lifecycle_state))
                    else:
                        target_resources.pop(i)
                        print("--->ERROR - Conflicted state: {} ({})".format(getattr(resource, self.dispname_keys[-1]), target.lifecycle_state))
            count += 1
            time.sleep(check_interval)

def list_resources(method, **kwargs):
    response = oci.pagination.list_call_get_all_results(
        method,
        **kwargs
    )
    if method.__name__ == "list_objects":
        return getattr(response.data, 'objects')
    else:
        return response.data

def get_resource(method, resource_id, **kwargs):
    response = method(resource_id, **kwargs)
    return response.data

def resource_action(method, resource, **kwargs):
    if method.__name__ == "delete_preauthenticated_request":
        response = method(resource.namespace_name, resource.bucket_name, resource.id, **kwargs)
    elif method.__name__ == "abort_multipart_upload":
        response = method(resource.namespace_name, resource.bucket_name, resource.object, resource.upload_id, **kwargs)
    elif method.__name__ == "delete_object":
        if hasattr(resource, 'version_id'):
            kwargs['version_id'] = resource.version_id
        response = method(resource.namespace_name, resource.bucket_name, resource.name, **kwargs)
    elif method.__name__ == "delete_bucket":
        response = method(resource.namespace_name, resource.name, **kwargs)
    elif method.__name__ == "delete_topic":
        response = method(resource.topic_id, **kwargs)
    elif hasattr(resource, 'id'):
        response = method(resource.id, **kwargs)
    else:
        print("ERROR : No id specified for action")
    return response.data

