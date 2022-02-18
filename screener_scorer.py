import sys
import pandas as pd
from pandas import DataFrame
from datetime import date 
import os
import numpy as np
import calendar
from datetime import datetime


# 1-4 import SQlite DB
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey


## 수정사항: 투자가능 ETF 뭐가 있는지 확인 해야함 

# =============================================================================
# date = input("Enter the portfolio date (format: YYYYMMDD) : ")
# variable = create_engine('sqlite:///theme_rotation.db', echo=True)
# connection = variable.connect()
# connection.text_factory = bytes
# 
# # 1. table1 
# table1meta = MetaData(variable)
# table1 = Table('etf_data', table1meta, autoload=True)
# DBSession = sessionmaker(bind=variable)
# session = DBSession()
# session.text_factory = bytes
# 
# result1 = session.query(table1)
# screener_data = pd.read_sql(result1.statement, result1.session.bind)
# screener_data = screener_data.drop(columns = ['index'])
# result1.all()
# 
# table2 = Table('etf_score', table1meta, autoload=True)
# result2 = session.query(table2)
# etf_score = pd.read_sql(result2.statement, result2.session.bind)
# etf_score = etf_score.drop(columns = ['index'])
# result2.all()
# 
# date_int = int(date)
# screener_data = screener_data[screener_data['DATE'] == date_int]
# etf_score = etf_score[etf_score['DATE'] == date_int]
# 
# connection.close()
# session.close()
# =============================================================================


# 투자가능 ETF Screening 
# 1. Make the initial Sheet: 설정액 현재 -> Final Value 까지
def initial_sheet(screener_data):
    scorer_A = screener_data[['DATE', 'THEME_ID', 'THEME_NAME', 'FULL TICKER', 'NAME', 'CURRENCY', 'MCAP(USD)', 'PX']]
    scorer_B = screener_data[['1M TR', '3M TR', '6M TR', '9M TR', '1Y TR', 'VOL 20D', 'VOL 60D', 'VOL 120D', 'VOL 180D', 'VOL 260D', 'SHS_OUT', 'SHS_OUT_3M_AGO']]

    scorer_data = [scorer_A, scorer_B]
    
    nan_value = 0
    scorer_sheet = pd.concat(scorer_data, join='outer', axis=1).fillna(nan_value)
    
    return scorer_sheet

#scorer_sheet = initial_sheet(screener_data)


def final_score(screener_data, scorer_sheet):
    
    inc_date = 90 
    scorer_sheet['INC DATE'] = np.where(screener_data['TRADE_DATE'] > inc_date, 1, 0) 
    
    mkt_cap = 20
    scorer_sheet['MKT CAP'] = np.where(scorer_sheet['MCAP(USD)'].astype(float) < mkt_cap, 0, 1)
    
    trd_amt = 1500000
    scorer_sheet['TRD AMT'] = np.where((screener_data['TRADE_AMOUNT']) < trd_amt, 0, 1)
    
    avg_spd = 0.5
    scorer_sheet['B/A%'] = np.where((screener_data['AVERAGE_BID_ASK_SPREAD_%']) < avg_spd, 1, 0)
    
    nv_te = 5 
    scorer_sheet['NAV TE'] = np.where((screener_data['NAV_TRACKING_ERROR']) < nv_te, 1, 0)
    
    scorer_sheet['PASSIVE'] = np.where((screener_data['ACTIVELY_MANAGED']) == 'Y' , 0, 1)
    
    scorer_sheet['FINAL'] =  scorer_sheet['INC DATE'] * scorer_sheet['MKT CAP'] * scorer_sheet['TRD AMT'] * scorer_sheet['B/A%'] * scorer_sheet['NAV TE'] * scorer_sheet['PASSIVE'] 
   
    return scorer_sheet
    

# = final_score(screener_data, scorer_sheet)

# 2. Module A: Calculate MOD.1Y TR, MOD.1Y 

def module_A(scorer_sheet):
    median_TR = scorer_sheet['1Y TR']
    TR_median = median_TR.median()
    
    scorer_sheet.loc[scorer_sheet['1Y TR'] != 0, 'MOD.1Y TR'] = scorer_sheet['1Y TR']
    scorer_sheet.loc[scorer_sheet['1Y TR'] == 0, 'MOD.1Y TR'] = TR_median 
    
    median_V = scorer_sheet['VOL 260D']
    V_median = median_V.median()
    
    scorer_sheet.loc[scorer_sheet['VOL 260D'] != 0, 'MOD.1Y V'] = scorer_sheet['VOL 260D']
    scorer_sheet.loc[scorer_sheet['VOL 260D'] == 0, 'MOD.1Y V'] = V_median 
    
    return scorer_sheet

#scorer_A = module_A(scorer_sheet)

# 3. Module B: Calculate R/V3M,	R/V6M, R/V9M, MOD.R/V12M 
# 0 지수 문제 생김 / 지금은 데이터에서 0 빼기 

def module_B(scorer_sheet):
        
    
    vol60_median = scorer_sheet['VOL 60D'].median()
    vol120_median = scorer_sheet['VOL 120D'].median()
    vol180_median = scorer_sheet['VOL 180D'].median()
    MRV_median = scorer_sheet['MOD.1Y V'].median()
            
    scorer_sheet.loc[scorer_sheet['VOL 60D']  == 0,'VOL 60D'] = vol60_median
    scorer_sheet.loc[scorer_sheet['VOL 120D']  == 0, 'VOL 120D'] = vol120_median
    scorer_sheet.loc[scorer_sheet['VOL 180D']  == 0, 'VOL 180D'] = vol180_median
    scorer_sheet.loc[scorer_sheet['MOD.1Y V']  == 0, 'MOD.1Y V'] = MRV_median
    
    scorer_sheet['R/V3M'] = scorer_sheet['3M TR'].astype(float) / scorer_sheet['VOL 60D'].astype(float)
    scorer_sheet['R/V6M'] = scorer_sheet['6M TR'].astype(float) / scorer_sheet['VOL 120D'].astype(float)
    scorer_sheet['R/V9M'] = scorer_sheet['9M TR'].astype(float) / scorer_sheet['VOL 180D'].astype(float)
    scorer_sheet['MOD.R/V12M'] = scorer_sheet['MOD.1Y TR'].astype(float) / scorer_sheet['MOD.1Y V'].astype(float)
    

    
    return scorer_sheet 

#scorer_B = module_B(scorer_sheet).med

# 4. Module C: Percent Rank PR.3M,PR.6M,PR.9M,PR.12M,PR.R/V3M,PR.R/V6M,PR.R/V9M,PR.R/V12M

def module_C(scorer_sheet):
    scorer_sheet['PR.3M'] = scorer_sheet['3M TR'].rank(pct = True)
    scorer_sheet['PR.6M'] = scorer_sheet['6M TR'].rank(pct = True)
    scorer_sheet['PR.9M'] = scorer_sheet['9M TR'].rank(pct = True)
    scorer_sheet['PR.12M'] = scorer_sheet['1Y TR'].rank(pct = True)
    scorer_sheet['PR.R/V3M'] = scorer_sheet['R/V3M'].rank(pct = True)
    scorer_sheet['PR.R/V6M'] = scorer_sheet['R/V6M'].rank(pct = True)
    scorer_sheet['PR.R/V9M'] = scorer_sheet['R/V9M'].rank(pct = True)
    scorer_sheet['PR.R/V12M'] = scorer_sheet['MOD.R/V12M'].rank(pct = True)
    
    return scorer_sheet

# = module_C(scorer_sheet)

# 4. Module D: Sumproduct WGT.S.R , WGT.S.R/V (Dot Product) & PR.R	PR.R/V

def Module_D(scorer_sheet):
    
    # Sumproduct     
    pr_ratio = [0.1, 0.2, 0.3, 0.4]
    
    sumprod_SR = scorer_sheet[['PR.3M', 'PR.6M','PR.9M','PR.12M']]
    scorer_sheet['WGT.S.R'] = np.dot(sumprod_SR, pr_ratio)
    
    sumprod_SRV = scorer_sheet[['PR.R/V3M','PR.R/V6M',	'PR.R/V9M',	'PR.R/V12M']]
    scorer_sheet['WGT.S.R/V'] = np.dot(sumprod_SRV, pr_ratio)
    
    # Percent Rank 
    scorer_sheet['PR.R'] = scorer_sheet['WGT.S.R'].rank(pct = True) * scorer_sheet['FINAL']
    scorer_sheet['PR.R/V'] = scorer_sheet['WGT.S.R/V'].rank(pct = True) * scorer_sheet['FINAL']
    
    # Sumproduct 
    prv_ratio = [0.3, 0.7]
    sumprod_PRV = scorer_sheet[['PR.R','PR.R/V']]
    scorer_sheet['PR.R+R/V'] = np.dot(sumprod_PRV, prv_ratio)
       
    return scorer_sheet

#scorer_D = Module_D(scorer_sheet)

# 5. Module F: Load Data from screener_score: SG,EPSG,SREV,EREV
# Need further edit on if-else statement
#_____이것도 업로드 필요 


def Module_E(scorer_sheet, etf_score):
    
    scorer_sheet = scorer_sheet[3:]
    scorer_sheet = scorer_sheet.reset_index()
    
    etf_score = etf_score.reset_index()

    scorer_sheet['SG'] = etf_score['SG']
    #scorer_sheet.join()
    scorer_sheet['EPSG'] = etf_score['EPSG']
    scorer_sheet['SREV'] = etf_score['SR']
    scorer_sheet['EREV'] = etf_score['ER']

    return scorer_sheet

#scorer_E = Module_E(scorer_sheet, etf_score)

# 6. Module G: PR.SG, PR.EPSG, PR.SREV, PR.EREV

def Module_F(scorer_sheet):
    scorer_sheet['PR.SG'] = scorer_sheet['SG'].rank(pct = True) * scorer_sheet['FINAL']
    scorer_sheet['PR.EPSG'] = scorer_sheet['EPSG'].rank(pct = True) * scorer_sheet['FINAL']
    scorer_sheet['PR.SREV'] = scorer_sheet['SREV'].rank(pct = True) * scorer_sheet['FINAL']
    scorer_sheet['PR.EREV'] = scorer_sheet['EREV'].rank(pct = True) * scorer_sheet['FINAL']
    
    return scorer_sheet

#scorer_F = Module_F(scorer_sheet)

# 7. Module H: PR.G, PR.REV, PR.G+REV, TOTAL
# all average
def Module_G(scorer_sheet):
    
    # average 
    prg = scorer_sheet[['PR.SG', 'PR.EPSG']]
    pr_rev = scorer_sheet[['PR.SREV', 'PR.EREV']]
    pr_grev = scorer_sheet[['PR.SG', 'PR.EPSG', 'PR.SREV', 'PR.EREV']]
    
    scorer_sheet['PR.G'] = prg.mean(axis = 1)
    scorer_sheet['PR.REV'] = pr_rev.mean(axis = 1)
    scorer_sheet['PR.G+REV'] = pr_grev.mean(axis = 1)
    
    # sumprod
    total_ratio = [0.15, 0.35, 0.25, 0.25]
    total = scorer_sheet[['PR.R', 'PR.R/V', 'PR.G', 'PR.REV']]
    
    scorer_sheet['TOTAL'] = np.dot(total, total_ratio)    
    
    return scorer_sheet

#scorer_G = Module_G(scorer_sheet)


def theme_score(screener_data, etf_score):
    scorer_sheet = initial_sheet(screener_data)
    scorer_sheet = final_score(screener_data, scorer_sheet)
    ans = module_A(scorer_sheet)
    ans = module_B(ans)
    ans = module_C(ans)
    ans = Module_D(ans)
    ans = Module_E(ans, etf_score)
    ans = Module_F(ans)
    ans = Module_G(ans)
    
    # Output as an Excel File 
    #score = pd.DataFrame.to_csv(scorer_sheet, 'output/1. Score.csv', sep=',', na_rep='.', index=False)
        
    return ans

#ans = theme_score(scorer_sheet, etf_score)


