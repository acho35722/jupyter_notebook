# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 14:23:45 2021

@author: ahram.cho
"""

import pandas as pd
from pandas import DataFrame
from datetime import date 
import calendar
from datetime import datetime
from functools import reduce
import settings


inv_score = settings.n_investor_score
print(inv_score)

df_asset_mix = pd.DataFrame(index=["Type", "Risk Score", "Weight"], columns=["초고위험", "초저위험"])
df_asset_mix.loc['Type'] = ["해외주식ETF", "해외채권ETF"]
df_asset_mix.loc['Risk Score'] = ["5.0", "1.0"]

cash_weight = 2.0

if inv_score >= 85:
    max_risk = 95
    print("")
    print("고객님의 투자 성향은 공격형입니다")
    print("위험 자산에 최대 100%까지 투자할 수 있습니다")
elif inv_score >= 69:
    max_risk = 84
    print("")
    print("고객님의 투자 성향은 적극투자형입니다")
    print("위험 자산에 최대 80%까지 투자할 수 있습니다")
elif inv_score >= 53:
    max_risk = 68
    print("")
    print("고객님의 투자 성향은 위험·수익중립형입니다")
    print("위험 자산에 최대 50%까지 투자할 수 있습니다")
elif inv_score >= 37:
    max_risk = 52
    print("")
    print("고객님의 투자 성향은 안정성장형입니다")
    print("위험 자산에 최대 30%까지 투자할 수 있습니다")
elif inv_score >= 36:
    max_risk = 21
    print("")
    print("고객님의 투자 성향은 안정추구형입니다")
    print("위험 자산에 최대 30%까지 투자할 수 있습니다")
else:
    max_risk = 20
    print("")
    print("고객님의 투자 성향은 안전형입니다")
    print("위험 자산에 최대 20%까지 투자할 수 있습니다")

df_asset_mix.loc['Weight'] = [max_risk, 100-max_risk]

#screener_result_original = pd.read_csv('output/3. Result.csv')
#screener_rank_original = pd.read_excel('input/screener_rank.xlsx')
#screener_px_original = pd.read_excel('input/screener_etfpx.xlsx', index_col=0)

#screener_rank = screener_rank 
#screener_result = sample_ans
#screener_data = screener_data

def return_asset_mix(inv_score):
    if inv_score >= 85:
        max_risk = 95
        print("")
        print("고객님의 투자 성향은 공격형입니다")
        print("위험 자산에 최대 100%까지 투자할 수 있습니다")
    elif inv_score >= 69:
        max_risk = 84
        print("")
        print("고객님의 투자 성향은 적극투자형입니다")
        print("위험 자산에 최대 80%까지 투자할 수 있습니다")
    elif inv_score >= 53:
        max_risk = 68
        print("")
        print("고객님의 투자 성향은 위험·수익중립형입니다")
        print("위험 자산에 최대 50%까지 투자할 수 있습니다")
    elif inv_score >= 37:
        max_risk = 52
        print("")
        print("고객님의 투자 성향은 안정성장형입니다")
        print("위험 자산에 최대 30%까지 투자할 수 있습니다")
    elif inv_score >= 36:
        max_risk = 21
        print("")
        print("고객님의 투자 성향은 안정추구형입니다")
        print("위험 자산에 최대 30%까지 투자할 수 있습니다")
    else:
        max_risk = 20
        print("")
        print("고객님의 투자 성향은 안전형입니다")
        print("위험 자산에 최대 20%까지 투자할 수 있습니다")
    
    df_asset_mix.loc['Weight'] = [max_risk, 100-max_risk]
    
    #print (df_asset_mix)
    
    return df_asset_mix



# 1. Order 

def screener_portfolio_mod(screener_result, screener_rank, screener_data):

    result = screener_result[['순위', '테마', 'ETF']]
    
    result = result.sort_values(by = ['순위'])
    result = result.head(10)
    
    # 2. Order With VOL_260D
    vol_260D = screener_rank[['FULL TICKER', 'VOL 260D']]
    df = pd.merge(result, vol_260D, left_on = 'ETF', right_on = 'FULL TICKER', how = 'inner')    
            
    # 3. Calculation 
    
    #df['/100'] = df['VOL 260D'] / 100
    #df['^2'] = df['/100'] * df['/100']
    #df['1/^2'] = 1 / df['^2'] 
    
    # Sum 
    #df_sum = df['1/^2'].sum()
    #df['%'] = df['1/^2'] / df_sum 
    
    df_isr = 1/((df['VOL 260D']/100).pow(2))
    isr_sum = df_isr.sum()
    df['%'] = df_isr/isr_sum * max_risk
    
    remain_wgt = (100-max_risk-cash_weight)/2
    df.loc[10] = [11, "US Bonds", "BND US EQUITY", "BND US EQUITY", 0, remain_wgt]
    df.loc[11] = [12, "US Bonds", "AGG US EQUITY", "AGG US EQUITY", 0, remain_wgt]
    
    #date = screener_rank['Date']
    #df['Date'] = date
    
    df['Date'] = screener_rank['DATE']
    df = df.drop(['FULL TICKER', 'VOL 260D'], axis = 1)
    
    #def weight():
    #    score4 = pd.DataFrame.to_csv(df, 'output/4. Weight.csv', sep=',', na_rep='.', index=False, encoding='utf-8-sig')
    #    return df
    
    df_selection_prnt = df.loc[:,['순위', '테마', 'ETF', '%']]
    df_rebalance_prnt = df_selection_prnt.copy()
    
    screener_result = screener_result.sort_values(['순위'], ascending = True)
    df_px = screener_result['ETF_price'][:10]
    bonds = screener_data.iloc[1:3]['PX']
    df_px = pd.concat([df_px, bonds])
    
    
    df_rebalance_prnt.loc[:,'ETF_price'] = df_px.values
    
    fx_rate = screener_data.iloc[0]['PX']
    inv_krw = 50000000
    inv_usd = inv_krw/fx_rate
    
    df_rebalance_prnt['SHARES'] = round(df_rebalance_prnt['%']*inv_usd/100/df_rebalance_prnt['ETF_price'])
    
    #show = weight()
    
    return df_rebalance_prnt


#answer = screener_portfolio_mod(screener_result, screener_rank, screener_data)