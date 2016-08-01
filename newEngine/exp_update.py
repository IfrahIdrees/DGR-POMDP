import sys
import uuid
import copy
from collections import deque
from treelib import Tree
from explanation import *
from database import *
from helper import *

sys.dont_write_bytecode = True
db = DB_Object()


#use to udpate the current explanation according to the input action_explanation
#act_expla is the explanation for this observation, expla is the current explanation
def generate_new_expla(act_expla, expla):
    #firstly remove the just happened action from the pending set
    expla._pendingSet = [x for x in expla._pendingSet if x[0]!=act_expla[0]]
    
    #case 1: there is no expla._forest
    if len(expla._forest)==0:
        #goals is all possible tree-format explanation for the given action
        #with the format of [tree.root, prob]
        goals = initialize_tree_structure(act_expla[0])
        
        ##for each element in goal, create new explanation and add it into the
        exp = explaSet() 
        for g in goals:
            my_forest = []
            my_forest.append(g)
            #calculate the probability of action level and branching factors
            prob = act_expla[1]*g._expandProb
            #print "the new probability is", prob
            newexp = Explanation(v=prob, forest = my_forest, pendingSet = expla._pendingSet)
            #v=0, forest=[], pendingSet=[]
            exp.add_exp(newexp)
        
        #update the probability for the explanations(this is a special step)
        #for initialization. In this step, goal priors will be considered
        #In this case, we are using evenly distributed goal priors. 
        exp.normalize()
    
    #case 2: this explanation has already been initialized
    #else:
        


##generate a tree structure for the action_explanation
##this function is called only when the _forest parameter is null
##(with lenght of 0)
##Input: is only the action name (probability is not included)
def initialize_tree_structure(action):
    task_net = []
    temp_forest = deque([])
    tree = Tree()
    opdata = Node_data(complete = True)
    tree.create_node(action, action, data=opdata)
    #tree.create_node(action, uuid.uuid4(), data=opdata)
    temp_forest.append([tree, 1])     
    
    while temp_forest:
        length = len(temp_forest)
        for i in range(length):
            thisTree = temp_forest.popleft()
            tag = thisTree[0].get_node(thisTree[0].root).tag
            parents = db.get_parent_list(tag)
            if parents==False: print "error happend here please check"
            if len(parents)>0: 
                for x in parents: #x must be an method
                    method = db.find_method(x)
                    decompose_choose = method_precond_check(method,tag)
                    for decompose in decompose_choose:
                        decompose[0]=thisTree[1]*decompose[0]
                        temptree = copy.deepcopy(thisTree[0])
                        temp_forest.append(my_create_new_node(x, decompose, temptree))
    
            elif len(parents)==0: #this tree already reached goal node
                #print "this child", tag, "has no parent"
                #print "the probability for branch factor is", thisTree[1]
                my_goal = TaskNet(goalName=tag, tree=thisTree[0], expandProb=thisTree[1])
                my_goal.update()
                task_net.append(my_goal)
    
    return task_net
    
    
    
    
def method_precond_check(method, child):
    ##Step 1: calculate the precondition satisfy prob for each branch
    prob = []
    #print method["precondition"]
    for branch in method["precondition"]:
        prob_temp=1
        for ob_name in branch:
            for attri in branch[ob_name]:
                prob_temp = prob_temp * db.get_attribute_prob_1(branch[ob_name][attri], ob_name, attri)    
        prob.append(prob_temp)
    ##Step 2: normatlize on the prob    
    my_normalize_1(prob)
    ##Step 3: return all the branches that include the specified child
    satisfy_branch = []
    #print method["subtasks"]
    #print "the check child is ", child
    for i, x in enumerate(method["subtasks"]):
        #print x
        find=False
        for y in x:
            if y==child:
                find=True
        #find the child in this branch, attach it into the satisfy_branh 
        if find==True:
            satisfy_branch.append([prob[i], x])        
    return satisfy_branch    

   
def my_create_new_node(parent, decompose, childTree):
    newTree = Tree()
    parent_data = Node_data(complete=False, ready = True, branch = True)
    #newTree.create_node(parent ,uuid.uuid4(), data=parent_data)
    newTree.create_node(parent, parent, data=parent_data)
    
    known_child = childTree.get_node(childTree.root)
    #print "the know child is", known_child
    #print decompose[1]
    for x in decompose[1]:
        #print x
        
        if x==known_child.tag:
            known_child.data._pre = decompose[1][x]["pre"]
            known_child.data._dec = decompose[1][x]["dec"]
            newTree.paste(newTree.root, childTree)
        else:
            mydata = Node_data(pre=decompose[1][x]["pre"], dec=decompose[1][x]["dec"])
            newTree.create_node(x, x, parent=newTree.root, data= mydata)
    
    #newTree.show(line_type = "ascii")
    #print "the probability for this decompose is", decompose[0]
    return [newTree, decompose[0]]	
    
    
    
    

    
    
    

