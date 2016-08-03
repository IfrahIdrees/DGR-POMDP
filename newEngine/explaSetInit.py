import sys
sys.dont_write_bytecode = True


from database import *
from explanation import *





def explaSetInit():
    db = DB_Object()
    goal = db.find_all_method()
    #pendingSet = set()
    mypendingSet=[]
    mystart_action = []
    
    for x in goal:
        if len(x["start_action"])>0:
            for y in x["start_action"]:
                if [y, 0] not in mypendingSet:
                    mypendingSet.append([y, 0])
                    mystart_action.append(y)
       
    ##provide prior prob for each action in the pending set
    prob = float(1)/(len(mypendingSet))
    for x in mypendingSet:
        x[1]=prob
    
    exp = Explanation(v=1, pendingSet=mypendingSet, start_action=mystart_action)
    expla = explaSet()
    expla.add_exp(exp)

############################################################3
############################################################
##initialization, should initialize pending set and also Tasknet. 
## 

'''   
def explaSetInit():
    db = DB_Object()
    goal = db.find_all_method()
    #pendingSet = set()
    mypendingSet = []
    mypendingSet1= []
    myforest = []
    
    for x in goal:
        if len(x["start_action"])>0:
            for y in x["start_action"]:
                ##need to check if the current action already exist in the pending set.
                if [y, 0] not in mypendingSet:  
                    mypendingSet.append([y, 0])
                    mypendingSet1.append(y)
    
    ##provide prior prob for each action in the pending set
    prob = float(1)/(len(mypendingSet))
    for x in mypendingSet:
        x[1]=prob
    
    tasknet_pendingset = TaskNetPendingSet()
    #add a tasknet to the expla_forest
    tasknet_pendingset = TaskNetPendingSet(pending_actions = mypendingSet1)
    tasknet = TaskNet(pendingset = tasknet_pendingset)
    myforest.append(tasknet)
    
    
    
    exp = Explanation(v=1, forest=myforest, pendingSet=mypendingSet)
    expla = explaSet()
    expla.add_exp(exp)
'''
