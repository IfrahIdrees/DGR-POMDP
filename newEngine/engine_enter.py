import sys
import time
import random
from explaSetInit import * 
from action_posterior import *
from update_state_belief import *
from explanation import *
from exp_expand import *

sys.dont_write_bytecode = True


no_notif_trigger_prob = 0.2
interval = 1 ##sleep time when there is no state change notification


while(True):
    notification=[1] ##here, listen to the notification
    #if no notification, and the random prob is less than no_notif_trigger_prob
    #sleep the engine
    if len(notification) ==0 and random.random()<no_notif_trigger_prob:
        time.sleep(interval)
    
    #go through the engine logic to update
    else:
        exp = explaSet()
        ##if exp.explaset has not been initialized, initialized it using
        ##explaSetInit()
        if len(exp.explaset) is 0:
            explaSetInit() 
             
        ##calcuate the posterior prob of each action in pending set
        explaSet = action_posterior()
        
        
        ##update the belief state
        update_state_belief()
        
        ##update the explanation         
        ##for each existing explanation, includes three steps:
            ##step1: decide which actions has happended and its distribution
                    ##(obtain the action level explanation for the current obs)
            ##step2: for each action level explanation, generate new explanation and
                    ##update the corresponding tree structure, and calculate the
                    ##probability of the explanation
            ##step3: calculate the probability of this explanation
            ##step4: update the pending set
                    ##(including the prior probability of actions in the pending set)
        
        explanation_expand()
        print len(exp.explaset)
        
        '''
        for x in exp.explaset:
            print x._prob
            print x._forest
            print x._pendingSet    
        '''
        ##calculate the probability of goals and innner nodes in the tree
        ##this kind of information is used for promp decision making. 
        ##unlike the paper, my algorithm needs to calculate the probability of
        ##each node. So as to realize hierarchical prompt.         
    break
     
         
        


    


