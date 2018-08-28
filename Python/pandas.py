# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:11:34 2016

@author: ebm94
"""

import pandas as pd
import os
os.chdir('/home/fractaluser/Downloads/Python Scripts')
os.getcwd()

trx_data = pd.read_csv('trx_data.csv')

a = trx_data.head()

trx_data.describe()
trx_data.dtypes
trx_data.shape # gives the no. of rows and columns in pandas dataframe
len(trx_data.index) # gives the no. of rows by counting indices

#how many no. of customers are present in my dataset?
total_customers = trx_data['customer_id'].nunique()

#what are the net sales?
total_sales = trx_data['net_amount'].sum()
check_sum = trx_data[['net_amount','discount_amount','gross_amount']].sum() # Sum of these 3 columns given as a list

#histogram of net sales with a condition on the same
trx_data['net_amount'][(trx_data['net_amount'] > 0) & (trx_data['net_amount'] < 100)].hist(bins = 500)

#who bought the costliest item?
trx_data[['customer_id','unit_sales_price']][trx_data['unit_sales_price'] ==  trx_data['unit_sales_price'].max()]

#what was the most expensive item bought?
# unique() and nunique() attribute does not work for dataframe; works for numpy.ndarray
# shows only the unique values in the ndarray
trx_data['sku_id'][trx_data['unit_sales_price'] == trx_data['unit_sales_price'].max()].unique()

#most expensive and cheapest skus
sku_prices = trx_data[['sku_id','unit_sales_price']][(trx_data['unit_sales_price'] == trx_data['unit_sales_price'].max()) | (trx_data['unit_sales_price'] == trx_data['unit_sales_price'].min())]
trx_data['sku_id'][(trx_data['unit_sales_price'] == trx_data['unit_sales_price'].max()) | (trx_data['unit_sales_price'] == trx_data['unit_sales_price'].min())].unique()



#remove duplicate product prices
#drop_duplicates works only for dataframes and NOT FOR NDARRAYS
# Ndarray: N-dimensional array of items of same type
#Tuple: immutable Python objects; However, you can concatentate tuples using + sign
# Lists: mutable Python objects
sku_prices = sku_prices.drop_duplicates()

#load the product_master dataset
product_master = pd.read_csv('product_master.csv')

sample_df = product_master.head()

#merge trx_data with product_master 
# List specifies the columns of the dataset you want to merge with
merged_df = trx_data.merge(product_master[['sku_id','sku_desc','cat_desc']], on = 'sku_id', how = 'left')

#again, determine the most expensive and cheapest skus along with their sku_descriptions
sku_prices = merged_df[['sku_id','unit_sales_price','sku_desc','cat_desc']][(merged_df['unit_sales_price'] == merged_df['unit_sales_price'].max()) | (merged_df['unit_sales_price'] == merged_df['unit_sales_price'].min())]
#remove duplicate product prices
sku_prices = sku_prices.drop_duplicates()

#how many months worth of data are we dealing with?
# Converting the datatype of the column
trx_data['transaction_timestamp'] = pd.to_datetime(trx_data['transaction_timestamp'])

#datatype changed from object to datetime
min_date = trx_data['transaction_timestamp'].min()
max_date = trx_data['transaction_timestamp'].max()

#extract the date from our datetime column and store it in a new column
# Creating a UDF
trx_data['Date'] = trx_data['transaction_timestamp'].apply(lambda x: x.date())

trx_data[['transaction_timestamp','Date']].head()

# Method 1: Drop a column for all the rows in trx_data
trx_data = trx_data.drop('transaction_timestamp',axis = 1)
# axis=1 indicates along columns (for every row), axis=0 is along rows (default). Rows are called index in pandas

# Method 2: To delete a column
del trx_data['Date']

# create a yearmonth identifier in our trx data
trx_data['YearMonth'] = trx_data['transaction_timestamp'].apply(lambda x: x.year*100 + x.month)
temp_df = trx_data[['transaction_timestamp','YearMonth']].head()

#missing value treatment
trx_data['promo_id'][trx_data['promo_id'].isnull()] = 'Not on offer'

#determine net monthly spend per customer
net_spend = trx_data.groupby(['customer_id','YearMonth']).agg({'net_amount':['sum','max']}).reset_index().sort('customer_id',ascending = False)
#apply own functions to columns using agg function
# groupby() with circle brackets

#Changing names of columns in a DataFrame
net_spend.columns = ['CustomerID','YearMonth','Total_Spend','Highest_Spend']



#how many months of data are we really dealing with?
trx_data['YearMonth'].unique()
 
#pivot the dataset on Yearmonth
pivoted_trx = pd.pivot_table(net_spend, cols = 'YearMonth', rows = 'CustomerID',values = 'Total_Spend', fill_value = 0).reset_index()
#In a different version, rows becomes index and cols becomes columns

#unpivot the above table
unpivoted_trx = pd.melt(pivoted_trx,id_vars = 'CustomerID',var_name = 'YearMonth',value_name = 'Total_Spend')
# id_vars for rows, var_name for columns, value_name for values in a Pivot Table

# Not needed to import this module
# import matplotlib.pyplot as plt

#bar plot of the total sales in jan 2010 and 2011; wont work
trx_data.plot(x = 'YearMonth',y= 'net_amount', kind = 'bar')


#roll up the data and plot total sales in jan2010 and 2011

trx_data.groupby('YearMonth').agg({'net_amount':'sum'}).reset_index().plot('YearMonth','net_amount',kind = 'bar')
# .plot used to plot a dataframe



########### TRIALS ###########
df = pd.DataFrame({'year':[2000, 2001], 'val':[20, 30]})    
df
df.plot('year', 'val',kind = 'bar')
trx_data.head()
trx_data.plot()

# Series (MUTABLE): a list of values of any mix type and default integer index
# Series takes input in the form of lists as well as dictionaries (keys are indices and values are part of column)
# To check whether an object is in a series, use.......... print 'index#' in SeriesName
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
a=(ts<1) #Returns a series of True and False with dates as indices
ts = ts.cumsum()

ts.plot()

########### TRIALS 2 ###########
s=pd.Series([1,2,3,np.nan,6,8])
s

dates=pd.date_range('20130101', periods=6)
dates
# A series is produced

df=pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
df
df.A # To access column A
# Date time index implies time series
# A column of dataframe is defined as a series
# Dataframes are made up of Series
# Matrices are made up of lists