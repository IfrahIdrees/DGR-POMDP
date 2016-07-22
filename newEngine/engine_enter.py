from explaSetInit import * 
from action_posterior import *
import time
explaSet=[] #explanation list
notification =[{
    "ob_name":"faucet_1",
    "reliability":"0.9",
    "attribute": "state",
    "previous": "off",
    "current": "on",
}] #notificiation list
interval = 1 ##sleep time when there is no state change notification

while(True):
    notification=[1] ##here, listen to the notification
    if len(notification) ==0:
        time.sleep(interval)
    else:
        if len(explaSet) is 0:
            explaSet = explaSetInit()
        '''
        for x in explaSet:
            print x._prob
            print x._forest
            print x._pendingSet
        '''
            
        ##calcuate the posterior prob of each action in pending set
        explaSet = action_posterior(explaSet, notification)
            
            
            
            
            
            
    break
     
         
        


    

#if 0 length, initialize the explaSet
if len(explaSet) is 0:
    explaSet = explaSetInit()
    '''
    for x in explaSet:
        print x._prob
        print x._forest
        print x._pendingSet
    '''

