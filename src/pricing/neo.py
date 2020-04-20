'''
Created on 20 Apr 2020

@author: root
'''

from math import exp, sqrt, log, pi
from scipy.stats import norm


class Plain:
    
    @staticmethod
    def black_d_1(forward=None, strike=None, vol=None, time=None, rate=None):
        return (log(forward / strike) + (-rate + (vol **2 / 2) * time)) / (vol * sqrt(time))
    
    @staticmethod
    def black_d_2(d_1=None, vol=None, time=None):
        return d_1 - (vol * sqrt(time))
    
    @staticmethod
    def black_price(opt_type=None, time=None, rate=None, vol=None, forward=None, strike=None, b_yield=None):
        
        if time <= 0:
            return 0
        
        if b_yield is None:
            b_yield = 0
            
        if vol <= 0:
            if opt_type == "C":
                return max(0, (forward - strike) * exp(-rate * time))
            elif opt_type == "P":
                return max(0, (strike - forward) * exp(-rate * time))
            
            else:
                return "N/A - unsupported option type"
        
        d_1 = Plain.black_d_1(forward=forward, strike=strike, vol=vol, time=time, rate=b_yield)
        d_2 = Plain.black_d_2(d_1, vol=vol, time=time)
        
        if opt_type == "C":
            res =  exp(-rate * time) * (forward * norm.cdf(d_1) * exp(-b_yield * time) - strike * norm.cdf(d_2))
        elif opt_type == "P":
            res = exp(-rate * time) * (-forward * norm.cdf(-d_1) * exp(-b_yield * time) + strike * norm.cdf(-d_2))
        else:
            return 0
        
        return res
    
    @staticmethod
    def invert_black_delta_get_strike(delta=None, opt_type=None, forward=None, time=None, vol=None, rate=None, b_yield=None):
        
        if time <= 0:
            return 0
        
        if rate is None:
            rate = 0
        if b_yield is None:
            b_yield = 0
            
        nd_1 = delta / exp((b_yield - rate) * time)
        
        if nd_1 == 0:
            if opt_type == "P":
                nd_1 = -0.001
            else:
                nd_1 = 0.001
                
        if opt_type == "C":
            d_1 = norm.ppf(nd_1)
            res = forward * exp(vol**2 * time / 2  - d_1 * vol * sqrt(time))
        elif opt_type == "P":
            d_1 = norm.ppf(norm.cdf(nd_1 + 1)) #norm.ppf(norm.cdf)) inverse cumulative distribution
            res =forward * exp(vol**2 * time / 2  - d_1 * vol * sqrt(time))
        else:
            res =  0
        
        return res
    
    @staticmethod
    def black_vega(forward=None, strike=None, time=None, vol=None, rate=None, b_yield=None):
        
        if time <= 0:
            return 0
        
        if b_yield is None:
            b_yield = 0
        
        if rate is None:
            rate = 0
        
        d_1 = Plain.black_d_1(forward, strike, vol, time, rate)
        
        return forward * exp((b_yield - rate) * time) * norm.pdf(d_1) * sqrt(time)

    @staticmethod
    def black_volga(forward=None, strike=None, time=None, vol=None, rate=None, b_yield=None):
        
        if time <= 0:
            return 0
        
        if b_yield is None:
            b_yield = 0
        
        if rate is None:
            rate = 0
        
        d_1 = Plain.black_d_1(forward, strike, vol, time, rate)
        d_2 = Plain.black_d_2(d_1, vol, time)
        
        vega = Plain.black_vega(forward=forward, strike=strike, time=time, vol=vol, rate=None, b_yield=None)
        return vega * ((d_1 * d_2) / (forward * vol))

    @staticmethod
    def black_vanna(forward=None, strike=None, time=None, vol=None, rate=None, b_yield=None):
        
        if time <= 0:
            return 0
        
        if b_yield is None:
            b_yield = 0
        
        if rate is None:
            rate = 0
        
        d_1 = Plain.black_d_1(forward, strike, vol, time, rate)
        d_2 = Plain.black_d_2(d_1, vol, time)
        vega = Plain.black_vega(forward=forward, strike=strike, time=time, vol=vol, rate=None, b_yield=None)
        
        return -vega * (d_2 / (vol * forward * sqrt(time))) 

    @staticmethod
    def black_gamma(rate=None, strike=None, forward=None, time=None, vol=None):
        
        d_1 = Plain.black_d_1(forward=forward, strike=strike, vol=vol, time=time, rate=rate)
        scaled = exp(-rate * time) / (forward * vol * sqrt(time))
        delta = (1 / sqrt(2 * pi)) * exp(-(d_1**2)/2)
        return scaled * delta

    
class NEO:
    
    @staticmethod
    def compute(name=None, params=None):
        #get attr and run the pricing here
        pass
    
    @staticmethod
    def price(df_r):
        
        pass