# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:02:06 2022

@author: ahram.cho
"""

import sys
import pandas as pd
from pandas import DataFrame
from datetime import date
import os
import numpy as np
import calendar
from datetime import datetime
from IPython.display import display, HTML
import warnings
warnings.filterwarnings('ignore')

# 0. 투자자 성향 도출 : investor_score 에 변수로 저장

import settings
import investment_score_mod
investor_score = settings.n_investor_score

# 1. 테마 ETF 비중 계산
# 1 - 1 screener 
import screener_scorer, screener_intra_sector, screener_selection, screener_portfolio_mod
from screener_scorer import theme_score
from screener_intra_sector import intra_sector, return_groupby
from screener_selection import screener_selection
from screener_portfolio_mod import screener_portfolio_mod, return_asset_mix
                                
# 1 - 2 import SQlite DB
import sqlite3
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey

# A. archive: loading data into s
#---------------------------------------------------------------------------------------------------# 
# A-a. Open the existing database  
#---------------------------------------------------------------------------------------------------# 
    

def call_data():

    date = input("Enter the portfolio date (format: YYYYMMDD) : ")
    variable = create_engine('sqlite:///theme_rotation.db', echo=False)
    connection = variable.connect()
    connection.text_factory = bytes
    
    # 1. table1 
    table1meta = MetaData(variable)
    table1 = Table('etf_data', table1meta, autoload=True)
    DBSession = sessionmaker(bind=variable)
    session = DBSession()
    session.text_factory = bytes
    
    result1 = session.query(table1)
    screener_data = pd.read_sql(result1.statement, result1.session.bind)
    screener_data = screener_data.drop(columns = ['index'])
    result1.all()
    
    table2 = Table('etf_score', table1meta, autoload=True)
    result2 = session.query(table2)
    etf_score = pd.read_sql(result2.statement, result2.session.bind)
    etf_score = etf_score.drop(columns = ['index'])
    result2.all()
    
    date_int = int(date)
    screener_data = screener_data[screener_data['DATE'] == date_int]
    etf_score = etf_score[etf_score['DATE'] == date_int]
    
    
    #screener_data = pd.Series(screener_data['MCAP(USD)', 'PX', 'PX_3M_AGO', '1M TR', '3M TR', '6M TR', '9M TR', '1Y TR', 'VOL 20D', 'VOL 60D', 'VOL 120D', 'VOL 180D', 'VOL 260D', 'TER', 'SHARPE_RATIO', 'NAV_PREM', 'SHS_OUT', 'SHS_OUT_3M_AGO'])
    
    #screener_data = pd.to_numeric(screener_data['MCAP(USD)'])
    
    data = [screener_data, etf_score]
    
    connection.close()
    session.close()
    
    return data


# B. Derive the Portfolio & load the intermediary data into the local DB as (intermediary data)
#---------------------------------------------------------------------------------------------------# 
data = call_data()


def return_mp(data, investor_score):    
    #data = call_data()
    screener_data = data[0]
    etf_score = data[1]
    
    screener_output = theme_score(screener_data, etf_score)
    
    screener_rank = intra_sector(screener_output)
    groupbyobj = return_groupby(screener_output)
    
    screener_result = screener_selection(screener_output, screener_rank)
        
    model_portfolio = screener_portfolio_mod(screener_result, screener_rank, screener_data)
    
    #print (model_portfolio)
    
    return model_portfolio
    
# if want to find the rebalance period
#---------------------------------------------------------------------------------------------------# 

print ("")
investor_score = settings.n_investor_score
asset_mix_score = return_asset_mix(investor_score)
display(HTML(asset_mix_score.to_html()))
investor_score = return_mp(data, investor_score)
display(HTML(investor_score.to_html()))

print ("")
investor_score = 100
asset_mix_100 = return_asset_mix(investor_score)
display(HTML(asset_mix_100.to_html()))
investor_100 = return_mp(data, investor_score)
display(HTML(investor_100.to_html()))

print ("")
investor_score = 80
asset_mix_80 = return_asset_mix(investor_score)
display(HTML(asset_mix_80.to_html()))
investor_80 = return_mp(data, investor_score)
display(HTML(investor_80.to_html()))

print ("")
investor_score = 50
asset_mix_50 = return_asset_mix(investor_score)
investor_50 = return_mp(data, investor_score)
display(HTML(asset_mix_50.to_html()))
display(HTML(investor_50.to_html()))




