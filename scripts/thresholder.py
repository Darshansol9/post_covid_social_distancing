import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import itertools
from dataloader import round_lat_long, data_loader
from plotter import plotter

def create_thresholds():
  
  df_manhattan = data_loader()
  print(df_manhattan.columns)
  df_total_avg = df_manhattan[['dropoff_latitude','dropoff_longitude','passenger_count']].groupby(['dropoff_longitude','dropoff_latitude'],as_index=False).sum()
  df_total_avg['passenger_count']/=90
  df_total_avg.to_csv('threshold_overall.csv',index=False)
  
  df_day_avg = df_manhattan[['dropoff_latitude','dropoff_longitude','passenger_count','week_day']].groupby(['dropoff_longitude','dropoff_latitude','week_day'],as_index=False).sum()
  df_day_avg['passenger_count']/=12
  df_day_avg.to_csv('threshold_day_avg.csv',index=False)
  
  choice = input('Do you want to create plots.Enter y/n ')
  if choice =='y':
    lat,lon = [round(float(i),3) for i in (input('Enter latitude,longitude (separate by comma or enter 0,0 for Goldmna Sachs) ')).split(',')]
    if lat==0 and lon==0:
      plotter(df_manhattan)
    else:
      plotter(df_manhattan,lat,lon)
  
  files.download('threshold_day_avg.csv')
  files.download('threshold_overall.csv')
  
  print('Data Load Succesfull')
  return('Data Load successful')

def find_threshold(lat,lon,mode=1,day=0):

  #print('Entered')
  
  if mode == 1:
    df=pd.read_csv('threshold_overall.csv')
    df = df[(df['dropoff_latitude']==lat)]
    df = df[(df['dropoff_longitude']==lon)]
    df = df['passenger_count']/2
    
    return df.values[0]

  if mode == 2:
    df = pd.read_csv('threshold_day_avg.csv')
    df = df[(df['dropoff_latitude']==lat)]
    df = df[(df['dropoff_longitude']==lon)]
    df = df[(df['week_day']==day)]
    df = df['passenger_count']/2
    
    return df.values[0]
    
#status = create_thresholds()
