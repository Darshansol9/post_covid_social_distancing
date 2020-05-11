#Plotter.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import itertools
from dataloader import round_lat_long, data_loader

def plotter(df_manhattan,latitude = 40.715,longitude = -74.014):
  temp_grouped = df_manhattan[['drop_date','dropoff_longitude','dropoff_latitude']].groupby(['dropoff_latitude','dropoff_longitude'],as_index=False).count()

  temp_grouped1 = temp_grouped[temp_grouped['drop_date']>500]
  cut_labels = [500,1000,3000,5000,7000,9000,11500]
  cut_bins = [0,500,1000,3000,5000,7000,9000,11532]
  temp_grouped1['date_bin'] = pd.cut(temp_grouped1['drop_date'], bins=cut_bins, labels=cut_labels)

  temp_grouped1.plot.scatter(x='dropoff_latitude', y='dropoff_longitude',c='date_bin',colormap='viridis',s=2+temp_grouped1['drop_date']*0.0009)

  df_200 = df_manhattan[(df_manhattan['dropoff_latitude']==latitude) & (df_manhattan['dropoff_longitude']==longitude)] 
  df_200['week_day'] = df_200['dropoff_datetime'].dt.dayofweek
  df_200_day = df_200[df_200['drop_date'] == "2016-05-31"] 
  df_200_day = df_200_day[['drop_time','passenger_count']]
  df_day = df_200_day.groupby('drop_time',as_index=False).sum()

  df_200_weekly = df_200[['passenger_count','week_day']].groupby('week_day',as_index=False).sum()
  df_200_weekly['passenger_count']/=12  #Averaging over 13 weeks i.e 12 count of each day
  plt.figure(figsize=(9,6))
  plt.plot(df_200_weekly['week_day'],df_200_weekly['passenger_count'])
  plt.title('Weekly Plot')
  plt.ylabel('Number of Visitors')
  plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],rotation=45)
  plt.xlabel('Day of Week')

  hour_list = list(np.arange(4,24))
  min_list = [0,30]
  time_list = list(itertools.product(hour_list,min_list))
  time_list = [str(x[0])+':'+str(x[1]) for x in time_list]

  plt.figure(figsize=(16,9))
  plt.plot(df_day['drop_time'].astype(str),df_day['passenger_count'])
  plt.title('Goldman Sachs Office Visitor plot for 2016-05-31')
  plt.ylabel('Number of Visitors')
  plt.xticks(np.arange(len(time_list)), time_list,rotation=45)
  plt.xlabel('Day of Week')

  plt.figure(figsize=(16,9))
  plt.bar(df_day['drop_time'].astype(str),df_day['passenger_count'])
  plt.title('Goldman Sachs Office Visitor plot for 2016-05-31')
  plt.ylabel('Number of Visitors')
  plt.xticks(np.arange(len(time_list)), time_list,rotation=45)
  plt.xlabel('Day of Week')

