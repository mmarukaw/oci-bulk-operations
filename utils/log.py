import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ------------

#from utils.logConf import logging
#logger = logging.getLogger(__name__)

# -------------

import configparser

class initConfig:
    def __init__(self, configfile, profile):
        inifile = configparser.ConfigParser()
        if not os.path.exists(configfile):
            #logger.error('設定ファイルがありません')
            print("No setting file exists")
            exit(-1)
        inifile.read(configfile, encoding='utf-8')
        #logging.info('----設定開始----')
        try:
            self.oci_config_file           = inifile.get(profile, 'oci_config_file')
            self.use_instance_principal    = inifile.getboolean(profile, 'use_instance_principal')
            self.top_level_compartment_ids = json.loads(inifile.get(profile, 'top_level_compartment_ids'))
            self.excluded_compartments     = json.loads(inifile.get(profile, 'excluded_compartments'))
            self.target_region_names       = json.loads(inifile.get(profile, 'target_region_names'))

        except Exception as e:
            #logger.critical("config error {0}".format(e))
            print("config error")
