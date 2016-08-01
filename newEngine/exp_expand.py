import sys
from explanation import *
from collections import deque
from exp_update import *
from helper import *


sys.dont_write_bytecode = True
delete_trigger = 0.001

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


def explanation_expand():
    exp = explaSet()
    length = exp.length()
    
    for i in range(length):
        x = exp.pop()  #get an explanation and remove it
        act_expla = action_level_explanation(x._pendingSet)
        for y in act_expla:
            #case1: nothing happened: update the prob of the explanation, 
            #do not need to update tree structure. 
            if y[0]=="nothing":
                newexpla = Explanation(v=x._prob*y[1], forest = x._forest, pendingSet = x._pendingSet)
                exp.add_exp(newexpla) 
                #v=0, forest=[], pendingSet=[]
            #case2:something happend, need to update the tree structure as well
            else:
                generate_new_expla(y, x)

    return

    
def action_level_explanation(pendingset):
    nothing_happen = 1
    prob_sum = 0
    ##calculate the prob of nothing happen
    for x in pendingset:
        prob_sum = prob_sum + x[1]
        nothing_happen = nothing_happen*(1-x[1])
    #print "nothing happend is", nothing_happen
    
    ##normalize the prob of something happen prob
    act_expla = []
    some_happen = 1-nothing_happen
    act_expla.append(["nothing", nothing_happen])
    for x in pendingset:
        act_expla.append([x[0], x[1]/prob_sum*some_happen])
    
    ##delete some action whose prob<delete_trigger and normalize
    act_expla = [x for x in act_expla if x[1]>=delete_trigger]
    act_expla = my_normalize(act_expla)
    
    return act_expla






'''
##get the action level explanation
##allow multiple action happen version 
def action_level_explanation(exp):
    act_expand = deque([])
    for i in range(len(exp)):
        if len(act_expand)==0:
            act_expand.append([list(exp[i])])
            act_expand.append([list(["nothing", 1-exp[i][1]])])
        else:
            length = len(act_expand)
            for j in range(length):
                temp = act_expand.popleft();
                temp.append(exp[i])
                act_expand.append(list(temp))
                temp.pop()
                temp.append(["nothing", 1-exp[i][1]])
                act_expand.append(list(temp))
                                
    return act_expand                
'''  
    
    
    
    
    
        
