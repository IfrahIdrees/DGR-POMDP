#########################################################################################
#Author: Dan Wang <d97wang@uwaterloo.ca>, Dec. 06, 2015
#Hierarchical_Activity_recog.py function
#Given the specific action, generate the partial tree based on domain knowledge.
#When generating the partial tree, we need to check the preconditions of method 
#in domain knowledge. The result of the function is the hierarchical structure that
#include the specific action. With the hierarchical structure we can realize
#hierarchical activity recognition. That is we can not only tell which action the person
#is doing, we can also tell the goal of the person and also what kind of other actions the 
#person will do to accomplish the goal.  
###########################################################################################
# import time
# import datetime
import random
import uuid
import copy
import ClassforHierarActRec
import FuncforHierarActRec
# import Action_recog
from treelib import Tree

from platform import node
import DK_grooming
# import functools
# from tokenize import Funny


def Hierarchical_Activity_recog(execute_actions, state_t, person):
    #print "\n Inside Hierarchical_Activity_recog!"
    
    #a list of method trees
    forest = copy.deepcopy(DK_grooming.forest)
    #a list of operators that might be happening 
    actionlist = copy.deepcopy(execute_actions)
    #the list of operators
    operators = copy.deepcopy(DK_grooming.operators)
    #store the method dictionary
    methods = copy.deepcopy(DK_grooming.methods) 
    #store the partial hierarchical trees
    P_Hierar_Trees = []
    #state on time t
    state_t = copy.deepcopy(state_t)
  
    #print "hierarchical Activity recognition"

    forest_ingenerate = []
    ##the basic idea is generate the tree evenly

    for operator in actionlist:
        '''
        print "\n"
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print "the recognized atomic action is", operator
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print "\n"
        '''
        
        currentTree = Tree()
        #firstly change the completeness state of the operator into 
        #completeness = true
        nodedata = ClassforHierarActRec.Operator_my_data()
        nodedata._completeness = True
        #ID = FuncforHierarActRec.generate_unique_ID(currentTree)
        currentTree.create_node(operator, uuid.uuid4(), data = nodedata)
        currentTreeclass = ClassforHierarActRec.complete_tree(currentTree, False)
        #currentTree.show(line_type = "ascii")
        forest_ingenerate.append(currentTreeclass)
    
    
    ##Up search one step for each tree in forest_ingenerate
    while forest_ingenerate:
        splitlabel = False
        currentTreeclass = random.choice(forest_ingenerate)
        currentTree = currentTreeclass._tree
        node = currentTree.get_node(currentTree.root).tag 
        #parent tag, it is the same as the "ID" in trees in forest
        for tree in forest:
            if tree.contains(node) and tree.get_node(tree.root).tag != node: 
                #node should be the child of the tree
                methodID = tree.root
                method = methods[methodID][0]
                subtask = method(state_t, person)
                
                if subtask == False: 
                    #the precondition of the method is not satisfied in state_t
                    #the node should be the root of a tree. 
                    #Append it to P_Hierar_Trees
                    #but should not remove it from forest_ingenerate
                    if currentTree not in P_Hierar_Trees:
                        P_Hierar_Trees.append(currentTreeclass)
                
                elif subtask[0] == 'ordered':
                    #the subtasks are ordered
                    if subtask[2][0] == node:  #node is the tag name
                        #the root of currentTree should be the first subtask of the method
                        #since it is in initialization process
                        newTree = Tree()
                        parent_data = ClassforHierarActRec.Method_my_data()
                        parent_data._childrenrelation = 0
                        if subtask[1] == 'split':
                            parent_data._split = True
                            splitlabel = True
                        
                        #other attribute in data is updated after all children are added into the tree
                        newTree.create_node(methodID, uuid.uuid4(), data=parent_data)
                        
                        currentTree.get_node(currentTree.root).data._order = 1
                        newTree.paste(newTree.root, currentTree) #paste the currentTree to the newTree     
                        #paste other subtasks into the tree                       
                        for i in range(3, len(subtask)):                       
                            if subtask[i][0] in operators:
                                #print "in operators"
                                childdata = ClassforHierarActRec.Operator_my_data()
                                childdata._order = i-1
                                newTree.create_node(subtask[i][0], uuid.uuid4(), parent=newTree.root, data= childdata)
                            else:
                                childdata = ClassforHierarActRec.Method_my_data()
                                childdata._order = i-1
                                newTree.create_node(subtask[i][0], uuid.uuid4(), parent=newTree.root, data= childdata)
                        #update the data attribute of the root of the new tree
                        newTree.get_node(newTree.root).data = FuncforHierarActRec.updatedata(newTree)
                        newTreeclass = ClassforHierarActRec.complete_tree(newTree, splitlabel)
                        forest_ingenerate.append(newTreeclass)
                        
                    else: print "error operation! Alert the care-giver!"  #in real situation  
                        
                else: #the subtasks are unordered, easy to implement 
                    newTree = Tree()
                    parent_data = ClassforHierarActRec.Method_my_data()
                    if subtask[1] == 'split':
                        parent_data._split = True
                        splitlabel = True
                    newTree.create_node(methodID, uuid.uuid4(), data=parent_data)
                    newTree.paste(newTree.root, currentTree)
                    for i in range(2, len(subtask)):
                        if subtask[i][0] == node:
                            pass
                        else:
                            if subtask[i][0] in operators:
                                childdata = ClassforHierarActRec.Operator_my_data()
                            else:
                                childdata = ClassforHierarActRec.Method_my_data()
                            newTree.create_node(subtask[i][0], uuid.uuid4(), parent=newTree.root, data= childdata)
                                
                    newTree.get_node(newTree.root).data = FuncforHierarActRec.updatedata(newTree)
                    newTreeclass = ClassforHierarActRec.complete_tree(newTree, splitlabel)
                    forest_ingenerate.append(newTreeclass)
    
        forest_ingenerate.remove(currentTreeclass)#remove the currentTree after traversal on the forest 
        #add the completed tree into P_Hierar_Trees and delete from
        ##forest_ingenerate
        for generate_treeclass in forest_ingenerate:
            generate_tree = generate_treeclass._tree
            node = generate_tree.get_node(generate_tree.root).tag
            
            label = FuncforHierarActRec.check_highest_level(node, forest)
            if label == True:
                if generate_treeclass not in P_Hierar_Trees:
                    P_Hierar_Trees.append(generate_treeclass)
                    forest_ingenerate.remove(generate_treeclass)  
    
    '''
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "this is the result of hierarchical activity recognition result"  
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        
    for x in P_Hierar_Trees:
        x._tree.show(line_type = "ascii")
    '''       
    return P_Hierar_Trees      





    
    
