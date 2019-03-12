import pandas as pd
import seaborn; seaborn.set()
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import statsmodels.stats.proportion as sm
import math
import datetime
from datetime import timedelta


data = pd.read_csv('transactions_dataset.csv')
data['order_date'] = pd.to_datetime(data['order_date'])
data.index = data['order_date']


def graph(timeseries,w, title, ylabel):
    """
    Histogram of a time series
        """
    fig, ax = plt.subplots()
    ax.bar(timeseries.index, timeseries, w)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Order date')
    ax.set_title(title)
    plt.show()


def tts(ds):

    perday = ds['order_id'].resample('D').count()
    perhour = ds['order_id'].resample('H').count()
    perweek = ds['order_id'].resample('W').count()
    print('Average orders number placed per week:', perweek.mean(), 'Average orders number placed per day:',
    perday.mean(), 'Average orders number placed per hour:', perhour.mean())
    graph(perweek, 4, 'Orders per week', 'Number of orders')
    graph(perday, 0.5, 'Orders per day', 'Number of orders')
    graph(perhour, 0.1, 'Orders per hour', 'Number of orders')


def season(data):

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    week_data = data['order_id'].groupby(data['order_date'].dt.weekday_name).count().reindex(days)
    days1 = ['Mon','Tue','Wed','Th','Fri','Sat', 'Sun']
    fig, ax = plt.subplots()
    ax.bar(days1, week_data)
    ax.set_ylabel('Number of orders')
    ax.set_title('Orders per day of the week')
    plt.show()
    hourly_data = data['order_id'].groupby(data['order_date'].dt.hour).count()
    graph(hourly_data, 0.35, 'Orders per day hour', 'Number of orders')


def cancel(data):

    p=data['is_canceled'].mean()
    n=len(data['is_canceled'])
    print(p)
    print(math.sqrt(p*(1-p)/n))
    print(sm.proportion_confint(data['is_canceled'].sum(), n))
    dcancel=data[['number_of_paid_orders_before', 'is_canceled']].query('number_of_paid_orders_before <=10')
    dcancel['is_canceled'].groupby(dcancel['number_of_paid_orders_before']).mean().plot(kind='bar', title='Cancel rate')
    plt.show()
    graph(data['is_canceled'].resample('M').mean(),10,'Cancel rate per month', 'Cancel rate')


def dtc(data):

    dtset=data[data.duplicated(subset=['customer_id'], keep=False)]
    print('No return:',1-len(dtset)/len(data['is_canceled']))
    dt=dtset.groupby('customer_id').order_date.apply(lambda x: (x-x.min()).astype('m8[D]').mean()).reset_index()
    print('Mean of dt:',dt['order_date'].mean())
    ax = dt['order_date'].plot(kind='hist', title='Avg time between orders')
    ax.set(ylabel="Number of customers", xlabel="Days")
    plt.show()
    p = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 96.0, 99.0])
    for a in p:
        print(a,'%:', np.percentile(dt['order_date'], a))
    dtmulti=dtset.groupby('customer_id').order_date.apply(lambda x: (x-x.min()).astype('m8[h]')[(x-x.min()).astype('m8[h]')!=0]
                                                      .min()).reset_index()
    dtmulti['order_date'].fillna(0,inplace= True)
    print(dtmulti.loc[dtmulti['order_date']<=1])


def retention(data):

    data_copy = data.copy(deep=False)
    data_copy['order_date'] = pd.to_datetime(data_copy['order_date'])
    data.index = data['order_date']
    data_copy.index = data_copy['order_id']
    data['is_returned'] = ""
    pd.options.mode.chained_assignment = None
    for a in data_copy.index:
        b = data_copy['order_date'][a]
        date_mask = (data.index > b) & (data.index <= b + timedelta(days=60))
        s = data.loc[date_mask]['customer_id']
        val = data_copy['customer_id'][a]
        if val in s.unique():
            data['is_returned'][b] = 1
        else:
            data['is_returned'][b] = 0
    data['is_returned'] = pd.to_numeric(data['is_returned'])
    d = datetime.datetime(2016, 4, 30)
    data_ret = data[data.index < d]
    dretention = data_ret[['number_of_paid_orders_before', 'is_returned']].query('number_of_paid_orders_before <=5')
    dretention['is_returned'].groupby(dretention['number_of_paid_orders_before']).mean().plot(kind='bar',
                                                                                              title='Return rate')
    plt.show()
    n1 = len(data_ret.loc[data_ret['is_canceled'] == 1])
    n2 = len(data_ret.loc[data_ret['is_canceled'] == 0])
    p1 = data_ret.loc[data_ret['is_canceled'] == 1]['is_returned'].mean()
    p2 = data_ret.loc[data_ret['is_canceled'] == 0]['is_returned'].mean()
    print(p1, p2)
    print('confidence interval: delta+-=',
          p2 - p1 - sc.stats.norm.ppf(1 - 0.05) * math.sqrt((1 - p1) * p1 / (n1 * n1) + (1 - p2) * p2 / (n2 * n2)),
          p2 - p1 + sc.stats.norm.ppf(1 - 0.05) * math.sqrt((1 - p1) * p1 / (n1 * n1) + (1 - p2) * p2 / (n2 * n2)))


tts(data)
season(data)
cancel(data)
dtc(data)
retention(data)









