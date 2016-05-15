import time
import datetime
#import ClassforHierarActRec
from treelib import Tree, Node
from copy import deepcopy
from platform import node
import ClassforHierarActRec
import copy

def check_highest_level(current_node, forest):
    rootnode = True
    for tree in forest:
        if tree.contains(current_node) and current_node != tree.get_node(tree.root).tag:
            rootnode = False
            return rootnode
    return rootnode



def updatedata(object):
    #print "inside updatedatat"
    #print object.root.tag
    completenum = 0
    startnum = 0
    parentnode = object.get_node(object.root) #obtain the parent node
    #print parentnode.tag
    data = parentnode.data
    siblings = parentnode.fpointer
    #print "the number of siblings is", len(siblings)
    for x in siblings:
        node = object.get_node(x)
        #print "this child is ", node.tag
        if node.data._completeness == True:
            completenum += 1
        if (node.is_leaf() == False) and (node.data._start) == True:
            startnum = startnum + 1

    data._completednum = completenum
    if (completenum + startnum) > 0:
        data._start = True
    
    if completenum == len(siblings):
        data._completeness = True
    
    parentnode.data = data
    #print parentnode.data._start
    #print parentnode.data._completeness    
    return data

   

def generate_unique_ID(tree):
    ID = 1
    if tree.size()== 0:
        return ID
    allnode = tree.all_nodes()
    for node in allnode:
        if node.identifier > ID:
            ID = node.identifier       
    ID +=1
    return ID        
            
def put_in_sequence(childID, tree):
    thetree = copy.deepcopy(tree)
    #print len(childID)
    
    #tree.show(line_type = "ascii")
    #print "inside put in sequence"
    thelist = copy.deepcopy(childID)
    for x in childID:
        childnode = tree.get_node(x)
        if childnode != None:
            #print childnode.tag
            thelist[childnode.data._order -1] = x
        #print type(childnode)
        #print tree.get_node(x).data._order - 1
        #thelist[tree.get_node(x).data._order - 1] = x
    return thelist


def search_in_prompt(operator, treeprompt):
    if treeprompt._splitlabel == False: #should not split current task
        label = in_prompt_list(operator, treeprompt._prior_prompt_set, treeprompt._tree)
    else:
        label = in_prompt_list(operator, treeprompt._promp_set, treeprompt._tree)   
    return label


    
def in_prompt_list(operator, promptlist, tree):
    
    for levelprompt in promptlist:
        for prompt in levelprompt:
            node = tree.get_node(prompt)
            if node.tag == operator:
                return node.identifier
    return False        


def exist_in_prompt(prompt, operator):
    for promptset in prompt:
        for treeprompt in promptset:
            label = search_in_prompt(operator, treeprompt)
            if label != False: #found the node in prompt list
                storetreeprompt = copy.deepcopy(treeprompt)
                #update the record the the corresponding tree
                #mainly update the data of the tree
                storetreeprompt = Complete_tree_update\
                (label, storetreeprompt, state_t1, person)
                promptset = []
                promptset.append(storetreeprompt) #only store this tree, delete others
                find_in_prompt = True
                break

        
    
    
    
    
