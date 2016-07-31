import sys
from database import *
sys.dont_write_bytecode = True


#db = DB_Object()
###normalize the probability of pending set[action_name, prob]
def my_normalize(act_expla):
    mysum = 0
    for x in act_expla:
        mysum=mysum+x[1]
    for x in act_expla:
        x[1]=x[1]/mysum
    return act_expla

##to check if the precondition of a method is satisfied
## the return value is [[prob, [subtasks]]]
def method_precond_check(method, child):
    db = DB_Object()
    #print method["precondition"]
    #if len(method["precondition"])==1:  ##there is no alternative branch
     #   return [[1, method["subtasks"][0]]]
    
    ##there are alternative branches
    ##Step 1: calculate the precondition satisfy prob for each branch
    ##Step 2: normatlize on the prob
    ##Step 3: return the branch that include the specified child
    #else:
    prob = []
    #print method["precondition"]
    for branch in method["precondition"]:
        prob_temp=1
        for ob_name in branch:
            #print ob_name
            for attri in branch[ob_name]:
                #print attri
                prob_temp = prob_temp * db.get_attribute_prob(branch[ob_name][attri], ob_name, attri)
                
       
                    
                
                #print attri
            
        prob.append(prob_temp)
    print prob   
    return 0
        
            


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
        if i==0: continue
        if float(ab1[i]) < float(pre_ab2[i]):
           return False
    #print "i want return true"
    return True 


    
    
    
