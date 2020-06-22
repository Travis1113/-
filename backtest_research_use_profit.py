import numpy as np
import pandas as pd

class back_cal_use_profit():
    def __init__(self,list0,rf,annualization_factor):
        self.list0 = list0
        self.rf = rf
        self.annualization_factor = annualization_factor

    def drawdown(self):
        dic = {i: self.list0[i] for i in range(len(self.list0))}
        max_value = -1
        for i_draw in range(len(self.list0)):
            for i_draw1 in range(len(self.list0)):
                if (i_draw < i_draw1) and ((dic[i_draw] - dic[i_draw1])/(1+dic[i_draw]) > max_value):
                    max_value = (dic[i_draw] - dic[i_draw1])/(1+dic[i_draw])
        return max_value

    def highestvalue(self):
        value_high = max(self.list0)
        return value_high

    def lowestvalue(self):
        value_low = min(self.list0)
        return value_low

    def profit_end(self):
        profit = self.list0[-1]
        return profit

    def sharperatio(self):
        list0 = self.list0
        list1 = []
        for i in range(len(list0)):
            if i < (len(list0)-1):
                try:
                    list1.append(((1+list0[i+1])/(1+list0[i]))-1)
                except:
                    list1.append(0)
        # print(np.mean(list1))
        # print(np.std(list1))
        sharpe = (np.mean(list1) - ((1+self.rf)**(1/self.annualization_factor)-1)) / np.std(list1, ddof=1)*((self.annualization_factor)**0.5)
        return sharpe

    def sortino(self):
        list_source = self.list0
        list0 = []
        for i in range(len(list_source)):
            if i < (len(list_source)-1):
                try:
                    list0.append(((1+list_source[i+1])/(1+list_source[i]))-1)
                except:
                    list0.append(0)
        df0 = pd.DataFrame({'profit':list0})
        list_profit_mean = []
        for i in range(len(list0)):
            list_profit_mean.append(np.mean(list0[:(i+1)]))
        df0.insert(1,'profit_mean',list_profit_mean)
        df0['f'] = df0.apply(lambda x:0 if x['profit'] >= x['profit_mean'] else 1,axis=1)
        df0['cal'] = df0.apply(lambda x:((x['profit']-x['profit_mean'])**2)*x['f'],axis=1)
        value_mean = np.mean(df0['cal'].tolist())
        # print('value_mean',value_mean)
        dside_risk = np.sqrt(value_mean) * np.sqrt(self.annualization_factor)
        # print('dside_risk',dside_risk)
        value_sortino = (np.mean(list0) - ((1+self.rf)**(1/self.annualization_factor)-1)) / dside_risk * self.annualization_factor
        return dside_risk,value_sortino

    def profit_year(self):
        profit1 = (1+self.list0[-1])**(self.annualization_factor/len(self.list0)) - 1
        profit2 = profit1/12
        return profit1,profit2

    def vol(self):
        list0 = self.list0
        list1 = []
        for i in range(len(list0)):
            if i < (len(list0)-1):
                try:
                    list1.append(((1+list0[i+1])/(1+list0[i]))-1)
                except:
                    list1.append(0)
        value_profit_mean = np.mean(list1)
        list2 = list(map(lambda x:((x-value_profit_mean)**2),list1))
        value_vol = (np.sum(list2)*(self.annualization_factor/(len(list2)-1)))**0.5
        return value_vol


    def research_main(self):
        value_drawdown = self.drawdown()
        value_highestvalue = self.highestvalue()
        value_profit = self.profit_end()
        value_sharpe = self.sharperatio()
        value_lowestvalue = self.lowestvalue()
        profit_year,profit_month = self.profit_year()
        dside_risk,value_sortino = self.sortino()
        value_vol = self.vol()
        return value_drawdown, value_highestvalue, value_profit, value_sharpe ,value_lowestvalue,profit_year,profit_month,dside_risk,value_sortino,value_vol

if __name__ == '__main__':
    f = open("E:\基金回测\估值/value2/result\分析/jicha.csv")
    df0 = pd.read_csv(f)
    list0 = df0['cum_rate'].tolist()
    back_test = back_cal_use_profit(list0,0.015,19/8)
    value_drawdown, value_highestvalue, value_profit, value_sharpe, value_lowestvalue, profit_year, profit_month, dside_risk, value_sortino, value_vol = back_test.research_main()
    print(value_drawdown, value_highestvalue, value_profit, value_sharpe ,value_lowestvalue,profit_year,profit_month,dside_risk,value_sortino,value_vol)
    # back_test = back_cal_use_profit([0,1,1,1,1], 0, 250)
    # print(back_test.sharperatio())
    # print(dside_risk)