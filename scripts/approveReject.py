
import data_generator as dg
import pyqrcode  
from pyqrcode import QRCode 
import cv2
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
import random
import pickle
import png
from thresholder import find_threshold
import dataloader as dl
import os

global threshold

def generatePlot(dict_requests):
    
  time_intervals = list(dict_requests.keys())
  no_people  = list(dict_requests.values())
  plt.bar(time_intervals,no_people,width=0.5,align='center',label='No_of_People')
  plt.xlabel('Time Interval Spanning from 00:00 - 23:30')
  plt.ylabel('No of people in the Office')
  plt.legend()
  plt.grid()
  plt.xticks(time_intervals, rotation='vertical', size=8)
  plt.show()


def generateQRCode(start_time,end_time,location,no_of_employees,fol_name,mail_id = 'das968@nyu.edu'):
  # String which represent the QR code 
  s = f'Start Time:{start_time} End Time: {end_time} Location : {location} People: {no_of_employees}'

  # Generate QR code 
  url = pyqrcode.create(s) 

  #print('Generated')
  # Create and save the png file naming "myqr.png"
  path = os.path.join(os.getcwd(),fol_name)
  png_path = os.path.join(path,f'{mail_id}.png')
  url.png(png_path, scale = 6) 

  #Read image from the file and send it to the respective requestor
  img = cv2.imread(png_path)
  plt.imshow(img)



def approveReject(request_sheet,finding = 'overall'):


  #Getting the threshold for given location

  if(finding == 'overall'):
    threshold = find_threshold(40.715,-74.014,1,0)
  else:
    threshold = find_threshold(40.715,-74.014,2,1)
  
  dict_requests = {}
  approval_dict = {}
  time_slots = dg.generateTimeKeys()
  dict_requests = {i:0 for i in time_slots}
  count_true = 0

  for k,v in request_sheet.items():

    start_time = v['start_time']
    end_time = v['end_time']  
    people = v['people']
    location = str(v['lat'])+' '+str(v['long'])

    dt_time = datetime.datetime.now() + datetime.timedelta(days=1)
    s = str(dt_time.year) + '-' + str(dt_time.month) + '-' + str(dt_time.day) + ' 00:00:00'
    timestamp_tomorrow = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())

    hour,minutes = end_time.split(':')[0],end_time.split(':')[1]

    if(len(hour) == 1):
      hour = '0'+str(hour)
      end_time = hour+':'+minutes

    s_idx = time_slots.index(start_time)
    e_idx = time_slots.index(end_time)

    allSlots = []
    allSlots = time_slots[s_idx:e_idx+1]

    not_statisfied = 0
    

    for key_ in allSlots:
      if not (dict_requests[key_] + people <= threshold):
        not_statisfied = 1
        break
    
    if(not_statisfied == 0):
      for key_ in allSlots:
        dict_requests[key_] += people
        
      #generateQRCode(start_time,end_time,location,people,fol_name = 'qrCode')
      count_true +=1
      approval_dict[k] = v
    else:
      not_statisfied = 0

  with open('scheduler.p','wb') as f:
      pickle.dump(dict_requests,f,protocol=pickle.HIGHEST_PROTOCOL)


  with open('approved_requets.p', 'wb') as fp:
    pickle.dump(approval_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)
    
  print(f'Percentage of approved requests',count_true/len(request_sheet)*100,'%')
  generatePlot(dict_requests)

  return threshold


##with open('requests_sheet.p', 'rb') as fp:
##  request_sheet_sorted = pickle.load(fp)
##
##with open('optimized_request_sheet.p', 'rb') as f:
##  req_sheet = pickle.load(f)
##
##print('Approved Request')
##approveReject(request_sheet_sorted)
##approveReject(req_sheet)
##  

