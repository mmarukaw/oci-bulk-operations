# coding: utf-8
import sys, os, argparse, configparser, json
import oci, utils
from modules import *

### Read arguments ###
parser = argparse.ArgumentParser()
parser.add_argument("-p",
                    "--profile",
                    default="DEFAULT",
                    help="profile name in settings.ini file. Default: DEFAULT")
args = parser.parse_args()
profile = args.profile

### Load parameters from settings.ini file ###
basedir = os.path.dirname(os.path.abspath(__file__))
ini_file_path = os.path.join(basedir, 'settings.ini')

if not os.path.exists(ini_file_path):
    #logger.error('設定ファイルがありません')
    print("settings.ini file does not exist")
    exit(-1)

inifile = configparser.SafeConfigParser()
inifile.read(ini_file_path, encoding='utf-8')

if not inifile.has_section(profile):
    print('could not find profile {0} in settings.ini file'.format(profile))
    exit(-1)

### Load profile from OCI CLI config file ###
oci_config_file = inifile.get(profile, 'oci_config_file', fallback='~/.oci/config')
oci_profile = inifile.get(profile, 'oci_profile', fallback='DEFAULT')
use_instance_principal = inifile.getboolean(profile, 'use_instance_principal', fallback=False)
target_compartment_ids = json.loads(inifile.get(profile, 'target_compartment_ids', fallback='[]'))
excluded_compartment_names = json.loads(inifile.get(profile, 'excluded_compartment_names', fallback='[]'))
target_region_names = json.loads(inifile.get(profile, 'target_region_names', fallback='[]'))

config = oci.config.from_file(oci_config_file, oci_profile)
signer = utils.oci.init_signer(config, use_instance_principal)

print ("\n===========================[ Login check ]=============================")
user = utils.oci.try_login(config, signer)
print("Logged in as: {} @ {}".format(user.description, config['region']))

print ("\n==========================[ Target regions ]===========================")
regions, home_region = utils.oci.list_target_regions(config, signer, target_region_names)
for region in regions: print(region.region_name)
print("Home region: {}".format(home_region))

print ("\n========================[ Target compartments ]========================")
compartments = utils.oci.list_target_compartments(config, signer, target_compartment_ids, excluded_compartment_names)
for compartment in compartments: print(compartment.name)

for region in regions:
    print ("\n============[ {} ]================".format(region.region_name))

    config["region"] = region.region_name

    ###Database###
    database.purge_autonomous_dbs(config, signer, compartments)
    database.purge_db_systems(config, signer, compartments)

    ###Load Balancer###
    load_balancer.purge_load_balancers(config, signer, compartments)

    ###Compute & Compute Operation###
    auto_scaling.purge_auto_scaling_configurations(config, signer, compartments)
    compute_management.purge_instance_pools(config, signer, compartments)
    compute_management.purge_instance_configurations(config, signer, compartments)
    compute.purge_compute_instances(config, signer, compartments)
    compute.purge_dedicated_vm_hosts(config, signer, compartments)
    compute.purge_images(config, signer, compartments)

    ###Block Volume###
    blockstorage.purge_volume_group_backups(config, signer, compartments)
    blockstorage.purge_volume_groups(config, signer, compartments)
    blockstorage.purge_volume_backup_policies(config, signer, compartments)
    blockstorage.purge_volume_backups(config, signer, compartments)
    blockstorage.purge_volumes(config, signer, compartments)
    blockstorage.purge_boot_volume_backups(config, signer, compartments)
    ##blockstorage.purge_boot_volumes(config, signer, compartments) #AD Required

    ###File Storage###
    file_storage.purge_exports(config, signer, compartments)
    file_storage.purge_snapshots(config, signer, compartments)
    file_storage.purge_file_systems(config, signer, compartments) #AD Required
    file_storage.purge_mount_targets(config, signer, compartments) #AD Required

    ###Object Storage###
    object_storage.purge_preauthenticated_requests(config, signer, compartments)
    object_storage.purge_multipart_uploads(config, signer, compartments)
    object_storage.purge_objects(config, signer, compartments)
    object_storage.purge_buckets(config, signer, compartments)

    ###Virtual Network###
    virtual_network.purge_subnets(config, signer, compartments)
    virtual_network.clear_route_rules(config, signer, compartments)
    virtual_network.purge_route_tables(config, signer, compartments)
    virtual_network.purge_drg_attachments(config, signer, compartments)
    virtual_network.purge_local_peering_gateways(config, signer, compartments)
    virtual_network.purge_internet_gateways(config, signer, compartments)
    virtual_network.purge_nat_gateways(config, signer, compartments)
    virtual_network.purge_service_gateways(config, signer, compartments)
    virtual_network.purge_network_security_groups(config, signer, compartments)
    virtual_network.purge_security_lists(config, signer, compartments)
    virtual_network.purge_dhcp_options(config, signer, compartments)
    #virtual_network.purge_ipv6s(config, signer, compartments)
    #virtual_network.purge_vlans(config, signer, compartments)
    virtual_network.purge_vcns(config, signer, compartments)
    virtual_network.purge_remote_peering_connections(config, signer, compartments)
    virtual_network.purge_ip_sec_connections(config, signer, compartments)
    #virtual_network.purge_cross_connects(config, signer, compartments)
    #virtual_network.purge_cross_connect_groups(config, signer, compartments)
    #virtual_network.purge_virtual_circuits(config, signer, compartments)
    virtual_network.purge_drgs(config, signer, compartments)
    virtual_network.purge_cpes(config, signer, compartments)
    virtual_network.purge_public_ips(config, signer, compartments)

    if region.region_name == home_region:

        ###Web Application Firewall###
        waas.purge_address_lists(config, signer, compartments)
        waas.purge_certificates(config, signer, compartments)
        waas.purge_custom_protection_rules(config, signer, compartments)
        waas.purge_waas_policies(config, signer, compartments)

        ###IAM###
        identity.purge_policies(config, signer, compartments)
        identity.purge_compartments(config, signer, compartments)

print ("\n========================[ Completed ]========================")
