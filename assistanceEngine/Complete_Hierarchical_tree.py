#########################################################################################
#Author: Dan Wang <d97wang@uwaterloo.ca>, Dec. 09, 2015
#Hierarchial_tree_expand.py function
#Given the initialized partial tree, generate the completed tree based on current state_t1
#when expanding the tree, dynamically expand nodes without children if the precondition of the 
#corresponding method is satisfied
#
#Attention! in order to include same node in a tree, modified the tree.py add_node
###########################################################################################
import random
import uuid
import copy
#import Action_recog
import DK_grooming
#import Hierarchical_Activity_recog
import ClassforHierarActRec
#from treelib import Tree, Node
#import FuncforHierarActRec


def Complete_Hierarchical_tree(Partial_tree, state_t1, person):
    #print "\n Inside Complete_Hierarchical_tree !"
    #state on time t+1
    #when generate next step, current situation must be considered
    #so as to guarantee the feasible of the generated prompt
    state_t1 = copy.deepcopy(state_t1)
    #initialized partial trees
    P_Hierar_Trees = copy.deepcopy(Partial_tree)
    #the expanded complete tree, only completed tasks are involved
    C_Hierar_Trees = []
    #a list of method trees
    forest = copy.deepcopy(DK_grooming.forest)
    #store the method dictionary
    methods = copy.deepcopy(DK_grooming.methods)
    #the list of operators
    operators = copy.deepcopy(DK_grooming.operators)
    
    
    for treeclass in P_Hierar_Trees:
        tree = treeclass._tree      
        checkednode = [] #only store the ID for these node
        for node in tree.all_nodes():
            checkednode.append(node.identifier)
             
        while checkednode:
            currentnodeID = random.choice(checkednode)
            currentnode = tree.get_node(currentnodeID)
            currenttag = currentnode.tag
            #print "inside complete tree, the current node tag is", currentnode.tag
            children = currentnode.fpointer
            '''
            for x in children:
                print "this children is", tree.get_node(x).tag
            '''
            
            if len(children) > 0: #the current node has children, don't need to expand
                #print "it goes into here, len(children)>1"
                checkednode.remove(currentnodeID)
            else:
                for subtree in forest:
                    if subtree.root == currenttag: 
                        
                        method = methods[currenttag][0]
                        subtask = method(state_t1, person)
                        if subtask == False: #precondition is not satisfied, don't need to expand
                            pass
                            
                        elif subtask[0] == "ordered":
                            tree.get_node(currentnodeID).data._childrenrelation = 0
                            if subtask[1] == 'split':
                                tree.get_node(currentnodeID).data._split = True
                            #paste other subtasks into the tree 
                            for i in range(2, len(subtask)):
                                if subtask[i][0] in operators:
                                    operator = operators[subtask[i][0]]
                                    statenow = copy.deepcopy(state_t1)
                                    if operator(statenow, person) == False:  #precondition unsatisfied
                                        break
                                    else:
                                        childdata = ClassforHierarActRec.Operator_my_data()
                                        childdata._order = i-1
                                        childID = uuid.uuid4()
                                        tree.create_node(subtask[i][0], childID, parent=currentnodeID, data= childdata)                            
                                        checkednode.append(childID)
                                else:
                                    childmethod = methods[subtask[i][0]][0]
                                    if childmethod(state_t1, person) == False:
                                        break
                                    else:
                                        childdata = ClassforHierarActRec.Method_my_data()
                                        childdata._order = i-1
                                        childID = uuid.uuid4()
                                        tree.create_node(subtask[i][0], childID, parent=currentnodeID, data= childdata)                                
                                        checkednode.append(childID)
                        else: #unordered
                            if subtask[1] == 'split':
                                tree.get_node(currentnodeID).data._split = True
                            for i in range(2, len(subtask)):
                                if subtask[i][0] in operators:
                                    operator = operators[subtask[i][0]]
                                    statenow = copy.deepcopy(state_t1)
                                    if operator(statenow, person) == False:  #precondition unsatisfied
                                        pass
                                    else:
                                        childdata = ClassforHierarActRec.Operator_my_data()
                                        childID = uuid.uuid4()
                                        tree.create_node(subtask[i][0], childID, parent=currentnodeID, data= childdata)
                                        checkednode.append(childID) 
                                else:
                                    childmethod = methods[subtask[i][0]][0]
                                    if childmethod(state_t1, person) == False:
                                        pass
                                    else:
                                        childdata = ClassforHierarActRec.Method_my_data()
                                        childID = uuid.uuid4()
                                        tree.create_node(subtask[i][0], childID, parent=currentnodeID, data= childdata)
                                        checkednode.append(childID)
                        #P_Hierar_Trees.append(tree)                                         
                checkednode.remove(currentnodeID)
        
        completetreeclass = ClassforHierarActRec.complete_tree(tree, treeclass._splitlabel)    
        C_Hierar_Trees.append(completetreeclass)
    
    '''
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "this is the tree decomposition result"
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    for x in C_Hierar_Trees:
        x._tree.show(line_type = "ascii")
    '''    
    return C_Hierar_Trees
                   
            
      
        
        
        
    
