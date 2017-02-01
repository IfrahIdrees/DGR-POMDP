import sys
sys.dont_write_bytecode = True

import copy
from treelib import Tree
from treelib import Node
from collections import deque
from TaskNetPendingSet import *
from database import *
from helper import *
from Node_data import *


db = DB_Object()
class TaskNet(object):
    def __init__(self, goalName="", tree=Tree(), expandProb = 1, pendingset=TaskNetPendingSet(), complete = False):
        self._goalName=goalName ##this is the goal name of the tree, it is a string;
        self._tree = tree
        self._expandProb=expandProb
        self._pendingset = pendingset #[tree, action, new_added branch prob compared with the self._tree]
        self._complete = complete
    
    

    
    ##Functions:
    
    ##(1) update node completeness property
    ##(2) update node ready property
    ##(3) generate the new pending set
    ##(4) for each action in the pending set, calculate the branching prob based on the tree structure 
    
    #rootnode.data.print_property()
    
    def update(self):
        #print
        #print "update a new tree-------------------"
        rootnode = self._tree.get_node(self._tree.root)
        #update completeness
        
        self.complete_update(rootnode, self._tree)
        if rootnode.data._completeness == True:
            self._complete=True
            return
        
        #update ready-ness
        self.readiness_update(self._tree.root, self._tree)
        
        #update pendingset
        self._pendingset = self.pendingset_update(self._tree.root, self._tree)
        
        
        
    #update pending set
    #pendingset is a list, each element has the format of 
    #[tree, action, new_added branch prob compared with the initial tree]
    def pendingset_update(self, node, tree):
        
        
        expand_tree = []
        tree_queue = deque([])
        tree_queue.append([copy.deepcopy(tree), 1])
        while tree_queue:
            thisTree = tree_queue.popleft()
            leaves = thisTree[0].leaves()
            #print "the leaves is"
            
            finish = True #to check if the tree finished its decomposition process
            #for each node:
            #if it is a leaf node, check
                #
            for leaf in leaves:
                #print "this leaf is", leaf.tag
                #print "the readiness is", leaf.data._ready
                #print "the completeness is", leaf.data._completeness
                if leaf.data._ready==True:
                    method = db.find_method(leaf.tag)
                    if method==None: 
                        #print "this leaf is an step, not method:   ", leaf.tag
                        continue
                    else:
                        finish = False
                        #print "this leaf is a method     ", leaf.tag
                        branches = self.method_decompose(method)
                        for x in branches:
                            newTree = copy.deepcopy(thisTree[0])
                            self.add_child(newTree, leaf.tag, x[1])
                            tree_queue.append([newTree, thisTree[1]*x[0]])
                        break
                        
            if finish==True:
                #print 
                #print "udpate the tree again?????????????????"
                self.readiness_update(self._tree.root, self._tree)
                tree_pending=[x.tag for x in leaves if x.data._ready==True and x.data._completeness==False]
                #print "the new pending set is ", tree_pending
                thisTree.append(tree_pending)
                
                mytasknetpending = TaskNetPendingSet(tree = thisTree[0], branch_factor = thisTree[1], pending_actions = thisTree[2])
                
                expand_tree.append(mytasknetpending)
        return expand_tree
    
    
    
    
    def method_decompose(self, method):
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
        
        satisfy_branch = []
        for i, x in enumerate(method["subtasks"]):
            satisfy_branch.append([prob[i], x])
        return satisfy_branch      
    

    def add_child(self, tree, node_id, branch):
        #print "the target node is", node_id
        #print "the branch is", branch
        for x in branch:
            #print "this action is   ", x
            mydata=None
            #print "this branch is", branch[x]["pre"]
            if len(branch[x]["pre"]) == 0:
                
                mydata=Node_data(ready=True, branch = False, pre=branch[x]["pre"], dec = branch[x]["dec"])
            else:
                '''
                checkReady = True
                for x in branch[x]["pre"]:
                    print x
                    if tree.get_node(x)!=None and tree.get_node(x).data._completeness == False:
                        checkReady = False
                        break
                '''
                mydata=Node_data(ready=False, branch = False, pre=branch[x]["pre"], dec = branch[x]["dec"])
            
            tree.create_node(x, x, parent = node_id, data = mydata)
            #print "the length is", len(branch[x]["pre"])
            #print branch[x]["pre"]

    #complete = False, ready=False, branch = False, pre="", dec=""
    #mydata = Node_data(pre=decompose[1][x]["pre"], dec=decompose[1][x]["dec"])
            #    newTree.create_node(x, x, parent=newTree.root, data= mydata)

        
    #update completeness
    def complete_update(self, node, tree):
        
            
        if node.is_leaf(): return node.data._completeness
        child = node._fpointer #get the id of childrens
        for x in child:
            if self.complete_update(tree.get_node(x), tree): continue
            else:
                node.data._completeness = False
                return False
        
        node.data._completeness = True
        
        return True
    
    #update readiness
    #idea: from top to bottom, BFS
    def readiness_update(self, root_id, tree):
        '''
        tree.show(line_type = "ascii")
        all_node = tree.all_nodes()
        print "before update the ready ones is--------------------------------"
        for x in all_node:
            print x.tag, "   ", x.data._ready
        '''
        node_queue = deque([])
        node_queue.append(root_id)
         
        while node_queue:
            cur_node = tree.get_node(node_queue.popleft())
            #case 1: this node has no parent, readiness = true
            if cur_node.is_root():
                cur_node.data._ready=True
            #case 2: this node has parent, and len(pre)=0
                    #equal to parents's readiness
            elif len(cur_node.data._pre)==0:
                pid = cur_node._bpointer
                cur_node.data._ready = tree.get_node(pid).data._ready
            #case 3: this node has parent, and len(pre)>0
            else:
                cur_node.data._ready=True
                pre_list = cur_node.data._pre
                #print "the current node is", cur_node.tag
                for x in pre_list:
                    #print "thuis pre in pre_list is", tree.get_node(x).tag, tree.get_node(x).data._completeness
                    if tree.get_node(x).data._completeness == False:
                        #print "the pre is not finished, change it to false"
                        cur_node.data._ready = False
                        break
            if cur_node.is_leaf() == False:
                child = cur_node._fpointer
                node_queue.extend(child)        


        
