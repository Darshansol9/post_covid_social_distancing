#Dataloader.py
import pandas as pd
import numpy as np
import datetime


def round_lat_long(x):
  return x.round(3)

def data_loader():
  url_green_march = "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2016-03.csv"
  url_green_april = "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2016-04.csv"
  url_green_may = "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2016-05.csv"

  url_yellow_march = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2016-03.csv"
  url_yellow_april = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2016-04.csv"
  url_yellow_may = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2016-05.csv"
  
  urls = [url_green_march, url_green_april, url_green_may, url_yellow_march, url_yellow_april, url_yellow_may]

  list_df = []
  for i in range(3):
    df = (pd.read_csv(urls[i]))
    df = df[['Lpep_dropoff_datetime','Dropoff_longitude','Dropoff_latitude','Passenger_count']]
    df.columns = ['dropoff_datetime', 'dropoff_longitude', 'dropoff_latitude','passenger_count']
    list_df.append(df)
    #,names=['dropoff_datetime', 'dropoff_latitude', 'dropoff_longitude', 'passenger_count'],usecols=['tpep_dropoff_datetime','dropoff_latitude','dropoff_longitude','passenger_count']))
  for i in range(3,len(urls)):
    df = (pd.read_csv(urls[i]))
    df = df[['tpep_dropoff_datetime','passenger_count','dropoff_longitude','dropoff_latitude']]
    df.columns = ['dropoff_datetime', 'passenger_count', 'dropoff_longitude', 'dropoff_latitude']
    list_df.append(df)

  df = pd.concat(list_df, ignore_index=True)
  
  df.dropoff_longitude = round_lat_long(df.dropoff_longitude)
  df.dropoff_latitude = round_lat_long(df.dropoff_latitude)

  #Manhattan Lat Long Details
  lats = [40.715574,40.70208,40.804152,40.854020]
  longs = [-73.977809,-74.015058,-73.935101,-73.939040]
  min_lat = round(min(lats),4)
  max_lat = round(max(lats),4)
  min_long = round(min(longs),4)
  max_long = round(max(longs),4)

  df_manhattan = df[df['dropoff_latitude'].between(min_lat,max_lat) & df['dropoff_longitude'].between(min_long,max_long)]
  df_manhattan['dropoff_datetime'] = pd.to_datetime(df_manhattan['dropoff_datetime'])
  df_manhattan['dropoff_datetime'] = df_manhattan.dropoff_datetime.dt.floor('30T')
  df_manhattan['drop_date'] = df_manhattan.dropoff_datetime.dt.date
  df_manhattan['drop_time'] = [datetime.datetime.time(d) for d in df_manhattan['dropoff_datetime']] 
  df_manhattan['drop_date'] = pd.to_datetime(df_manhattan['drop_date'])
  df_manhattan['week_day'] = df_manhattan['dropoff_datetime'].dt.dayofweek
  
  return df_manhattan
