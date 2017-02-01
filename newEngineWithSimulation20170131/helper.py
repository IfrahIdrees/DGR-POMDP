import sys
sys.dont_write_bytecode = True

from database import *
import json



db = DB_Object()


##############################################################
#################normalizing##################################
###############################################################



###normalize the probability of pending set[action_name, prob]
def my_normalize(act_expla):
    mysum = 0
    for x in act_expla:
        mysum=mysum+x[1]
    for x in act_expla:
        x[1]=x[1]/mysum
    return act_expla
    
##normatlize the probability p[p1, p2, p3]    
def my_normalize_1(prob):
    mysum=0
    for x in prob:
        mysum=mysum+x
    if mysum==0: return
    for i in range(len(prob)):
        prob[i] = float(prob[i]/mysum)
##to check if the precondition of a method is satisfied
## the return value is [[prob, [subtasks]]]

def compare_ability(ab1, pre_ab2):
    if pre_ab2[0] == ">=":
        #print "come to here"
        return no_less_than(ab1, pre_ab2)
    return False
   
#############################################################
###################constraint################################
#############################################################
#############################################################
#constraint: no_less_than
def no_less_than(ab1, pre_ab2):
    #print ("inside no less than")
    
    #len_ab1 = len(ab1)
    for i, x in enumerate(ab1):
        #print x
        if i==0: continue
        if float(ab1[i]) < float(pre_ab2[i]):
           return False
    #print "i want return true"
    return True 

##############################################################
#################return the average of a list###################
def list_average(mylist):
    length = len(mylist)
    if length==0:
        return -1
    mysum = 0
    for x in mylist:
        mysum = mysum+x
    ##the return value is an int now
    return mysum/length

