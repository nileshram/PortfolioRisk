'''
Created on 20 Apr 2020

@author: root
'''

import os
import json
import logging.config

from model.data import PortfolioManager

def _configure_log():
    logconfjson = os.path.join("conf", "log_config.json")
    if os.path.exists(logconfjson) and os.path.isfile(logconfjson):
        with open(logconfjson, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config["log"])
    else:
        logging.basicConfig(level=logging.INFO)
    
if __name__ == "__main__":
    _configure_log()
    log = logging.getLogger("portfolio_risk")
    log.info("Starting risk application")
    try:
        p = PortfolioManager(portfolio_name="tuco", params_portfolio="arc")
        print(p.tuco.head())
        print(p.arc.head())
    except Exception as e:
        print(e)