#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# import reqiuired packages
# conda install -c conda-forge geopandas
from datetime import datetime

import pandas as pd

import matplotlib as plt
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
from shapely.geometry import Point, Polygon
from collections import Counter
import seaborn as sns
pd.set_option('display.max_rows', 5)
pd.set_option('display.max_columns', 5)
pd.set_option('display.width', 5)


# In[ ]:


# read the dataset
df = pd.read_excel('ANZdataset.xlsx')


# In[ ]:


# let's check the dataset 
df.head()


# In[ ]:


# how many rows and columns do we have
df.shape


# In[ ]:


# what are the column names
df.info()


# In[ ]:


df['status'].value_counts()


# In[ ]:


df['merchant_suburb'].value_counts()


# In[ ]:


len(df['merchant_suburb'].unique())


# In[ ]:


for i in range(len(df)):
    df['merchant_suburb'][i] = str(df['merchant_suburb'][i]).capitalize()


# In[ ]:



df['card_present_flag'].value_counts()


# In[ ]:


df['bpay_biller_code'].value_counts()


# In[ ]:


df.duplicated().sum()


# In[ ]:


# account numbers
df['account'].value_counts()


# In[ ]:


df['first_name'].value_counts()


# In[ ]:


df['long_lat'].value_counts()


# In[ ]:


df['txn_description'].unique()


# In[ ]:


df['merchant_code'].value_counts()


# In[ ]:


df['extraction'].value_counts()


# In[ ]:


df['movement'].value_counts()


# In[ ]:


df.describe()


# In[ ]:


print('Mean age is ' + str(df['age'].mean()))
print('median age is ' + str(df['age'].median()))
print('standard deviation for age is ' + str(df['age'].std()))


# In[ ]:


plt.hist(df['age'])
plt.xlabel('age')
plt.ylabel('count')
plt.title('Age')
plt.show()

plt.hist(df['balance'])
plt.xlabel('balance')
plt.ylabel('count')
plt.title('balance')
plt.show()

plt.hist(df['amount'])
plt.xlabel('amount')
plt.ylabel('count')
plt.title('amount')
plt.show()


# In[ ]:


df.isnull().sum()


# In[ ]:


df.notnull().sum()


# In[ ]:


df.head()


# In[ ]:


df.groupby('gender')['age', 'amount', 'balance'].mean()


# In[ ]:


df.groupby(['merchant_state'])['age', 'amount', 'balance'].mean()


# In[ ]:


df.groupby(['txn_description'])['age', 'amount', 'balance'].mean()


# In[ ]:


df[['age', 'amount', 'balance']].corr()


# In[ ]:


df.boxplot('age')


# In[ ]:


df.boxplot('amount')


# In[ ]:


df.boxplot('balance')


# In[ ]:


# Following two code blocks are for removing the outliers. However, it may not be convinient 
#to remove outliers at this point
'''def remove_outlier(col):
    sorted(col)
    q1, q3 = col.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower_range = q1 - (1.5 * iqr)
    upper_range = q3 + (1.5 * iqr)
    return lower_range, upper_range'''


# In[ ]:


'''low_age, high_age = remove_outlier(df['age'])
df['age'] = np.where(df['age'] > high_age, high_age, df['age'])
df['age'] = np.where(df['age'] < low_age, low_age, df['age'])'''


# In[ ]:


'''df.boxplot('age')'''


# In[ ]:


'''low_amount, high_amount = remove_outlier(df['amount'])
df['amount'] = np.where(df['amount'] > high_amount, high_amount, df['amount'])
df['amount'] = np.where(df['amount'] < low_amount, low_amount, df['amount'])'''


# In[ ]:


'''df.boxplot('amount')'''


# In[ ]:


'''low_balance, high_balance = remove_outlier(df['balance'])
df['balance'] = np.where(df['balance'] > high_balance, high_balance, df['balance'])
df['balance'] = np.where(df['balance'] < low_balance, low_balance, df['balance'])'''


# In[ ]:


'''df.boxplot('balance')'''


# In[ ]:


'''plt.hist(df['age'])
plt.xlabel('age')
plt.ylabel('count')
plt.title('Age')
plt.show()

plt.hist(df['balance'])
plt.xlabel('balance')
plt.ylabel('count')
plt.title('balance')
plt.show()

plt.hist(df['amount'])
plt.xlabel('amount')
plt.ylabel('count')
plt.title('amount')
plt.show()'''


# In[ ]:


plt.scatter(df['amount'], df['balance'])
plt.show()


# In[ ]:


df.groupby('first_name')['age', 'amount', 'balance'].mean()


# In[ ]:


df.insert(12, 'time_in_day', 0)
df.insert(12, 'time', 0)


# In[ ]:



for i in range(len(df)) :
    df['time'][i] = df['extraction'][i][:19]
    
#for i in bad_chars :
#    test_string = test_string.replace(i, '')


# In[ ]:


for i in range(len(df)):
    df['time'][i] = datetime.datetime.strptime(str(df['time'][i]), '%Y-%m-%dt%H:%M:%S')


# In[ ]:


'''for i in range(len(df)):
    df.groupby(df['time'][i].hour).value_col.sum()'''

df.resample('d', on='time').amount.sum()


# In[ ]:





# In[ ]:


for i in range(len(df)):
    if 3 <= df['time'][i].hour <= 5:
        df['time_in_day'][i] = 'Early morning'
    if 5 < df['time'][i].hour < 11:
        df['time_in_day'][i] = 'Morning'
    if 11 <= df['time'][i].hour <= 15: 
        df['time_in_day'][i] = 'Around noon'
    if 15 < df['time'][i].hour < 18:
        df['time_in_day'][i] = 'Afternoon'
    if 18 <= df['time'][i].hour <= 22: 
        df['time_in_day'][i] = 'Evening'     
    if 22 < df['time'][i].hour:
        df['time_in_day'][i] = 'Night'
    if df['time'][i].hour <= 3:
        df['time_in_day'][i] = 'Late night'


# In[ ]:


df.groupby('time_in_day')['age'].median()


# In[ ]:


df.groupby('time_in_day')['age'].mean()


# In[ ]:


k =pd.DataFrame(df.groupby('time_in_day')['amount'].sum())
k['time'] = k.index
k.amount


# In[ ]:


order = ["Early morning", "Morning", "Around noon", "Afternoon", "Evening", "Night", "Late night"]
plt.figure(figsize=(8,5))
ax = sns.barplot(x="time", y="amount", data=k, estimator=sum, order = order)
plt.xlabel("Time in day")
plt.ylabel("Amount")
plt.title('Payments made during the day')
plt.show()


# In[ ]:


df.merchant_long_lat.fillna(df.long_lat, inplace=True)
    
'''    df['merchant_long_lat'][i] = df['merchant_long_lat'][i].replace(np.nan, str(df['long_lat'][i]))

    if df['merchant_long_lat'][i] == np.nan:
        df['merchant_long_lat'][i] = df['long_lat'][i]'''


# In[ ]:


df.head(-60)


# In[ ]:


df.insert(25, 'day', 0)
df.insert(26, 'month', 'jan')


# In[ ]:


for i in range(len(df)): 
    df['day'][i] = df['time'][i].day
    df['month'][i] = df['time'][i].month


# In[ ]:


for i in range(len(df)):
    if df['month'][i] == 8:
        df['month'][i] = 'August'
    if df['month'][i] == 9:
        df['month'][i] = 'September'
    if df['month'][i] == 10:
        df['month'][i] = 'October'


# In[ ]:


plt.figure(figsize=(3,5))
ax.set(xlabel='common xlabel', ylabel='common ylabel')
ax = sns.catplot(kind='bar', x='month', y='amount', hue='day', data=df, color='b', legend=False, height=5, aspect=30/12)
plt.xlabel("")
plt.ylabel("Amount")
plt.title('Payments made throughout months')
plt.show()


# In[ ]:


df.insert(23, 'longitude', 0)
df.insert(24, 'latitude', 0)
df.insert(26, 'geometry', 0)


# In[ ]:


for i in range(12043):
    df['longitude'][i] = float(str(df['merchant_long_lat'][i]).split(' ')[0])
    df['latitude'][i] = float(str(df['merchant_long_lat'][i]).split(' ')[1])


# In[ ]:


str(df['merchant_long_lat'][120]).split(' ')


# In[ ]:


streetmap = gpd.read_file('shapefile/AUS_2016_AUST.shp')


# In[ ]:


crs = {'init': 'epsg:4326'}


# In[ ]:


counts = Counter(df.merchant_suburb)
k = df[df.merchant_suburb.isin([key for key in counts if counts[key] > 60])]


# In[ ]:


k['geometry'] = [Point(xy) for xy in zip(k['longitude'], k['latitude'])]


# In[ ]:


geo_df = gpd.GeoDataFrame(k, crs = crs, geometry = k['geometry'])


# In[ ]:


len(k)


# In[ ]:




fig,ax = plt.subplots(figsize = (15,15))
streetmap.plot(ax = ax, alpha = 0.4, color = 'grey')
'''geo_df[geo_df['merchant_suburb'] == 'Sydney'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Sydney']['amount'].sum(), marker = 'o', label = 'Sydney')
geo_df[geo_df['merchant_suburb'] == 'Southport'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Southport']['amount'].sum(), marker = 'o', label = 'SPort')
geo_df[geo_df['merchant_suburb'] == 'Gladesville'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Gladesville']['amount'].sum(), marker = 'o', label = 'Pentapin')
geo_df[geo_df['merchant_suburb'] == 'Melbourne'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Melbourne']['amount'].sum(), marker = 'o', label = 'Melbourne')
geo_df[geo_df['merchant_suburb'] == 'Perth'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Perth']['amount'].sum(), marker = 'o', label = 'Perth')
geo_df[geo_df['merchant_suburb'] == 'West Wodonga'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'West Wodonga']['amount'].sum(), marker = 'o', label = 'West Wodonga')
geo_df[geo_df['merchant_suburb'] == 'Canberra'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Canberra']['amount'].sum(),  marker = 'o', label = 'Canberra')
geo_df[geo_df['merchant_suburb'] == 'Brisbane'].plot(ax = ax, alpha=0.1, markersize = df[df['merchant_suburb'] == 'Brisbane']['amount'].sum(), marker = 'o', label = 'Brisbane')
'''
for i in geo_df['merchant_suburb']:
    geo_df[geo_df['merchant_suburb'] == i].plot(ax = ax, markersize = k[k['merchant_suburb'] == i]['amount'].sum(), marker = 'o', label = i)


#plt.legend(prop={'size': 10})
plt.show()


# In[2]:


import jupyterresourceusage


# In[ ]:




