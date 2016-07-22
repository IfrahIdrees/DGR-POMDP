from database import *
from explanation import *

def explaSetInit():
    db = DB_Object()
    goal = db.find_all_method()
    pendingSet = [[y, 0] for x in goal if len(x["start_action"])>0 for y in x["start_action"]]
    #pendingSet.append(["nothing_hap", 0])
    
    ##provide prior prob for each action in the pending set
    prob = float(1)/(len(pendingSet))
    for x in pendingSet:
        x[1]=prob
    
    exp = Explanation()
    exp.set_prob(1)
    exp.update_pendSet(pendingSet)
    
    explaSet = []
    explaSet.append(exp)
    return explaSet

    
    


