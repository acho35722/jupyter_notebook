# -*- coding: utf-8 -*-

"""
     1. 고객님의 금융상품에 대한 이해 수준은 어느 정도라고 생각 하십니까?
            파생상품을 포함한 대부분의 금융투자상품의 구조 및 위험을 상품설명서 등을 읽고 스스로 이해할 수 있음
            널리알려진 금융투자상품(주식, 채권, 펀드 등)의 구조 및 위험을 이해하고 있음
            널리알려진 금융투자상품(주식, 채권, 펀드 등)의 특징을 일정 부분 이해하고 있으며 설명을 들으면 구조와 위험을 이해할 수 있음
            금융투자상품에 대해 스스로 결정을 해 본 적이 없음
     2. 고객님께서 투자하신 경험이 있는 금융자산 또는 투자형태는 어떤 것입니까?
            선물·옵션·ELW, 신용거래, 파생상품펀드(파생형ETF 포함)
            주식, 주식형펀드, ELS/DLS, 투자자문·일임, 외화자산, 신탁
            혼합형펀드, 회사채, CP, 전자단기사채, 채권형펀드
            예금, CMA, MMF, RP, 국공채
            금융 투자 경험 없음
     3. 고객님께서 투자한 금융투자상품(주식, 펀드, 채권, 파생상품 등)의 투자경험기간은 총 얼마나 되십니까?
            10년 이상
            3년 이상 - 10년 미만
            1년 이상 - 3년 미만
            1년 미만
            전혀 없음     
     4. 고객님의 총 금융자산대비 금융투자상품(주식, 펀드, 채권, 파생상품 등)은 어느 정도의 비중을 차지합니까?
            70% 이상
            50% 이상 - 70% 미만
            10% 이상 - 50% 미만
            10% 미만
     5. 고객님과 고객님의 가족을 포함하여 현재와 미래의 소득수준을 가장 잘 표현한 것은 어느 것입니까?
            현재 안정적인 소득(급여, 금융소득 등)이 발생하고 있으며, 향후 현재의 소득수준의 유지 혹은 증가 예상
            현재 안정적인 소득(급여, 금융소득 등)이 발생하고 있으며, 향후 현재의 소득수준의 감소 예상
            현재나 미래에 일정한 소득(급여, 금융소득)을 통한 여유자금의 마련이 어려울 것으로 예상     
     6. 고객님께서 금융상품 투자를 통해 기대하는 수익과 감수할 수 있는 손실을 가장 잘 표현한 것은 어느 것입니까?
            원금 초과 손실까지 감수하며 적극적인 투자를 통하여 시장수익률(예:주가지수)을 초과하는 높은 수익을 추구
            원금손실을 감수하며 시장수익률과 비슷한 수준의 수익을 기대
            원금의 일부 손실을 감수하며 시중금리보다 다소 높은 수준의 수익을 기대
            제한적인 손실을 감수하며 시중금리 수준의 수익을 기대     
     7. 고객님께서 1년의 기간 동안(투자를 변경하기 전에) 고객님께서 질 수 있는 대략적인 손실은 어느 정도입니까?
            25% 이상
            10% 이상 - 15% 미만
            5% 이상 - 10% 미만
            5% 이하
            
    8. 고객님의 현재 나이는 어떻게 되십니까?
            30세 이하
            31세~40세
            41세~50세 
            51세~60세
            61세 이상
"""

import tkinter as tk
from tkinter import ttk

import settings
import pandas as pd

print("Running investment_score.py")

root = tk.Tk()
root.title('투자자 성향 설문 조사')
root.geometry('800x480')

ttk.Label(root, text="1. 고객님의 금융상품에 대한 이해 수준은 어느 정도라고 생각 하십니까?:").grid(column=0, row=0, padx=2, pady=2, sticky='w')
s_q1 = tk.StringVar()
q1 = ttk.Combobox(root, textvariable=s_q1, width=100)
q1['values'] = ('파생상품을 포함한 대부분의 금융투자상품의 구조 및 위험을 상품설명서 등을 읽고 스스로 이해할 수 있음',
                '널리알려진 금융투자상품(주식, 채권, 펀드 등)의 구조 및 위험을 이해하고 있음',
                '널리알려진 금융투자상품(주식, 채권, 펀드 등)의 특징을 일정 부분 이해하고 있으며 설명을 들으면 구조와 위험을 이해할 수 있음',
                '금융투자상품에 대해 스스로 결정을 해 본 적이 없음')
q1.grid(column=0, row=1, padx=5, sticky='w')
q1.current()

ttk.Label(root, text = "2. 고객님께서 투자하신 경험이 있는 금융자산 또는 투자형태는 어떤 것입니까?").grid(column=0, row=2, padx=2, pady=2, sticky='w')
s_q2 = tk.StringVar()
q2 = ttk.Combobox(root, textvariable=s_q2, width=100)
q2['values'] = ('선물·옵션·ELW, 신용거래, 파생상품펀드(파생형ETF 포함)',
                '주식, 주식형펀드, ELS/DLS, 투자자문·일임, 외화자산, 신탁',
                '혼합형펀드, 회사채, CP, 전자단기사채, 채권형펀드',
                '예금, CMA, MMF, RP, 국공채',
                '금융 투자 경험 없음')
q2.grid(column=0, row=3, padx=5, sticky='w')
q2.current()

ttk.Label(root, text = "3. 고객님께서 투자한 금융투자상품(주식, 펀드, 채권, 파생상품 등)의 투자경험기간은 총 얼마나 되십니까?").grid(column=0, row=4, padx=2, pady=2, sticky='w')
s_q3 = tk.StringVar()
q3 = ttk.Combobox(root, textvariable=s_q3, width=100)
q3['values'] = ('10년 이상',
                '3년 이상 - 10년 미만',
                '1년 이상 - 3년 미만',
                '1년 미만',
                '전혀 없음')
q3.grid(column=0, row=5, padx=5, sticky='w')
q3.current()

ttk.Label(root, text = "4. 고객님의 총 금융자산대비 금융투자상품(주식, 펀드, 채권, 파생상품 등)은 어느 정도의 비중을 차지합니까?").grid(column=0, row=6, padx=2, pady=2, sticky='w')
s_q4 = tk.StringVar()
q4 = ttk.Combobox(root, textvariable=s_q4, width=100)
q4['values'] = ('70% 이상',
                '50% 이상 - 70% 미만',
                '10% 이상 - 50% 미만',
                '10% 미만')
q4.grid(column=0, row=7, padx=5, sticky='w')
q4.current()

ttk.Label(root, text = "5. 고객님과 고객님의 가족을 포함하여 현재와 미래의 소득수준을 가장 잘 표현한 것은 어느 것입니까?").grid(column=0, row=8, padx=2, pady=2, sticky='w')
s_q5 = tk.StringVar()
q5 = ttk.Combobox(root, textvariable=s_q5, width=100)
q5['values'] = ('현재 안정적인 소득(급여, 금융소득 등)이 발생하고 있으며, 향후 현재의 소득수준의 유지 혹은 증가 예상',
                '현재 안정적인 소득(급여, 금융소득 등)이 발생하고 있으며, 향후 현재의 소득수준의 감소 예상',
                '현재나 미래에 일정한 소득(급여, 금융소득)을 통한 여유자금의 마련이 어려울 것으로 예상')
q5.grid(column=0, row=9, padx=5, sticky='w')
q5.current()

ttk.Label(root, text = "6. 고객님께서 금융상품 투자를 통해 기대하는 수익과 감수할 수 있는 손실을 가장 잘 표현한 것은 어느 것입니까?").grid(column=0, row=10, padx=2, pady=2, sticky='w')
s_q6 = tk.StringVar()
q6= ttk.Combobox(root, textvariable=s_q6, width=100)
q6['values'] = ('원금 초과 손실까지 감수하며 적극적인 투자를 통하여 시장수익률(예:주가지수)을 초과하는 높은 수익을 추구',
                '원금손실을 감수하며 시장수익률과 비슷한 수준의 수익을 기대',
                '원금의 일부 손실을 감수하며 시중금리보다 다소 높은 수준의 수익을 기대',
                '제한적인 손실을 감수하며 시중금리 수준의 수익을 기대')
q6.grid(column=0, row=11, padx=5, sticky='w')
q6.current()

ttk.Label(root, text = "7. 고객님께서 1년의 기간 동안(투자를 변경하기 전에) 고객님께서 질 수 있는 대략적인 손실은 어느 정도입니까?").grid(column=0, row=12, padx=2, pady=2, sticky='w')
s_q7 = tk.StringVar()
q7= ttk.Combobox(root, textvariable=s_q7, width=100)
q7['values'] = ('25% 이상',
                '10% 이상 - 15% 미만',
                '5% 이상 - 10% 미만',
                '5% 미만')
q7.grid(column=0, row=13, padx=5, sticky='w')
q7.current()

ttk.Label(root, text = "8. 고객님의 현재 나이는 어떻게 되십니까?").grid(column=0, row=14, padx=2, pady=2, sticky='w')
s_q8 = tk.StringVar()
q8= ttk.Combobox(root, textvariable=s_q8, width=100)
q8['values'] = ('30세 이하',
                '31세~40세',
                '41세~50세',
                '51세~60세'
                '61세 이상')
q8.grid(column=0, row=15, padx=5, sticky='w')
q8.current()

def calcScore():
    n_q1 = q1.current()
    n_q2 = q2.current()
    n_q3 = q3.current()
    n_q4 = q4.current()
    n_q5 = q5.current()
    n_q6 = q6.current()
    n_q7 = q7.current()
    n_q8 = q8.current()
    
    if n_q1 == 0:
        n_q1_score = 1
    elif n_q1 == 1:
        n_q1_score = 0.8
    elif n_q1 == 2:
        n_q1_score = 0.6
    elif n_q1 == 3:
        n_q1_score = 0.2
    else:
        n_q1_score = 0
        return

    if n_q2 == 0:
        n_q2_score = 1
    elif n_q2 == 1:
        n_q2_score = 0.8
    elif n_q2 == 2:
        n_q2_score = 0.6
    elif n_q2 == 3:
        n_q2_score = 0.4
    elif n_q2 == 4:
        n_q2_score = 0.2
    else:
        n_q2_score = 0
        return

    if n_q3 == 0:
        n_q3_score = 1
    elif n_q3 == 1:
        n_q3_score = 0.8
    elif n_q3 == 2:
        n_q3_score = 0.6
    elif n_q3 == 3:
        n_q3_score = 0.4
    elif n_q3 == 4:
        n_q3_score = 0.2
    else:
        n_q3_score = 0
        return

    if n_q4 == 0:
        n_q4_score = 1
    elif n_q4 == 1:
        n_q4_score = 0.8
    elif n_q4 == 2:
        n_q4_score = 0.6
    elif n_q4 == 3:
        n_q4_score = 0.2
    else:
        n_q4_score = 0
        return

    if n_q5 == 0:
        n_q5_score = 1
    elif n_q5 == 1:
        n_q5_score = 0.6
    elif n_q5 == 2:
        n_q5_score = 0.2
    else:
        n_q5_score = 0
        return

    if n_q6 == 0:
        n_q6_score = 1
    elif n_q6 == 1:
        n_q6_score = 0.8
    elif n_q6 == 2:
        n_q6_score = 0.6
    elif n_q6 == 3:
        n_q6_score = 0.2
    else:
        n_q6_score = 0
        return

    if n_q7 == 0:
        n_q7_score = 1
    elif n_q7 == 1:
        n_q7_score = 0.8
    elif n_q7 == 2:
        n_q7_score = 0.6
    elif n_q7 == 3:
        n_q7_score = 0.2
    else:
        n_q7_score = 0
        return
    
    if n_q8 == 0:
        n_q8_score = 1
    elif n_q8 == 1:
        n_q8_score = 0.8
    elif n_q8 == 2:
        n_q8_score = 0.6
    elif n_q8 == 3:
        n_q8_score = 0.4
    elif n_q8 == 4:
        n_q8_score = 0.2
    else:
        n_q8_score = 0
        return

    tot_score = n_q1_score + n_q2_score + n_q3_score + n_q4_score + n_q5_score + n_q6_score + n_q7_score + n_q8_score
    n_inv_score = int(tot_score/7*100)
    #print(n_inv_score)
    
    settings.n_investor_score = n_inv_score
    
    df_item = [n_inv_score]
    df_inv_score = pd.DataFrame(df_item)
    df_inv_score.to_csv("0. IS.csv", index=False, header=False)
    root.destroy()
   

btn = tk.Button(root, text="제출", overrelief="solid", command=calcScore)
btn.grid(column=0, row=16, pady=5, sticky='E')

root.mainloop()

