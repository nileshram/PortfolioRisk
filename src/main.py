'''
Created on 20 Apr 2020

@author: root
'''

import os
import json
import logging.config

from model.data import PortfolioManager
import pandas as pd

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
        
        #write to excel
        writer = pd.ExcelWriter(os.path.dirname(__file__), engine = 'xlsxwriter')
        p.live_risk_sterling.to_excel("sterling.xlsx")
        p.live_risk_euribor.to_excel("euribor.xlsx")
    except Exception as e:
        print(e)