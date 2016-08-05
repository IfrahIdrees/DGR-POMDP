from explanation import *

def pendingset_generate():
    exp = explaSet()
    exp.normalize()
    for expla in exp.explaset:
        #print "before,  ", expla._prob
        #print "before,  ", expla._pendingSet
        if len(expla._pendingSet)==0:
            expla.set_pendingSet(create_pendingSet(expla))
        else:
            expla.set_pendingSet(normalize_pendingSet_prior(expla))
     
    #for expla in exp.explaset:
        #print "after,  ", expla._prob
        #print "after,  ", expla._pendingSet 
            
                
def create_pendingSet(expla):
    #print expla._prob
    pendingSet = set()
    for taskNet in expla._forest:
        for taskNetPending in taskNet._pendingset:
            for action in taskNetPending._pending_actions:
                pendingSet.add(action)
    for action in expla._start_action:
        pendingSet.add(action)
    
    pendingSet1 = []
    prior = float(1)/len(pendingSet)
    for x in pendingSet:
        pendingSet1.append([x, expla._prob*prior])
    
    return pendingSet1
    
    
def normalize_pendingSet_prior(expla):
    pendingSet =  expla._pendingSet
    prior = float(1)/len(pendingSet)
    for x in pendingSet:
        x[1]=expla._prob*prior
    return pendingSet   
    
    
