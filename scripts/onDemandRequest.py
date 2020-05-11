import sys
import pickle
import data_generator as dg
import approveReject as ar
import os
import send_mail as sme

class ChatBot:
    

    def onDemandRequest(self,data,request_sheet,req_no,threshold):

      location = str(request_sheet[req_no]['lat'])+' '+ str(request_sheet[req_no]['long'])
      self_imposed = 0
      tolerance = int(0.05 * threshold)
      time_slots = dg.generateTimeKeys()

      path = os.path.join(os.getcwd(),'scheduler.p')
      with open(path, 'rb') as fp:
          dict_requests = pickle.load(fp)

      for k,v in data.items():
        prev_end_time = request_sheet[k]['end_time']
        time_ext = v['time_extension']
        end_time = dg.convertToMinutes(prev_end_time,time_ext)
        people = v['no_of_people']


        hour,minutes = end_time.split(':')[0],end_time.split(':')[1]

        if(len(hour) == 1):
          hour = '0'+str(hour)
          end_time = hour+':'+minutes

        if(int(hour) >= 24):
            end_time = '23:30'
            self_imposed = 1

        if(self_imposed == 1):
            message = 'We cannot allow to allocate the request excedding to the next day\n'
            response = input('Do you want to continue till 23:30 ? Y/N')
            if(response.lower() == 'n'):
                print('Your Request has been cancelled...')
                return 
            else:
                print('Processing your request further...\n')
                
        s_idx = time_slots.index(prev_end_time)
        e_idx = time_slots.index(end_time)

        allSlots = []
        allSlots = time_slots[s_idx:e_idx+1]

        not_statisfied = 0

        for key_ in allSlots:
          threshold = threshold+tolerance
          if not (dict_requests[key_] + people <= threshold):
            not_statisfied = 1
            break
        
        if(not_statisfied == 0):
          for key_ in allSlots:
            dict_requests[key_] += people

          ar.generateQRCode(prev_end_time,end_time,location,people,fol_name = 'OnDemand_qrCode',mail_id = 'vvt223@nyu.edu')
          sme.mailMe(location,'vvt223@nyu.edu')
        else:
          print('Your request has been Rejected, we apologize your loss')
          not_statisfied = 0
    
    def askMe(self,threshold):


      with open(os.path.join(os.getcwd(),'approved_requets.p'), 'rb') as fp:
          request_sheet = pickle.load(fp)


      print(list(request_sheet.keys())[0:10])
          
      print('Alexa - Welcome to helpdesk for extension time')
      
      req_no = int(input('Enter Previous Request Number Allocated to Fetch All Information\n'))
      
      print('----------User Information----------\n')
      print('Start_Time :',request_sheet[req_no]['start_time'])
      print('End_Time :',request_sheet[req_no]['end_time'])
      print('Time spent :',request_sheet[req_no]['time_spent'])
      print('People Approved :',request_sheet[req_no]['people'])

      while(True):
          time_ext = int(input('Enter the time to be extended(mins): '))
          if(req_no not in request_sheet):
              print('Enter correct request number')
          else:
              break

      no_of_people = request_sheet[req_no]['people']
      apprv = input(f'Do you want to request extension for {no_of_people} people Y/N : ')

      if(apprv.lower() == 'n'):
          no_of_people = int(input('Enter no of people'))

      else:
          no_of_people = request_sheet[req_no]['people']
          
      print('Wait for Processing your On Demand Request.....\n You will be notified on mail Shortly')

      data = {req_no:{'time_extension':time_ext,'no_of_people':no_of_people}}
      self.onDemandRequest(data,request_sheet,req_no,threshold)


    def queueManager(self,threshold):
        for line in sys.stdin:
            line = line.rstrip()
            if(line == 'Exit'):
                break
            else:
                self.askMe(threshold)

