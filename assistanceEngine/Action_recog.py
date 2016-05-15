###############################################################
#Author: Dan Wang <d97wang@uwaterloo.ca>, Dec. 06, 2015
#action_recog.py function
#given an state change(compare state at time t and state at time t+1)
#target the atomic action.
################################################################
#import time
import copy
from DK_grooming import operators
from ClassforHierarActRec import State

#Assumption: Recognize one operator at one step
def action_recog(state_t, state_t1):
    #print "\n Inside Action_recog \n"
    #store all operators that generate the specific state change
    execute_operators = {}
    if state_t == state_t1:
        print " no state change"
    else:
        print " has state change"
        for atomic in operators:
            state_tt = State
            state_tt = copy.deepcopy(state_t)
            operator = operators[atomic]
            state_tt = operator(copy.deepcopy(state_tt),'grandpa')
            if state_tt == state_t1:
                execute_operators.update({operator.__name__:operator})    
    return execute_operators
