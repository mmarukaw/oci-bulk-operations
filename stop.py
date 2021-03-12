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

### Set setting.ini file path ###
basedir = os.path.dirname(os.path.abspath(__file__))
ini_file_path = os.path.join(basedir, 'settings.ini')

### Load parameters from settings.ini file ###
if not os.path.exists(ini_file_path):
    #logger.error('設定ファイルがありません')
    print("settings.ini file does not exist")
    exit(-1)

inifile = configparser.SafeConfigParser()
inifile.read(ini_file_path, encoding='utf-8')

if not inifile.has_section(profile):
    print('could not find profile {0} in settings.ini file'.format(profile))
    exit(-1)

oci_config_file = inifile.get(profile, 'oci_config_file', fallback='~/.oci/config')
oci_profile = inifile.get(profile, 'oci_profile', fallback='DEFAULT')
use_instance_principal = inifile.getboolean(profile, 'use_instance_principal', fallback=False)
target_compartment_ids = json.loads(inifile.get(profile, 'target_compartment_ids', fallback='[]'))
excluded_compartment_names = json.loads(inifile.get(profile, 'excluded_compartment_names', fallback='[]'))
target_region_names = json.loads(inifile.get(profile, 'target_region_names', fallback='[]'))

### Load OCICLI config file and profile ###
config = oci.config.from_file(oci_config_file, oci_profile)
signer = utils.oci.init_signer(config, use_instance_principal)

print ("\n===========================[ Login check ]=============================")
user = utils.oci.try_login(config, signer)
print("Logged in as: {} @ {}".format(user.description, config['region']))

print ("\n==========================[ Target regions ]===========================")
regions = utils.oci.list_target_regions(config, signer, target_region_names)
for region in regions: print(region.region_name)

print ("\n========================[ Target compartments ]========================")
compartments = utils.oci.list_target_compartments(config, signer, target_compartment_ids, excluded_compartment_names)
for compartment in compartments: print(compartment.name)

for region in regions:
    print ("\n============[ {} ]================".format(region.region_name))

    config["region"] = region.region_name

    database.change_autonomous_db_licenses(config, signer, compartments)
    compute.stop_compute_instances(config, signer, compartments)
    database.stop_db_systems(config, signer, compartments)
    database.stop_autonomous_dbs(config, signer, compartments)

print ("\n========================[ Completed ]========================")
