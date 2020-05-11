import data_generator as dg
import approveReject as ar
import onDemandRequest as dr
import pickle

if __name__ == '__main__':

    print('Generated Data')
    dg.generateData(4000)
    
    with open('requests_sheet.p', 'rb') as fp:
        request_og = pickle.load(fp)

    with open('optimized_request_sheet.p', 'rb') as f:
        request_opt = pickle.load(f)

    
    #print('Approved Request')
    ar.approveReject(request_og)
    th = ar.approveReject(request_opt)

    ar.approveReject(request_og,'day-wise')
    th = ar.approveReject(request_opt,'day-wise')

    #print('Chat Bot')

    c = dr.ChatBot()
    c.queueManager(th)



    
