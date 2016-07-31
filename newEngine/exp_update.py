import sys
import uuid
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
    newexp = Explanation(expla._prob, expla._forest, expla._pendingSet)
    if len(expla._forest)==0:
        initialize_tree_structure(act_expla[0])





##generate a tree structure for the action_explanation
##this function is called only when the _forest parameter is null
##(with lenght of 0)
##Input: is only the action name (probability is not included)
def initialize_tree_structure(action):
    task_net = []
    temp_forest = deque([])
    tree = Tree()
    opdata = Operator_my_data(True)
    tree.create_node(action ,uuid.uuid4(), data=opdata)
    
    #[tree, 1]: [tree structure, probability]
    temp_forest.append([tree, 1])     
    
    while(True):
        length = len(temp_forest)
        stop = True
        for i in range(length):
            thisTree = temp_forest.popleft()
            tag = thisTree[0].get_node(thisTree[0].root).tag
            parents = db.get_parent_list(tag)
            if parents==False: print "error happend here please check"
            if len(parents)>0: 
                stop=False
                for x in parents: #x must be an method
                    method = db.find_method(x)
                    decompose_choose = method_precond_check(method,tag)
                    print decompose_choose
                
                
                
                
            elif len(parents)==0: #this tree already reached goal node
                my_goal = TaskNet(root=thisTree[0], expandProb=thisTree[1])
                task_net.append(my_goal)
            
        if stop==True: break
            
           
            
            
            
        break        
        
        
        
    
    
    #temp_forest = deque([]) #store all possible explanation for this action
    
    #TaskNet()
    
    
    
    #temp_tree._root.show(line_type = "ascii")
    
    
    
    
    
    

    
    
    

