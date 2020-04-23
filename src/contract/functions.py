'''
Created on 20 Apr 2020

@author: root
'''
"""
Copyright : 2018 Atlantic Trading London Ltd. All rights reserved.

Date of Creation : 22 Jul 2019
Author : nish

"""
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

class PortfolioFunctions:
    
    @staticmethod
    def apply_datetime(data, header):
        data[header] = pd.to_datetime(data[header], format="%Y-%m-%d")
        return data[header]
    
class DateFunctions:

    @staticmethod
    def add_month_code(df_r):
        mth = df_r["ExpirationDate"].month
        if mth  == 1:
            return "F"
        elif mth == 2:
            return "G"
        elif mth == 3:
            return "H"
        elif mth == 4:
            return "J"
        elif mth == 5:
            return "K"
        elif mth == 6:
            return "M"
        elif mth == 7:
            return "N"
        elif mth == 8:
            return "Q"
        elif mth == 9:
            return "U"
        elif mth == 10:
            return "V"
        elif mth == 11:
            return "X"
        elif mth == 12:
            return "Z"
    
    @staticmethod
    def add_underlying_future_month_code(df_r):
        mth = df_r["ExpirationDate"].month
        if mth  == 1:
            return "H"
        elif mth == 2:
            return "H"
        elif mth == 3:
            return "H"
        elif mth == 4:
            return "M"
        elif mth == 5:
            return "M"
        elif mth == 6:
            return "M"
        elif mth == 7:
            return "U"
        elif mth == 8:
            return "U"
        elif mth == 9:
            return "U"
        elif mth == 10:
            return "Z"
        elif mth == 11:
            return "Z"
        elif mth == 12:
            return "Z"
        
    @staticmethod
    def get_year_expiry(df_r):
        year = df_r["ExpirationDate"].year
        return str(year)[-2:]

    @staticmethod
    def add_mm_yy(df_r):
        return datetime.datetime.strftime(df_r["ExpirationDate"], "%m-%y")
    
class ContractSpecification:
    
    @staticmethod
    def add_contract_spec(df_r):
        if df_r["Symbol"] == "STERL":
            return "L"
        elif df_r["Symbol"] == "FEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3MC":
            return "K"
        elif df_r["Symbol"] == "OEU3MC2":
            return "K2"
        elif df_r["Symbol"] == "OEU3MC3":
            return "K3"
        elif df_r["Symbol"] == "OSTERL":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC":
            return "M"
        elif df_r["Symbol"] == "OSTERLMC2":
            return "M2"
        elif df_r["Symbol"] == "OSTERLMC3":
            return "M3"
        
    @staticmethod   
    def add_underlying_contract_spec(df_r):
        if df_r["Symbol"] == "STERL":
            return "L"
        elif df_r["Symbol"] == "OSTERL":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC2":
            return "L"
        elif df_r["Symbol"] == "OSTERLMC3":
            return "L"
        elif df_r["Symbol"] == "FEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3":
            return "I"
        elif df_r["Symbol"] == "OEU3MC":
            return "I"
        elif df_r["Symbol"] == "OEU3MC2":
            return "I"
        elif df_r["Symbol"] == "OEU3MC3":
            return "I"

    
    @staticmethod
    def add_contract_name(df_r):
        if df_r["Product"] == "Future":
            contract_year = "".join((df_r["underlying_future_month"], df_r["underlying_future_expiry_year"]))
            contract_name = " ".join((df_r["underlying_contract_id"], contract_year, df_r["Product"]))
            return contract_name
        elif df_r["Product"] == "Option":
            contract_year = "".join((df_r["month_code"], df_r["expiry_year"]))
            contract_kind = "".join((str(df_r["Strike"]), df_r["PutCall"][0]))
            contract_name = " ".join((df_r["pcc"], contract_year, contract_kind))
            return contract_name
    
    @staticmethod
    def add_underling_future_expiry_year(df_r):
        if df_r["pcc"] in ["L", "I"]:
            return datetime.datetime.strftime(df_r["ExpirationDate"], "%y")
        elif df_r["pcc"] in ["M", "K"]:
            return datetime.datetime.strftime(df_r["ExpirationDate"] + relativedelta(years=1),
                                              "%y")
        elif df_r["pcc"] in ["M2", "K2"]:
            return datetime.datetime.strftime(df_r["ExpirationDate"] + relativedelta(years=2),
                                              "%y")
        elif df_r["pcc"] in ["M3", "K3"]:
            return datetime.datetime.strftime(df_r["ExpirationDate"] + relativedelta(years=3),
                                              "%y")
    
    @staticmethod
    def add_underlying_future_spec(df_r):
        pcc = df_r["underlying_contract_id"]
        mth = df_r["underlying_future_month"]
        yy = df_r["underlying_future_expiry_year"]
        return "{} {}{}".format(pcc, mth, yy)
                
    @staticmethod
    def gen_quarterlies(max_date):
        q = (pd.date_range(pd.to_datetime(datetime.datetime.now().date()), 
            pd.to_datetime(max_date) + pd.offsets.QuarterBegin(1), freq='Q')
                           .strftime('%m%y')
                           .tolist())
        fut_code = []
        expiry_index = {v : "".join(("ex",str(k))) for k, v in enumerate(q, start=1)}
        return expiry_index

    @staticmethod
    def add_fut_expiries(df_r):
        fut_month = df_r["underlying_future_month"]
        fut_year = df_r["underlying_future_expiry_year"]
        s = fut_month + fut_year
        exp_index = ContractSpecification.gen_quarterlies("2025-01-01") #arbitary date in future
        return exp_index[df_r["UnderlyingFutureMM-YY"]]
    
    @staticmethod
    def add_product(df_r):
        if df_r["underlying_contract_id"] == "L":
            return "sterling"
        elif df_r["underlying_contract_id"] == "I":
            return "euribor"
    
    @staticmethod
    def add_fut_shock_upper(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["fut"]["up"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_fut_shock_lower(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["fut"]["down"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_vol_shock_upper(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["vol"]["up"][df_r["ExpiryIndex"]]

    @staticmethod
    def add_vol_shock_lower(df_r, config, scenario):
        return config["product"][df_r["ProductName"]]["shocks"]["scenario"][scenario]["vol"]["down"][df_r["ExpiryIndex"]]
    
    @staticmethod
    def add_tick_value(df_r):
        if df_r["ProductName"] == "sterling":
            return 12.5
        elif df_r["ProductName"] == "euribor":
            return 25
    
    @staticmethod
    def add_multiplier(df_r):
        if df_r["Product"] in ["Option", "Future"]:
            return 1000
    
    @staticmethod
    def add_curve_segment(df_r):
        _curve = {"whites" : ["ex1", "ex2", "ex3", "ex4"],
                 "mids" : ["ex5", "ex6", "ex7", "ex8"],
                 "greens" : ["ex9", "ex10", "ex11", "ex12"],
                "blues" : ["ex13", "ex14", "ex15", "ex16"]}
        for segment in _curve:
            if df_r["ExpiryIndex"] in _curve[segment]:
                return segment