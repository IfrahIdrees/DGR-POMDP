
#from explanation import *
from database import *


{
    "ob_name":"faucet_1",
    "reliability":"0.9",
    "attribute": "state",
    "previous": "off",
    "current": "on",
}



def action_posterior(explaSet, notification):
    for expla in explaSet:
        for action in expla._pendingSet:
            action[1]=cal_posterior(action, notification)
            ####################3
    return explaSet
    

def cal_posterior(action, notification):
    db = DB_Object()
    op = db.get_operator(action[0])
    prob = action[1]
    print prob
    #print op["precondition"]
    
    beforeS = []
    afterS = []
    for x in op["precondition"]:
        beforeS.append(db.get_object_state(x))
    
    afterS = beforeS
    
    
    title = []
    for x in beforeS:
        for y in x:
            if y!="ob_name" and y!="ob_type" and y!="_id":
                title.append([x["ob_name"], y])
                
    '''
    for x in title:
        print x
    '''            
    enum = myDFS(title, beforeS)
    new_prob=variable_elim(enum, op)
    for x in enum:
        new_prob=new_prob+ float(prob)*(bayesian_expand(x, op))
    
    
    '''
    print "the length of enum is ", len(enum)
    for x in enum:
        print x
    '''
##dfs is used to generate the enumeration of all possible
##state combinations    
def myDFS(title, beforeS):
    enum = []
    va = []
    realMyDFS(enum, va, title, beforeS)
    return enum


def realMyDFS(enum, va, title, beforeS):
    if len(va)==len(title):
        enum.append(list(va))
        return enum
        
    key = title[len(va)]
    select_state = [x for x in beforeS if x["ob_name"]==key[0]]
    attr = select_state[0][key[1]]
    for x in attr:
        va.append(x)
        realMyDFS(enum, va, title, beforeS)
        va.remove(x)
        
##impliment the bayesian network calculation for one possible state
##variable elimination!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##
def variable_elim()
def bayesian_expand(sv, op):
            
    
    
           
        
        
    
    '''
    for x in op:
        for y in x["precondition"]:
            print x["precondition"][y]
'''
    ##find the action knowledge base from the database
    

'''
{
    "name":"faucet_1",
    "reliability":"0.9",
    "attribute": "state",
    "previous": "on",
    "current": "off",
}
'''
#explaSet = action_posterior(explaSet, notification)
