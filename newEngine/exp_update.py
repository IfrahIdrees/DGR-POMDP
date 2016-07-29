import sys
import uuid
from collections import deque
from treelib import Tree
from explanation import *

sys.dont_write_bytecode = True



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
    temp_forest = deque([])
    tree = Tree()
    opdata = Operator_my_data(True)
    tree.create_node(action ,uuid.uuid4(), data=opdata)
    temp_forest.append(tree)    
    
    while(True):
        length = len(temp_forest)
        for i in range(length):
            thisTree = temp_forest.popleft()
            tag = thisTree.get_node(thisTree.root).tag
            
            
            print tag
            
        break        
        
        
        
    
    
    #temp_forest = deque([]) #store all possible explanation for this action
    
    #TaskNet()
    
    
    
    #temp_tree._root.show(line_type = "ascii")
    
    
    
    
    
    

    
    
    

