import oci

identity = oci.identity.IdentityClient

def init_signer(config, use_instance_principal):
    if use_instance_principal == 'TRUE':
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    else:
        signer = oci.signer.Signer(
            tenancy = config['tenancy'],
            user = config['user'],
            fingerprint = config['fingerprint'],
            private_key_file_location = config['key_file'],
            pass_phrase = config['pass_phrase']
        )
    return signer


def try_login(config, signer):
    login_user = identity(config, signer=signer).get_user(config['user']).data
    return login_user


def list_target_regions(config, signer, target_region_names):
    all_regions = identity(config, signer=signer).list_region_subscriptions(config['tenancy']).data
    target_regions=[]
    for region in all_regions:
        if (not target_region_names) or (region.region_name in target_region_names):
            target_regions.append(region)
        if region.is_home_region:
            home_region = region.region_name
    return target_regions, home_region


def get_home_region(config, signer):
    regions = identity(config, signer=signer).list_region_subscriptions(config['tenancy']).data
    for region in regions:
        if (not target_region_names) or (region.region_name in target_region_names):
            target_regions.append(region)
    return target_regions


def list_target_compartments(config, signer, top_level_comp_id_list, excluded_comp_list):
    target_compartments = []
    temp_comp_list = []
    if not top_level_comp_id_list: top_level_comp_id_list = [config['tenancy']]

    for top_level_comp_id in top_level_comp_id_list:
        top_level_compartment = identity(config, signer=signer).get_compartment(top_level_comp_id).data
        temp_comp_list.append(top_level_compartment)
        target_compartments.append(top_level_compartment)

    while len(temp_comp_list) > 0:
        target = temp_comp_list.pop(0)
        if (target.name not in excluded_comp_list) and (target.lifecycle_state == 'ACTIVE'):
            child_compartments = oci.pagination.list_call_get_all_results(
                identity(config, signer=signer).list_compartments,
                target.id
            ).data
            temp_comp_list.extend(child_compartments)
            target_compartments.extend(child_compartments)
        else:
            target_compartments.remove(target)

    target_compartments.reverse()
    return target_compartments

