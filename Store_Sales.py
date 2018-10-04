# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:10:54 2018

@author: chenxi
"""
import pandas as pd

# SELECT DATA

df = pd.read_csv(r'146987data.csv',encoding='gbk')

# GROUPBY & PIVOT

df_dateSales = df.groupby(['门店名称','兑券日期'])[['销售额']].sum()

df_DateSales = df_dateSales.pivot_table(index='门店名称',columns='兑券日期')

df_DateSales.fillna(0,inplace=True)

df_DateSales['SUM'] = df_DateSales['销售额'].iloc[:,0] + df_DateSales['销售额'].iloc[:,1]

# STORE_COUPON INFORMATION

df1 = df[['门店编号','兑券日期','POS机号','流水号','销售额','兑券数','门店名称']]
df1['门店编号-兑券日期-POS机号-流水号'] =df1['门店编号'].astype(str) + '_'+ df1['兑券日期'].astype(str)+ '_' + df1['POS机号'].astype(str) + '_' + df1['流水号'].astype(str)
df1.drop(['门店编号','兑券日期','POS机号','流水号'], axis=1, inplace=True)

df_drop = df1.drop_duplicates(['门店编号-兑券日期-POS机号-流水号']) 
sum_coupon =df_drop['门店编号-兑券日期-POS机号-流水号'].groupby(df1['门店名称']).count()
df_sumCoupon = pd.DataFrame(sum_coupon)

# JOIN TWO TABLE

df_StoreSales = df_DateSales.join(df_sumCoupon)

#OUTPUT 

excelfilename = "20180622AnalysisData_StoreSales.xlsx"
writer = pd.ExcelWriter(excelfilename) 
df_StoreSales.to_excel(writer, 'Store_Sales')

writer.save()