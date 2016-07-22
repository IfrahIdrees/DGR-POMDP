#[">=", "0", "0", "0"]
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
