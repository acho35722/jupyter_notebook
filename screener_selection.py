# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:48:40 2021

@author: ahram.cho
"""

import sys
import pandas as pd
from pandas import DataFrame
from datetime import date 
import shutil
from tempfile import mkdtemp
import os
import shutil
import numpy as np
from datetime import datetime
import math


#screener_rank = show
#screener_output = ans 

# 0. Make Initial File 
def investable_etf(screener_rank):
        
    screener_format = pd.DataFrame()
    lst = ['Health/Biotech', 'Cloud', 'Payments', 'Internet/e-Retail', 'AI/Data/Automation', 'Cyber Security', 'e-Sports', 'Network/5G', 'AV/EV', 
           'Infrastructure', 'Rare Metal', 'Clean Energy', 'China IT', 'China Healthcare', 'Semiconductor']  
    screener_format = pd.DataFrame(lst, columns = ['THEME_NAME'])
    #screener_format.columns = ['THEME NAME']

    
    count_list = []
    for i in screener_format['THEME_NAME']:
        count = sum(screener_rank['THEME_NAME'] == i)
        count_list.append(count)
        
    screener_format['Number of respective ETF'] = count_list
    
# 2.  투자 가능 ETF 개수
    investable_etf = screener_rank.groupby('THEME_NAME')['IN/OUT'].sum()
    ordered_etf = []
    for i in screener_format['THEME_NAME']:
        ordered_etf.append(investable_etf[i])
        
    screener_format['Number of respective ETF'] = ordered_etf
    
    return screener_format


#step_A = investable_etf(show)

# 3. 설정액(현재)	설정액(3개월전)	설정액증가율 
def investable_amount(screener_format, screener_rank):   
    screener_rank['SHS_OUT'] = screener_rank['SHS_OUT'].astype(float)
    df = screener_rank.groupby('THEME_NAME')['SHS_OUT'].sum().astype(float)
    screener_rank['SHS_OUT_3M_AGO'] = screener_rank['SHS_OUT_3M_AGO'].astype(float)
    df2 = screener_rank.groupby('THEME_NAME')['SHS_OUT_3M_AGO'].sum().astype(float)
    order = []
    #df3 = df / df2 * 100 - 100
    ordered_df = []
    
    
    for i in screener_format['THEME_NAME']:
        #screener_format['Investable'][i] = investable_etf[i]
    #    print (df[i])
        ordered_df.append(df[i])
        order.append(df2[i])
    
    screener_format['SHS_OUT'] = ordered_df
    screener_format['SHS_OUT_3M_AGO'] = order
    screener_format['Shares Increase'] = screener_format['SHS_OUT'].astype(float) / screener_format['SHS_OUT_3M_AGO'].astype(float)* 100 - 100
    screener_format['Shares Increase'] = screener_format['SHS_OUT'].astype(float) / screener_format['SHS_OUT_3M_AGO'].astype(float)* 100 - 100
    
    return screener_format
# 4. PR.R	PR.R/V	PR.G	PR.REV	PR.G+REV

#step_B = investable_amount(step_A, screener_rank)    

def return_invest(screener_format, screener_rank):
    prr = screener_rank.groupby('THEME_NAME')['PR.R'].sum() 
    prrv = screener_rank.groupby('THEME_NAME')['PR.R/V'].sum() 
    prg = screener_rank.groupby('THEME_NAME')['PR.G'].sum() 
    prrev = screener_rank.groupby('THEME_NAME')['PR.REV'].sum() 
    prgrev = screener_rank.groupby('THEME_NAME')['PR.G+REV'].sum() 
    
    prr_ordered = []
    prrv_ordered = []
    prg_ordered = []
    prrev_ordered = []
    prgrev_ordered = []
    
    for i in screener_format['THEME_NAME']:
       #screener_format['Investable'][i] = investable_etf[i]
       prr_ordered.append(prr[i]) 
       prrv_ordered.append(prrv[i])      
       prg_ordered.append(prg[i])  
       prrev_ordered.append(prrev[i])  
       prgrev_ordered.append(prgrev[i])  
    
    screener_format['PR.R'] = prr_ordered / screener_format['Number of respective ETF']
    screener_format['PR.R/V'] = prrv_ordered / screener_format['Number of respective ETF']
    screener_format['PR.G'] = prg_ordered / screener_format['Number of respective ETF']
    screener_format['PR.REV'] = prrev_ordered / screener_format['Number of respective ETF']
    screener_format['PR.G+REV'] = prgrev_ordered / screener_format['Number of respective ETF']
    
    return screener_format 

#step_C = return_invest(step_B, screener_rank)

# 5. 0.1	0.3	0.3	0.15	0.15 + extra 
def return_number(screener_format):
    screener_format['0.1'] = screener_format['Shares Increase'].rank(axis = 0, pct = True)
    screener_format['0.3'] = screener_format['PR.R'].rank(axis = 0, pct = True)
    screener_format['0.3_b'] = screener_format['PR.R/V'].rank(axis = 0, pct = True)
    screener_format['0.15'] = screener_format['PR.G'].rank(axis = 0, pct = True)
    screener_format['0.15_b'] = screener_format['PR.REV'].rank(axis = 0, pct = True)
    screener_format['rank_last'] = screener_format['PR.G+REV'].rank(axis = 0, pct = True)
    
    
    
    
    total_ratio = [0.1, 0.3, 0.3, 0.15, 0.15, 0]
    total_prod = screener_format[screener_format.columns[10:]]
    screener_format['종합'] = np.dot(total_prod, total_ratio)
    screener_format['순위'] = screener_format['종합'].rank(ascending = False) 
    screener_format['테마'] = screener_format['THEME_NAME']
    
    return screener_format

#step_D = return_number(step_C)    


def return_selection(screener_output, screener_rank, screener_format):  
    screener_format = screener_format
    sample = ['Health/Biotech', 'Cloud', 'Payments', 'Internet/e-Retail', 'AI/Data/Automation', 'Cyber Security', 'e-Sports', 'Network/5G', 'AV/EV', 
           'Infrastructure', 'Rare Metal', 'Clean Energy', 'China IT', 'China Healthcare', 'Semiconductor']  
    #screener_output = ans
    groupby = {}
    for i in sample:
        df_i = screener_rank.loc[screener_rank['THEME_NAME'] == i]
        groupby[i] = df_i
    
    etf = []
    for i in screener_format['THEME_NAME']:
        for j in groupby:
            if i == j:
                obj = groupby[j]
                #if obj['ETF_rank'].idxmin() != int() :
                    #minimumm = int(obj['ETF_rank'].nsmallest(2).index[1])
                #    pass
                #else:
                minimum = obj['ETF_rank'].idxmin() 
                
                
                minm = screener_rank['level_0'].iloc[minimum]
                etf.append(minm)

        
    ticker = []
    price = []
    for i in etf:
        for j in screener_rank.iterrows():
    #        print (j)
            if i == j[1]['level_0']:
                answer = j[1]['FULL TICKER']
                prc = j[1]['PX']
                ticker.append(answer)
                price.append(prc)
    
    screener_format['ETF'] = ticker
    screener_format['ETF_price'] = price
    
    return screener_format
    
#step_E = return_selection(screener_output, screener_rank, step_D)

def screener_selection(screener_output, screener_rank):
    step_A = investable_etf(screener_rank)
    step_B = investable_amount(step_A, screener_rank)
    step_C = return_invest(step_B, screener_rank)
    step_D = return_number(step_C)
    
    result = return_selection(screener_output, screener_rank, step_C)

    return result


#sample_ans = screener_selection(screener_output, screener_rank)
    

