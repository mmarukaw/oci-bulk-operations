import oci
from modules.common import *

client = oci.core.VirtualNetworkClient

def clear_route_rules(config, signer, compartments):
    #details = oci.core.models.UpdateRouteTableDetails()
    #details.route_rules = []
    details = oci.core.models.UpdateRouteTableDetails(route_rules = [])

    target = TargetResources()
    target.resource_names  = ['route rule']
    target.action          = 'CLEAR'
    target.target_state    = 'AVAILABLE'
    target.state_in_action = 'PROVISIONING'
    target.list_methods    = [client(config, signer=signer).list_route_tables]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_route_table
    target.action_method   = client(config, signer=signer).update_route_table
    target.action_args     = {'update_route_table_details' : details}

    def filter_logic(resource):
        if (resource.lifecycle_state not in ['TERMINATING', 'TERMINATED']):
            return True
        else:
            return False

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_vcns(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['VCNs']
    target.is_statefuls    = [True]
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_vcns]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_vcn
    target.action_method   = client(config, signer=signer).delete_vcn
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

def purge_subnets(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['subnets']
    target.is_statefuls    = [True]
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_subnets]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_subnet
    target.action_method   = client(config, signer=signer).delete_subnet
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

def purge_route_tables(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['route tables']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_route_tables]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_route_table
    target.action_method   = client(config, signer=signer).delete_route_table
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

def purge_drg_attachments(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['DRG attachments']
    target.action          = 'DETACH'
    target.target_state    = 'DETACHED'
    target.state_in_action = 'DETACHING'
    target.list_methods    = [client(config, signer=signer).list_drg_attachments]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_drg_attachment
    target.action_method   = client(config, signer=signer).delete_drg_attachment
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

def purge_local_peering_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['local peering gateways']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_local_peering_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_local_peering_gateway
    target.action_method   = client(config, signer=signer).delete_local_peering_gateway
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

def purge_internet_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['internet gateways']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_internet_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_internet_gateway
    target.action_method   = client(config, signer=signer).delete_internet_gateway
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

def purge_nat_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['NAT gateways']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_nat_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_nat_gateway
    target.action_method   = client(config, signer=signer).delete_nat_gateway
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

def purge_local_peering_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['local peering gateways']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_local_peering_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_local_peering_gateway
    target.action_method   = client(config, signer=signer).delete_local_peering_gateway
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

def purge_service_gateways(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['service gateways']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_service_gateways]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_service_gateway
    target.action_method   = client(config, signer=signer).delete_service_gateway
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

def purge_network_security_groups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['network security groups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_network_security_groups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_network_security_group
    target.action_method   = client(config, signer=signer).delete_network_security_group
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

def purge_security_lists(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['security lists']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_security_lists]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_security_list
    target.action_method   = client(config, signer=signer).delete_security_list
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

def purge_dhcp_options(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['dhcp options']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_dhcp_options]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_dhcp_options
    target.action_method   = client(config, signer=signer).delete_dhcp_options
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

def purge_cpes(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['CPEs']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_cpes]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_cpe
    target.action_method   = client(config, signer=signer).delete_cpe
    target.action_args     = {}

    def filter_logic(resource):
        return True

    target.filter_logics   = [filter_logic]
    target_resources = target.list(compartments)
    target.commit_action(target_resources)
    target.wait_completion(target_resources)

def purge_cross_connects(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['cross connects']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_cross_connects]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_cross_connect
    target.action_method   = client(config, signer=signer).delete_cross_connect
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

def purge_cross_connect_groups(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['cross connect groups']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_cross_connect_groups]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_cross_connect_group
    target.action_method   = client(config, signer=signer).delete_cross_connect_group
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

def purge_drgs(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['DRGs']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_drgs]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_drg
    target.action_method   = client(config, signer=signer).delete_drg
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

def purge_ip_sec_connections(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['IPsec connections']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_ip_sec_connections]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_ip_sec_connection
    target.action_method   = client(config, signer=signer).delete_ip_sec_connection
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

def purge_ipv6s(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['IPv6s']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_ipv6s]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_ipv6
    target.action_method   = client(config, signer=signer).delete_ipv6
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

def purge_public_ips(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['public ips']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_public_ips]
    target.list_args       = [{'scope' : 'REGION', 'lifetime' : 'RESERVED'}]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_public_ip
    target.action_method   = client(config, signer=signer).delete_public_ip
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

def purge_remote_peering_connections(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['remote peering connections']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_remote_peering_connections]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_remote_peering_connection
    target.action_method   = client(config, signer=signer).delete_remote_peering_connection
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

def purge_virtual_circuits(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['virtual circuits']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_virtual_circuits]
    target.list_args       = [None]
    target.dispname_keys   = ['display_name']
    target.parentid_keys   = [None]
    target.get_method      = client(config, signer=signer).get_virtual_circuit
    target.action_method   = client(config, signer=signer).delete_virtual_circuit
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

def purge_vlans(config, signer, compartments):
    target = TargetResources()
    target.resource_names  = ['VCNs', 'VLANs']
    target.action          = 'TERMINATE'
    target.target_state    = 'TERMINATED'
    target.state_in_action = 'TERMINATING'
    target.list_methods    = [client(config, signer=signer).list_vcns, client(config, signer=signer).list_vlans]
    target.list_args       = [None, None]
    target.dispname_keys   = ['display_name', 'display_name']
    target.parentid_keys   = [None, 'vcn_id']
    target.get_method      = client(config, signer=signer).get_vlan
    target.action_method   = client(config, signer=signer).delete_vlan
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


