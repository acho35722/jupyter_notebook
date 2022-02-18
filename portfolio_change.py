# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:10:49 2021

@author: ahram.cho
"""

import sys
import pandas as pd
from pandas import DataFrame
from datetime import date
import numpy as np
import calendar
from datetime import datetime

# =============================================================================
# # 1-4 import SQlite DB
# #variable = returnEngine()
# variable = create_engine('sqlite:///theme_rotation_sample.db', echo=True)
# connection = variable.connect()
# #session = Session(variable)
# 
# # 1. table1 
# table1meta = MetaData(variable)
# table1 = Table('model_portfolio', table1meta, autoload=True)
# DBSession = sessionmaker(bind=variable)
# session = DBSession()
# 
# result1 = session.query(table1)
# model_portfolio = pd.read_sql(result1.statement, result1.session.bind)
# # = screener_data.drop(columns = ['index'])
# result1.all()
# 
# 
# table2 = Table('input_screener_etfpx', table1meta, autoload=True)
# result2 = session.query(table2)
# etfpx = pd.read_sql(result2.statement, result2.session.bind)
# etfpx = etfpx.drop(columns = ['index'])
# etfpx = etfpx.rename(columns = {'TICKER': 'ETF'})
# 
# result1.all()
# connection.close()
# session.close()
# 
# =============================================================================
#____________________________________________________________________________________________________#

# Now we have the model portfolio 
# split the dataframe 

def model_portfolio(sample, red_date, cur_date):
    model_portfolio = sample
    date = model_portfolio['Date'].unique()
    
    mp_present = model_portfolio[model_portfolio['Date'] == date[0]][['테마', 'ETF', '%']]
    mp_past = model_portfolio[model_portfolio['Date'] == date[1]][['테마', 'ETF', '%']]
    
    
    # set dummy input portfolio size = $100,000
    # give the expected proportion to the respective portfolio size for the past and present 
    
    port_size = 100000
    mp_present['size'] = mp_present['%'] * port_size * 0.01
    mp_past['size'] = mp_past['%'] * port_size * 0.01
    
    
    # Merge Dataframe by full outer join 
    test = pd.merge(mp_past, mp_present, on = 'ETF', how = 'outer', indicator = True)
    test = test.replace(np.nan, 0)
    
    portfolio_change = test[['ETF', 'size_x', 'size_y']]
    portfolio_change['change'] = portfolio_change['size_x'] - portfolio_change['size_y']
    portfolio_change = pd.merge(portfolio_change, etfpx, on = 'ETF', how = 'inner', indicator = True)
    portfolio_change['shares_change'] = (portfolio_change['change'] / portfolio_change['PX LAST']).round(decimals = 0)
    # get the change in shares 
    
    # Merge Dataframe 
    print (portfolio_change)
    
    
def model_portfolio_calc(sample, red_date, cur_date):
    model_portfolio = sample
    date = model_portfolio['Date'].unique()
    
    mp_present = model_portfolio[model_portfolio['Date'] == date[0]][['테마', 'ETF', '%']]
    mp_past = model_portfolio[model_portfolio['Date'] == date[1]][['테마', 'ETF', '%']]
    
    
    # set dummy input portfolio size = $100,000
    # give the expected proportion to the respective portfolio size for the past and present 
    
    port_size = 100000
    mp_present['size'] = mp_present['%'] * port_size * 0.01
    mp_past['size'] = mp_past['%'] * port_size * 0.01
    
    
    # Merge Dataframe by full outer join 
    test = pd.merge(mp_past, mp_present, on = 'ETF', how = 'outer', indicator = True)
    test = test.replace(np.nan, 0)
    
    portfolio_change = test[['ETF', 'size_x', 'size_y']]
    portfolio_change['change'] = portfolio_change['size_x'] - portfolio_change['size_y']
    portfolio_change = pd.merge(portfolio_change, etfpx, on = 'ETF', how = 'inner', indicator = True)
    portfolio_change['shares_change'] = (portfolio_change['change'] / portfolio_change['PX LAST']).round(decimals = 0)
    # get the change in shares 
    
    # Merge Dataframe 
    print (portfolio_change)
    