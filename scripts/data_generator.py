import random
import os
import pickle


def generateTimeKeys():
  timings = []
  for i in range(48):
    if(i == 0):
      timings.append('00:00')
    elif(i%2 == 0 and i!= 0):
      hour = i//2
      if(hour <= 9):
        timings.append('0'+str(hour)+':'+'00')
      else:
        timings.append(str(hour)+':'+'00')
    else:
      hour = timings[-1].split(':')[0]
      timings.append(hour+':'+'30')

  return timings


def getClosestTime(time):
  
  tokens = time.split(':')
  hour = tokens[0]
  minutes = int(tokens[1])

  if(minutes > 30):
    minutes = 60
  else:
    if(minutes <= 15):
      minutes = 0
    else:
      minutes = 30

  if(minutes == 0):
    modified_time = hour + ':' + '00'
  elif(minutes == 60):
    modified_time = str(int(hour)+1) + ':' + '00'
  else:
    modified_time = hour + ':' + str(minutes)

  return modified_time


#Mapping of start_time and burst_time to end_time
def convertToMinutes(start_time,burst_time):
    
    hours,minutes = int(start_time.split(':')[0]),int(start_time.split(':')[1])
    total_minutes = minutes + burst_time
    hour, minute = divmod(total_minutes, 60)
    hour += hours 
    if(hour <= 9):
      hour = '0'+str(hour)

    return getClosestTime("%s:%02d" % (hour, minute))

def saveData(requests_sheet,requests_sheet_sorted):
    
    path = os.path.join(os.getcwd(),'requests_sheet.p')
    path_optimized = os.path.join(os.getcwd(),'optimized_request_sheet.p')
        
    with open(path, 'wb') as fp:
        pickle.dump(requests_sheet, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open(path_optimized, 'wb') as f:
        pickle.dump(requests_sheet_sorted, f, protocol=pickle.HIGHEST_PROTOCOL)

def generateData(gen_req):

  requests_sheet = dict()
  requests_sheet_sorted = dict()
  start_times = generateTimeKeys()
  count = 0
  
  while(count < gen_req):

##    lats = [40.715574,40.70208,40.804152,40.854020]
##    longs = [-73.977809,-74.015058,-73.935101,-73.939040]
##    
##    min_lat = round(min(lats),4)
##    max_lat = round(max(lats),4)
##    min_long = round(min(longs),4)
##    max_long = round(max(longs),4)

    #User input is only start_time,location,time_to_be_spent,number_of_people
    burst_times  = [30,45,60,75,90,120,150,180,210,240,260,300,360,385,400]

    number_of_people = [1,1,1,2,3,1,2]
    num_people = number_of_people[random.randint(0,len(number_of_people)-1)]
    burst_idx = random.randint(0,len(burst_times)-1)
    start_idx = random.randint(0,len(start_times)-1)
    req_time = random.randint(0,len(start_times)-1)
    
    #According to the start_time and burst_time is maps the nearest time slot pre-defined in half hour interval
    end_time = convertToMinutes(start_times[start_idx],burst_times[burst_idx])
    
    #Calculates the request is valid or not i.e if the time of departure is beyond that day that we reject that request straight away
    if(end_time.split(':')[0] <= '23'):
      count +=1
      initial_hr,initial_min,final_hr,final_min = int(start_times[start_idx].split(':')[0]),int(start_times[start_idx].split(':')[1]),int(end_time.split(':')[0]),int(end_time.split(':')[1])
      time_spent =  (final_hr - initial_hr) + (final_min - initial_min)/60

      #Create the dict with parameters start_time,end_time,burst_time,location,number_of_people,date of request
      requests_sheet[count] = {'start_time':start_times[start_idx],'end_time':end_time,'lat':40.715,'long':-74.014,'time_spent':time_spent,'people':num_people,'req_time':req_time}


  req_sheet = dict()

  for k,v in requests_sheet.items():
    hour,minute = v['start_time'].split(':')
    if( int(hour) <= 21 and int(minute) <= 0):
        req_sheet[k] = v

  
  #Sorting the request sheet by burst time as we promote people spending lesser time than usual to avoid occupancy in the office
  request_sheet_sorted = sorted(req_sheet.items(),key = lambda x:x[1]['time_spent'],reverse=False)

  opt_reqsheet = dict()
  for (k,v) in request_sheet_sorted:
      opt_reqsheet[k] = v

  saveData(req_sheet,opt_reqsheet)


    
    
