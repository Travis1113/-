# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 14:26:05 2018

@author: Pei Gu
"""

import pandas as pd
from mutual_fund import mutual_fund
mu_fund = mutual_fund()

def sift_contract(startdate, enddate):
    data = mu_fund.get_data('code,time_str,close','value_analyze3_1')
    valid_contract=[]#
    for i in range(data.iloc[:,0].size):#
        if data['time_str'][i]==startdate:#
            valid_contract.append(data['code'][i])#
    data = data.groupby(['time_str','code'])['close'].apply(lambda i:i.loc[i.index[0]] if len(i) < 2 else i.tolist()).unstack()
    data=data[data.index >= startdate]
    data=data[data.index <= enddate]
    for code in data.columns.tolist():#
        if code not in valid_contract:#
            del data[code]#
    return data   

def judge_top_last_20percent_assest(data):
    top_20percent_assest=[]
    last_20percent_assest=[]
    for i in range(len(data)):
        if data['ARR_diff'][i]>=data['ARR_diff'].quantile(0.8):
            top_20percent_assest.append(data['code'][i])
        elif data['ARR_diff'][i]<=data['ARR_diff'].quantile(0.2):
            last_20percent_assest.append(data['code'][i])
    top_last_20percent_assest=pd.DataFrame({'top_20percent_assest':top_20percent_assest,'last_20percent_assest':last_20percent_assest})
    return top_last_20percent_assest

def statistical_rank(data, statistical_term, test_term, benchmark):
    temp=[]
    test_time_point=[]
    statistical_time_point=[]
    statistical_dates=[]
    each_contract_all_accumu_return_ratio=[]
    all_contract_all_accumu_return_ratio=[]
    n=len(data)
    condition=n%statistical_term
    if condition==0:
        num=n/statistical_term
        for col in range(data.columns.size):
            for i in range(int(num)):
                for a in range(statistical_term*i, statistical_term*(i+1)-1, 1):
                    temp.append(data.iloc[a+1,col]/data.iloc[a,col]-1)
                each_contract_all_accumu_return_ratio.append(sum(temp))
                temp=[]
            all_contract_all_accumu_return_ratio.append(each_contract_all_accumu_return_ratio)
            each_contract_all_accumu_return_ratio=[]
    elif condition!=0:
        mark=[]
        data=data.reset_index()
        for i in range(condition):
            mark.append(i)
        data=data.drop(mark)
        data.set_index(["time_str"], inplace=True)
        n=len(data)
        num=n/statistical_term
        for col in range(data.columns.size):
            for i in range(int(num)):
                for a in range(statistical_term*i, statistical_term*(i+1)-1, 1):
                    temp.append(data.iloc[a+1,col]/data.iloc[a,col]-1)
                each_contract_all_accumu_return_ratio.append(sum(temp))
                temp=[]
            all_contract_all_accumu_return_ratio.append(each_contract_all_accumu_return_ratio)
            each_contract_all_accumu_return_ratio=[]
    for i in range(int(num)-1):
        test_time_point.append(statistical_term*(i+1))
    for i in range(int(num)):
        statistical_time_point.append(statistical_term*i)
    for i in statistical_time_point:
        if i==0:
            statistical_dates.append(data.index[1])
        else:
            statistical_dates.append(data.index[i])
    ARR_diff=[]
    all_ARR_diff_rank=[]
    all_top_last_20percent_code_rank=[]
    for i in range(data.columns.size):
        if data.columns[i]==benchmark:
            benchmark_num=i
            break
    columns_list=data.columns.tolist()
    del columns_list[benchmark_num]
    benchmark_list=all_contract_all_accumu_return_ratio[benchmark_num]
    del all_contract_all_accumu_return_ratio[benchmark_num]
    for a in range(int(num)):
        for i in range(len(all_contract_all_accumu_return_ratio)):
            ARR_diff.append(all_contract_all_accumu_return_ratio[i][a]-benchmark_list[a])
        contract_ARR_diff_rank=pd.DataFrame({'code':columns_list,'ARR_diff':ARR_diff}).sort_values(by = 'ARR_diff',axis = 0,ascending = False).reset_index().drop(['index'],axis=1)
        all_ARR_diff_rank.append(contract_ARR_diff_rank)
        top_last_20percent_code=judge_top_last_20percent_assest(contract_ARR_diff_rank)
        all_top_last_20percent_code_rank.append(top_last_20percent_code)
        ARR_diff=[]
    del all_top_last_20percent_code_rank[-1]
    return all_top_last_20percent_code_rank, test_time_point, data, all_ARR_diff_rank, statistical_dates


def Base_difference_momentum_implement(startdate, data, test_time_point, test_term, all_top_last_20percent_code_rank, contract_num, money):
    pnl=[money]
    each_last20percent_index_pnl=[]
    all_top_last_20percent_code_rank_and_test_time_point=[all_top_last_20percent_code_rank,test_time_point]
    for i in range(len(all_top_last_20percent_code_rank_and_test_time_point[1])):
        for a in all_top_last_20percent_code_rank[i]['last_20percent_assest']:
            num=pnl[-1]/len(all_top_last_20percent_code_rank[1])/data[a][test_time_point[i]]
            each_last20percent_index_pnl.append((data[a][test_time_point[i]+test_term-1]-data[a][test_time_point[i]])*num*contract_num)
        sum_last20percent_index_pnl=sum(each_last20percent_index_pnl)
        each_last20percent_index_pnl=[]
        pnl.append(pnl[-1]+sum_last20percent_index_pnl)
    right_trade=0
    total_trade=len(pnl)-1
    for i in range(len(pnl)-1):
        if pnl[1+i]>pnl[i]:
            right_trade +=1
    win_ratio=right_trade/total_trade
    return  win_ratio

def show_position_fluctuation(startdate, data, test_time_point, test_term, all_top_last_20percent_code_rank, contract_num, money):
    pnl=[money]
    each_last20percent_index_pnl=[]
    all_top_last_20percent_code_rank_and_test_time_point=[all_top_last_20percent_code_rank,test_time_point]
    for i in range(len(all_top_last_20percent_code_rank_and_test_time_point[1])):
        for b in range(test_time_point[i],test_time_point[i]+test_term-1,1):
            for a in all_top_last_20percent_code_rank[i]['last_20percent_assest']:
                num=pnl[-1]/len(all_top_last_20percent_code_rank[1])/data[a][test_time_point[i]]
                each_last20percent_index_pnl.append((data[a][b+1]-data[a][b])*num*contract_num)
            sum_last20percent_index_pnl=sum(each_last20percent_index_pnl)
            each_last20percent_index_pnl=[]
            pnl.append(pnl[-1]+sum_last20percent_index_pnl)
    trading_dates=[startdate]
    for i in test_time_point:
        for a in range(i+1,i+test_term,1):
            trading_dates.append(data.index[a])
    temp=[]
    ratio=[0]
    pnl_ratio=[]
    for i in range(len(pnl)-1):
        ratio.append(pnl[i+1]/pnl[i]-1)
    for i in range(len(ratio)):
        for a in range(i+1):
            temp.append(ratio[a])
        pnl_ratio.append(sum(temp))
        temp=[]
    pnl_ratio_df=pd.DataFrame({'pnl_ratio':pnl_ratio}, index=trading_dates)
    return pnl_ratio_df


def each_test_term_fluctuation(startdate, data, test_time_point, test_term, all_top_last_20percent_code_rank, contract_num, money):
    pnl=[]
    pnl_ratio=[]
    for i in range(len(test_time_point)):
        pnl.append([money])
        pnl_ratio.append([])
    each_last20percent_index_pnl=[]
    all_top_last_20percent_code_rank_and_test_time_point=[all_top_last_20percent_code_rank,test_time_point]
    for i in range(len(all_top_last_20percent_code_rank_and_test_time_point[1])):
        for b in range(test_time_point[i],test_time_point[i]+test_term-1,1):
            for a in all_top_last_20percent_code_rank[i]['last_20percent_assest']:
                num=pnl[i][-1]/len(all_top_last_20percent_code_rank[1])/data[a][test_time_point[i]]
                each_last20percent_index_pnl.append((data[a][b+1]-data[a][b])*num*contract_num)
            sum_last20percent_index_pnl=sum(each_last20percent_index_pnl)
            each_last20percent_index_pnl=[]
            pnl[i].append(pnl[i][-1]+sum_last20percent_index_pnl)
    for i in range(len(pnl)):
        temp=[]
        ratio=[0]
        for b in range(len(pnl[i])-1):
            ratio.append(pnl[i][b+1]/pnl[i][b]-1)
        for b in range(len(ratio)):
            for a in range(b+1):
                temp.append(ratio[a])
            pnl_ratio[i].append(sum(temp))
            temp=[]
        ratio=[0]
    trading_dates=[startdate]
    for i in test_time_point:
        for a in range(i+1,i+test_term,1):
            trading_dates.append(data.index[a])
    pnl_ratio_df=[]
    for i in range(len(pnl_ratio)):
        pnl_ratio_df.append(pd.DataFrame({'pnl_ratio':pnl_ratio[i]}))
    return pnl_ratio_df, trading_dates
        

















































#    trading_dates=[startdate]
#    for i in test_time_point:
#        trading_dates.append(data.index[i+test_term-1])
#    temp=[]
#    ratio=[0]
#    pnl_ratio=[]
#    for i in range(len(pnl)-1):
#        ratio.append(pnl[i+1]/pnl[i]-1)
#    for i in range(len(ratio)):
#        for a in range(i+1):
#            temp.append(ratio[a])
#        pnl_ratio.append(sum(temp))
#        temp=[]
#    pnl_ratio_df=pd.DataFrame({'pnl_ratio':pnl_ratio}, index=trading_dates)















