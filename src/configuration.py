'''
Created on 22 Jul 2019

@author: Nilesh Ramnarain
'''

import json
from os.path import join, dirname
  
class ConfigurationFactory:
      
    @staticmethod
    def create_config(config_type=None, portfolio_name=None):
        proj_dir = dirname(dirname(__file__))
        config = join(proj_dir, "conf", "log_config.json")
        try:
            with open(config, "r") as config:
                config_file = json.load(config)[config_type][portfolio_name]
        except IOError:
            print("Error with config filename/location please check the constant.py file")
        return config_file      

