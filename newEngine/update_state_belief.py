import sys
sys.dont_write_bytecode = True


from database import *
from notification import * 
from helper import *
from explanation import *


cond_not_satisfy = 0.001
cond_satisfy = 0.999
title = [] #all possible state in the effect list of pending set actions 
db = DB_Object()
exp=explaSet()
update_state = []
action_list = {}

def update_state_belief():    
    get_attr_in_effect()
    for i, x in enumerate(title):
        att = db.get_object_attri(x[0], x[1])
        att = update_attri_status_belief(att, i)
        #db.update_state_belief(title[i][0], title[i][1], att)

#get all the state that occur in the effect list
#of actions in the pending set
def get_attr_in_effect():
    my_set = set()
    for expla in exp.explaset:
        for action in expla._pendingSet:
            if action_list.has_key(action[0]):
                action_list[action[0]]=action_list[action[0]]+action[1]
            else:
                action_list[action[0]]=action[1]
                
            #action_list.append(action)
            op = db.get_operator(action[0])
            for x in op["effect"]:
                for y in op["effect"][x]:
                    s = x+"."+y
                    my_set.add(s)
    for x in my_set:
        title.append(x.split('.'))
    #calculate the prob of nothing happened
    noth_prob = 1
    for k, v in action_list.items():
        noth_prob = noth_prob*(1-v)
    '''    
    #normalize on something happened
    happen_prob = 1-noth_prob
    for k in action_list:
        action_list[k] = action_list[k]/happen_prob    
    '''
    
    action_list["nothing"] = noth_prob
    return 

#update the attribute status belief for a specific attribute
def update_attri_status_belief(att, index):
    newp = att
    sump=0
    for x in newp:
        #print "this attribute value is ", x
        p = 0
        for y in att:
            
            for k, v in action_list.items():
                ##p(a)
                pa = float(v)
                #print "pa is", pa
                ##p(s_1)
                ps_1 = float(att[y])
                #print "ps_1", ps_1
                
                #calculate p(o_t|s_t)
                po_s = db.get_obs_prob(x, title[index][0], title[index][1])
                #print "po_s", po_s
                
                #calculate p(s|s_t-1, a_t) happen
                ps_actANDs = get_ps_actANDs(x, y, [k, v], index)
                #print "ps_actANDs", ps_actANDs
                #print pa * ps_1 * po_s * ps_actANDs
                p = p+pa * ps_1 * po_s * ps_actANDs
                 
        #print "the final result is ", p    
        newp[x] = p
        #print ""
        sump = sump +p            
    
    
    #normalize
    for x in newp:
        newp[x] = newp[x]/sump
    return newp
    

def get_ps_actANDs(after, before, action, index):
    #case 1: nothing happened
    if action[0]=="nothing":
        if after==before:
            return cond_satisfy
        else:
            return cond_not_satisfy
    
    #get the action;   
    op = db.get_operator(action[0])
   
    
    #check effect 
    #the whether target attribute status change
    #exist in the effect list 
    #if exist, continue, else return 0   
    effect = op["effect"]
    
    if title[index][0] not in effect:
        if before == after:
            return cond_satisfy
        else:
            return cond_not_satisfy
    
    #print effect[title[index][0]][title[index][1]]
    elif effect[title[index][0]][title[index][1]] != after:
        return cond_not_satisfy
    
    ##check precondition
    #check if the precondition of the action is satisfied
    #in the previous state
    precond = op["precondition"]
    if precond[title[index][0]][title[index][1]] != before:
        return cond_not_satisfy
        
    #return value
    return cond_satisfy


