# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 14:28:57 2018

@author: Pei Gu
"""
import matplotlib.pyplot as plt
import sys
sys.path.append('C:\\Users\\Pei Gu\\Documents\\sogu intern\\Futures_arbitrage\\公募基金基差策略')
from get_data_calculate import get_data_calculate
from backtest_index import backtest_research_use_profit
from mutual_fund import mutual_fund
mu_fund = mutual_fund()

def backtest(startdate, enddate, statistical_term, test_term, benchmark, contract_num, money):
    data=get_data_calculate.sift_contract(startdate, enddate)
    all_code_rank, test_time_startpoint, Data, All_ARR_diff_rank, statistical_date = get_data_calculate.statistical_rank(data, statistical_term, test_term, benchmark)
    Win_ratio=get_data_calculate.Base_difference_momentum_implement(startdate, Data, test_time_startpoint, test_term, all_code_rank, contract_num, money)
    pnl_ratio=get_data_calculate.show_position_fluctuation(startdate, Data, test_time_startpoint, test_term, all_code_rank, contract_num, money)
    each_pnl_ratio, trading_dates=get_data_calculate.each_test_term_fluctuation(startdate, Data, test_time_startpoint, test_term, all_code_rank, contract_num, money)
    pnl_ratio.plot()
    return all_code_rank, pnl_ratio, All_ARR_diff_rank, Win_ratio, statistical_date,each_pnl_ratio,trading_dates, data
    return plt.show()

rank, PNL_ratio, all_ARR_diff_rank, win_ratio, statistical_date, each_pnl_ratio,trading_dates, data = backtest('2010-01-04','2018-08-24', 100, 100, '000001.SH', 1, 100000)
pnl_ratio = backtest_research_use_profit.back_cal_use_profit(list(PNL_ratio['pnl_ratio']),0,19/8)
value_drawdown, value_highestvalue, value_profit, value_sharpe ,value_lowestvalue,profit_year,profit_month,dside_risk,value_sortino,value_vol = pnl_ratio.research_main()

PNL_ratio.to_csv('pnl_ratio.csv')

all_ARR_diff_rank[0].to_csv('all_ARR_diff_rank0.csv')
all_ARR_diff_rank[1].to_csv('all_ARR_diff_rank1.csv')
all_ARR_diff_rank[2].to_csv('all_ARR_diff_rank2.csv')
all_ARR_diff_rank[3].to_csv('all_ARR_diff_rank3.csv')
all_ARR_diff_rank[4].to_csv('all_ARR_diff_rank4.csv')
all_ARR_diff_rank[5].to_csv('all_ARR_diff_rank5.csv')
all_ARR_diff_rank[6].to_csv('all_ARR_diff_rank6.csv')
all_ARR_diff_rank[7].to_csv('all_ARR_diff_rank7.csv')
all_ARR_diff_rank[8].to_csv('all_ARR_diff_rank8.csv')
all_ARR_diff_rank[9].to_csv('all_ARR_diff_rank9.csv')
all_ARR_diff_rank[10].to_csv('all_ARR_diff_rank10.csv')
all_ARR_diff_rank[11].to_csv('all_ARR_diff_rank11.csv')
all_ARR_diff_rank[12].to_csv('all_ARR_diff_rank12.csv')
all_ARR_diff_rank[13].to_csv('all_ARR_diff_rank13.csv')
all_ARR_diff_rank[14].to_csv('all_ARR_diff_rank14.csv')
all_ARR_diff_rank[15].to_csv('all_ARR_diff_rank15.csv')
all_ARR_diff_rank[16].to_csv('all_ARR_diff_rank16.csv')
all_ARR_diff_rank[17].to_csv('all_ARR_diff_rank17.csv')
all_ARR_diff_rank[18].to_csv('all_ARR_diff_rank18.csv')
all_ARR_diff_rank[19].to_csv('all_ARR_diff_rank19.csv')
all_ARR_diff_rank[20].to_csv('all_ARR_diff_rank20.csv')
all_ARR_diff_rank[21].to_csv('all_ARR_diff_rank21.csv')
all_ARR_diff_rank[22].to_csv('all_ARR_diff_rank22.csv')
all_ARR_diff_rank[23].to_csv('all_ARR_diff_rank23.csv')
all_ARR_diff_rank[24].to_csv('all_ARR_diff_rank24.csv')
import pandas as pd
statistical_date=pd.DataFrame({'date':statistical_date})
statistical_date.to_csv('statistical_date.csv')
rank[0].to_csv('rank0.csv')
rank[1].to_csv('rank1.csv')
rank[2].to_csv('rank2.csv')
rank[3].to_csv('rank3.csv')
rank[4].to_csv('rank4.csv')
rank[5].to_csv('rank5.csv')
rank[6].to_csv('rank6.csv')
rank[7].to_csv('rank7.csv')
rank[8].to_csv('rank8.csv')
rank[9].to_csv('rank9.csv')
rank[10].to_csv('rank10.csv')
rank[11].to_csv('rank11.csv')
rank[12].to_csv('rank12.csv')
rank[13].to_csv('rank13.csv')
rank[14].to_csv('rank14.csv')
rank[15].to_csv('rank15.csv')
rank[16].to_csv('rank16.csv')
rank[17].to_csv('rank17.csv')
rank[18].to_csv('rank18.csv')
rank[19].to_csv('rank19.csv')


each_pnl_ratio[0].to_csv('each_pnl_ratio0.csv')
each_pnl_ratio[1].to_csv('each_pnl_ratio1.csv')
each_pnl_ratio[2].to_csv('each_pnl_ratio2.csv')
each_pnl_ratio[3].to_csv('each_pnl_ratio3.csv')
each_pnl_ratio[4].to_csv('each_pnl_ratio4.csv')
each_pnl_ratio[5].to_csv('each_pnl_ratio5.csv')
each_pnl_ratio[6].to_csv('each_pnl_ratio6.csv')
each_pnl_ratio[7].to_csv('each_pnl_ratio7.csv')
each_pnl_ratio[8].to_csv('each_pnl_ratio8.csv')
each_pnl_ratio[9].to_csv('each_pnl_ratio9.csv')
each_pnl_ratio[10].to_csv('each_pnl_ratio10.csv')
each_pnl_ratio[11].to_csv('each_pnl_ratio11.csv')
each_pnl_ratio[12].to_csv('each_pnl_ratio12.csv')
each_pnl_ratio[13].to_csv('each_pnl_ratio13.csv')
each_pnl_ratio[14].to_csv('each_pnl_ratio14.csv')
each_pnl_ratio[15].to_csv('each_pnl_ratio15.csv')
each_pnl_ratio[16].to_csv('each_pnl_ratio16.csv')
each_pnl_ratio[17].to_csv('each_pnl_ratio17.csv')
each_pnl_ratio[18].to_csv('each_pnl_ratio18.csv')
each_pnl_ratio[19].to_csv('each_pnl_ratio19.csv')










#def optimize_parameters():
#    statistical_term=[]
#    test_term=[]
#    for i in range(10,500,1):
#        for a in range(10,500,1):
#            rank, PNL_ratio, all_ARR_diff_rank, win_ratio = backtest('2010-01-04','2018-08-24', 100, 100, '000001.SH', 1, 100000)
#            pnl_ratio = backtest_research_use_profit.back_cal_use_profit(list(PNL_ratio['pnl_ratio']),0,19/8)
#            value_drawdown, value_highestvalue, value_profit, value_sharpe ,value_lowestvalue,profit_year,profit_month,dside_risk,value_sortino,value_vol = pnl_ratio.research_main()
#            if 0.05<value_drawdown<0.2 and 0.4<value_sharpe<1 and 0.05<=profit_year<=0.1 and 0.1<=value_vol<0.2:
#                statistical_term.append(i)
#                test_term.append(a)
#                print('statistical_term= '+str(i)+', '+'test_term= '+str(a))
#            elif 0.01<value_drawdown<=0.05 and 0.2<value_sharpe<=0.4 and 0.03<=profit_year<0.5 and 0.05<=value_vol<0.1:
#                statistical_term.append(i)
#                test_term.append(a)
#                print('statistical_term= '+str(i)+', '+'test_term= '+str(a))
#    parameters=[statistical_term, test_term]
#    return parameters

#Parameter=optimize_parameters()