'''
Created on 20 Apr 2020

@author: root
'''
import numpy as np
import pandas as pd
from model.db import DatabaseManager
from configuration import ConfigurationFactory
from contract.functions import PortfolioFunctions, DateFunctions, ContractSpecification

class PortfolioManager:
    
    def __init__(self, portfolio_name=None, params_portfolio=None):
        self._init_model(portfolio_name)
        self._init_model(params_portfolio)
        
        #Apply portfolio params here
        self.apply_portfolio_params("tuco")
        self.apply_portfolio_params("arc")
        
        #merge portfolios together
        self.merge_portfolio(merged_portfolio_name="pinnacle", portfolio_a="tuco", portfolio_b="arc")
        
        #display live risk
        self.create_live_risk(live_risk_name="live_risk", portfolio_name="pinnacle")
    
    def _init_model(self, portfolio_name):
        db_config = ConfigurationFactory.create_config("db", portfolio_name)
        db = DatabaseManager(db_config)
        portfolio_df = db.execute_query(portfolio_name)
        setattr(self, portfolio_name, portfolio_df)
    
    
    def add_data_param(self, portfolio_name, param, function, args=None):
        if args is None:
            getattr(self, portfolio_name)[param] = getattr(self, portfolio_name).apply(lambda x: function(x), axis=1)
            #note that getattr(self, portfolio_name) === self.portfolio_name as the object     
        else:
            getattr(self, portfolio_name)[param] = getattr(self, portfolio_name).apply(function, args=args, axis=1)

    def apply_portfolio_params(self, portfolio_name):
        #change series of ExpirationDate to datetime series
        getattr(self, portfolio_name)['ExpirationDate'] = PortfolioFunctions.apply_datetime(getattr(self, portfolio_name), "ExpirationDate")
        self.add_data_param(portfolio_name, "month_code", DateFunctions.add_month_code)
        self.add_data_param(portfolio_name, "expiry_year", DateFunctions.get_year_expiry)
        self.add_data_param(portfolio_name, "pcc", ContractSpecification.add_contract_spec)

        #add underlying future data here
        self.add_data_param(portfolio_name, "underlying_contract_id", ContractSpecification.add_underlying_contract_spec)
        self.add_data_param(portfolio_name, "underlying_product", ContractSpecification.add_product)
        self.add_data_param(portfolio_name, "underlying_future_month", DateFunctions.add_underlying_future_month_code)
        self.add_data_param(portfolio_name, "underlying_future_expiry_year", ContractSpecification.add_underling_future_expiry_year)
        self.add_data_param(portfolio_name, "underlying_future_id", ContractSpecification.add_underlying_future_spec)
        
        #add contract id here
        self.add_data_param(portfolio_name, "contract_id", ContractSpecification.add_contract_name)
        
        #generate quarterly expiry tags here - add arbitary date in the future to generate labels up to that date
        self.add_data_param(portfolio_name, "future_mm", DateFunctions.add_underlying_future_month)
        self.add_data_param(portfolio_name, "underlying_future_mmyy", ContractSpecification.add_underlying_future_mmyy)
        self.add_data_param(portfolio_name, "expiry_id", ContractSpecification.add_fut_expiries)
        
    def merge_portfolio(self, merged_portfolio_name=None, portfolio_a=None, portfolio_b=None):
        tmp = pd.merge(getattr(self, portfolio_a), getattr(self, portfolio_b)[["Delta", "Gamma", "Theta", "Vega", "Theo", "Multiplier", "ActualVolatility", "contract_id"]],
                       on=["contract_id"], how="left")
        tmp = tmp.drop_duplicates()
        setattr(self, merged_portfolio_name, tmp)
    
    def create_live_risk(self, live_risk_name=None, portfolio_name=None):
        tmp = getattr(self, portfolio_name)

        #sterling portfolio
        sterling_tmp = tmp[tmp["underlying_product"] == "sterling"]
        sterling_tmp["nDelta"] = sterling_tmp["Delta"] * sterling_tmp["Position"]
        sterling_tmp["nGamma"] = sterling_tmp["Gamma"] * sterling_tmp["Position"]
        sterling_tmp["nTheta"] = sterling_tmp["Theta"] * sterling_tmp["Position"] * 1000
        sterling_tmp["nVega"] = sterling_tmp["Vega"] * sterling_tmp["Position"] * 10
        sterling_tmp["spread"] = sterling_tmp.apply(lambda x: PortfolioFunctions.compute_spread_to_exchange(x), axis=1)

        ##sterling pivot table
        sterling_tbl = pd.pivot_table(sterling_tmp, values=["nDelta", "nGamma", "nTheta", "nVega", "spread"], index=["expiry_id", "underlying_future_id"],
                                      aggfunc=np.sum, fill_value=0)
        #add the totals row
        stl_res = sterling_tbl.pivot_table(index=['expiry_id', 'underlying_future_id'], margins=True, margins_name='Total', aggfunc=sum)
        stl_res = stl_res.round(0)
        
        #euribor portfolio
        euribor_tmp = tmp[tmp["underlying_product"] == "euribor"]
        euribor_tmp["nDelta"] = euribor_tmp["Delta"] * euribor_tmp["Position"]
        euribor_tmp["nGamma"] = euribor_tmp["Gamma"] * euribor_tmp["Position"]
        euribor_tmp["nTheta"] = euribor_tmp["Theta"] * euribor_tmp["Position"] * 1000
        euribor_tmp["nVega"] = euribor_tmp["Vega"] * euribor_tmp["Position"] * 10
        euribor_tmp["spread"] = euribor_tmp.apply(lambda x: PortfolioFunctions.compute_spread_to_exchange(x), axis=1)

        ##euribor pivot table
        ebor_tbl = pd.pivot_table(euribor_tmp, values=["nDelta", "nGamma", "nTheta", "nVega", "spread"], index=["expiry_id", "underlying_future_id"],
                                      aggfunc=np.sum, fill_value=0)
        #add the totals row
        ebor_res = ebor_tbl.pivot_table(index=['expiry_id', 'underlying_future_id'], margins=True, margins_name='Total', aggfunc=sum)
        ebor_res = ebor_res.round(0)
        #temp append pivot to see what output looks like
        setattr(self, "{}_{}".format(live_risk_name, "sterling"), stl_res)
        setattr(self, "{}_{}".format(live_risk_name, "euribor"), ebor_res)
  


