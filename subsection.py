# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:13:57 2018

@author: chenxi
"""

# -*- coding:'utf-8' -*-

import pandas as pd

# SELECT DATA

df = pd.read_csv(r'146987data.csv',encoding='gbk')

df1 = df[['门店编号','兑券日期','POS机号','流水号','销售额','兑券数']]

df1['门店编号-兑券日期-POS机号-流水号'] =df1['门店编号'].astype(str) + '_'+ df1['兑券日期'].astype(str)+ '_' + df1['POS机号'].astype(str) + '_' + df1['流水号'].astype(str)

df1.drop(['门店编号','兑券日期','POS机号','流水号'], axis=1, inplace=True)

# GROUPBY

df2 = df1.groupby(['门店编号-兑券日期-POS机号-流水号'])[['销售额']].sum()

df3 = df1.groupby(['门店编号-兑券日期-POS机号-流水号'])[['兑券数']].count()
df3.rename(columns={'兑券数':'购买的商品数量'}, inplace = True)

df_sales_count = df2.join(df3)

# SUBSECTION

subsection = []
for i in range(int(round(max(df2['销售额'])/20)-3)):
    temp = len(df2[((68+i*20)<=df2['销售额']) & (df2['销售额']<(68+(i+1)*20))])    
    subsection.append(temp)
    
salesTitles = []
for i in range(int(round(max(df2['销售额'])/20)-3)):
    temp = str(68+i*20)+ '<= 销售额< ' + str(68+(i+1)*20)    
    salesTitles.append(temp)
    
df_sales = pd.DataFrame()  
df_sales['销售额'] = salesTitles
df_sales['数量'] = subsection

#OUTPUT 

excelfilename = "20180622AnalysisData68_16new.xlsx"
writer = pd.ExcelWriter(excelfilename) 
df_sales_count.to_excel(writer, 'Coupon_Sales')
df_sales.to_excel(writer, 'Sales_Subsection')

writer.save()