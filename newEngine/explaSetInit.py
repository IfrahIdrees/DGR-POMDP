import sys
from database import *
from explanation import *



sys.dont_write_bytecode = True

def explaSetInit():
    db = DB_Object()
    goal = db.find_all_method()
    #pendingSet = set()
    pendingSet=[]
    
    for x in goal:
        if len(x["start_action"])>0:
            for y in x["start_action"]:
                if [y, 0] not in pendingSet:
                    pendingSet.append([y, 0])
    
        
    ##provide prior prob for each action in the pending set
    prob = float(1)/(len(pendingSet))
    for x in pendingSet:
        x[1]=prob
    
    exp = Explanation()
    exp.set_prob(1)
    exp.update_pendSet(pendingSet)
    
    expla = explaSet()
    expla.add_exp(exp)

    


