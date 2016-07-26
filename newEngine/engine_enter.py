from explaSetInit import * 
from action_posterior import *
from update_state_belief import *
from explanation import *
import time
#explaSet=[] #explanation list
interval = 1 ##sleep time when there is no state change notification

while(True):
    notification=[1] ##here, listen to the notification
    if len(notification) ==0:
        time.sleep(interval)
    else:
        exp = explaSet()
        if len(exp.explaset) is 0:
            explaSetInit()
        '''
        for x in explaSet:
            print x._prob
            print x._forest
            print x._pendingSet
        '''
            
        ##calcuate the posterior prob of each action in pending set
        explaSet = action_posterior()
        
        '''
        for x in exp.explaset:
            print x._prob
            print x._forest
            print x._pendingSet    
        '''
        
        ##update the belief state
        update_state_belief()    
            
            
            
            
    break
     
         
        


    


