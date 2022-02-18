# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:48:40 2021
@author: ahram.cho
"""
import sys
import pandas as pd
from pandas import DataFrame
from datetime import date 
from tempfile import mkdtemp
import numpy as np
import pandas as pd
import calendar
from functools import reduce

# **** PSY US Equity 계산 N/A Value Input 확인해야함 
# 0. Open the Data 
# 몇 개가 빠져 있는 것 같긴 함 
# RNK.R	RNK.R/V	RNK.R+R/V	RNK.SG	RNK.EPSG	RNK.SREV	RNK.EREV	RNK.G	RNK.REV	RNK.G+REV	TOTAL	IN/OUT	THEME|RANK
# **** PSY US Equity 계산 N/A Value Input 확인해야함 
# 수정사항: rank 랑 수정 사항 확인 해야 함. 원래 데이터랑 결과값 맞춰서 볼 수 있는지. 

# just getting the order 
#ans = ans

def create_sheet(ans):
    screener_output = ans
    screener_intra_sector = screener_output[['DATE', 'THEME_NAME', 'FULL TICKER', 'NAME', 'FINAL']]
    group = screener_intra_sector.groupby('THEME_NAME')
    theme = screener_intra_sector.groupby('THEME_NAME').count()
    sample = theme.index.tolist()
    #groupby = {}
    
    return sample

def create_groupby(sample, ans):
    screener_output = ans
    groupby = {}
    for i in sample:
        df_i = screener_output.loc[screener_output['THEME_NAME'] == i]
        groupby[i] = df_i
    
    return groupby
    
# 2. Produce Rank_ we start w groupby     
# RNK.R	RNK.R/V	RNK.R+R/V	RNK.SG	RNK.EPSG	RNK.SREV	RNK.EREV	RNK.G	RNK.REV	RNK.G+REV	TOTAL	IN/OUT	THEME|RANK

def rank(df_i):

    df_i.loc[:,'RNK.R'] = df_i['PR.R'].rank(ascending = False)
    df_i.loc[:,'RNK.R/V'] = df_i['PR.R/V'].rank(ascending = False)
    df_i.loc[:,'RNK.R+R/V'] = df_i['PR.R+R/V'].rank(ascending = False)
    df_i.loc[:,'RNK.SG'] = df_i['PR.SG'].rank(ascending = False)
    df_i.loc[:,'RNK.EPSG'] = df_i['PR.EPSG'].rank(ascending = False)
    df_i.loc[:,'RNK.SREV'] = df_i['PR.SREV'].rank(ascending = False)
    df_i.loc[:,'RNK.EREV'] = df_i['PR.EREV'].rank(ascending = False)
    df_i.loc[:,'RNK.G'] = df_i['PR.G'].rank(ascending = False)
    df_i.loc[:,'RNK.REV'] = df_i['PR.REV'].rank(ascending = False)
    df_i.loc[:,'RNK.G+REV'] = df_i['PR.G+REV'].rank(ascending = False)
    df_i.loc[:,'TOTAL_Rank'] = df_i['TOTAL'].rank(ascending = False)
    # IN - OUT  은 추가 확인 필요 
    df_i.loc[:,'IN/OUT'] = df_i['FINAL']
    df_i.loc[:,'THEME|RANK'] = df_i['THEME_ID'].apply(str) + '/' + df_i['TOTAL_Rank'].apply(str)
    df_i.loc[:,'THEME_rank'] = df_i['THEME_ID']
    df_i.loc[:,'ETF_rank'] = df_i['TOTAL_Rank']
    df_i.loc[:,'TIKR'] = df_i['FULL TICKER']
    
    return df_i 
    
def return_intra_sector(groupby):    
    for i in groupby:
        result = rank(groupby[i])
        
    
    # Reorder the entire sheet
    order = ['Health/Biotech','Cloud','Payments','Internet/e-Retail','AI/Data/Automation','Cyber Security',
             'e-Sports','Network/5G','AV/EV','Infrastructure','Rare Metal','Clean Energy','China IT', 'China Healthcare',
             'Semiconductor']
    
    start = groupby['Health/Biotech']
    for i in order[1:]:
        for j in groupby:
            if i == j:
                end = pd.concat([start, groupby[j]], axis=0)
                start = end 
                
    screener_rank = end.reset_index()
    return screener_rank


def intra_sector(ans):
    
    sample = create_sheet(ans)
    groupby = create_groupby(sample, ans)
    intra_sector = return_intra_sector(groupby)
    
    return intra_sector

def return_groupby(ans):
    
    sample = create_sheet(ans)
    groupby = create_groupby(sample, ans)
    
    return groupby

# just checking the ordre

    
    
    