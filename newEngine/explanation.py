import sys
import copy
from collections import deque
from treelib import Tree
from treelib import Node
from database import *
from helper import *


sys.dont_write_bytecode = True
db = DB_Object()

class Explanation(object):
    '''
    def __init__(self):
        self._prob=0
        self._forest=[] #this is a list of TaskNet;
        self._pendingSet=[] #this is list, each element has format of ["action_name", "prob"]
        '''
    
    def __init__(self, v=0, forest=[], pendingSet=[], start_action = []):
        self._prob = v
        self._forest = forest
        self._pendingSet = pendingSet
        self._start_action = start_action
    
        
    def set_prob(self, v):
        self._prob = v
        
    def set_forest(self, forest):
        self._forest = forest
     
    def set_pendingSet(self, pendingset):
        self._pendingSet = pendingset   
    
    
         
    def add_tasknet_ele(self, tasknet):
        self._forest.append(tasknet)
    
    def add_pendSet_ele(self, val):
        self._pendingSet.append(val)
        #self._pendingSet[key]=val           
    def update_forest(self, forest):
        self._forest = forest
    def update_pendSet(self, pendingSet):
        self._pendingSet = pendingSet
    
    
    
class TaskNetPendingSet(object):
    def __init__(self, tree = Tree(), branch_factor = 1, pending_actions = []):
        self._tree = tree
        self._branch_factor = branch_factor
        self._pending_actions = pending_actions


    
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
        rootnode = self._tree.get_node(self._tree.root)
        #update completeness
        
        complete_update(rootnode, self._tree)
        if rootnode.data._completeness == True:
            self._complete=True
            return
        
        #update ready-ness
        readiness_update(self._tree.root, self._tree)
        
        #update pendingset
        self._pendingset = pendingset_update(self._tree.root, self._tree)
        

#update pending set
#pendingset is a list, each element has the format of 
#[tree, action, new_added branch prob compared with the initial tree]
def pendingset_update(node, tree):
    expand_tree = []
    tree_queue = deque([])
    tree_queue.append([tree, 1])
    while tree_queue:
        thisTree = tree_queue.popleft()
        leaves = thisTree[0].leaves()
        finish = True #to check if the tree finished its decomposition process
        #for each node:
        #if it is a leaf node, check
            #
        for leaf in leaves:
            if leaf.data._ready==True:
                method = db.find_method(leaf.tag)
                if method==None: 
                    #print "this leaf is an step, not method:   ", leaf.tag
                    continue
                else:
                    finish = False
                    #print "this leaf is a method     ", leaf.tag
                    branches = method_decompose(method)
                    for x in branches:
                        newTree = copy.deepcopy(thisTree[0])
                        add_child(newTree, leaf.tag, x[1])
                        tree_queue.append([newTree, thisTree[1]*x[0]])
                    break
                    
        if finish==True:
            tree_pending=[x.tag for x in leaves if x.data._ready==True and x.data._completeness==False]
            #print "the new pending set is ", tree_pending
            thisTree.append(tree_pending)
            
            mytasknetpending = TaskNetPendingSet(tree = thisTree[0], branch_factor = thisTree[1], pending_actions = thisTree[2])
            
            expand_tree.append(mytasknetpending)
    return expand_tree
    
    
    
    
def method_decompose(method):
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
    

def add_child(tree, node_id, branch):
    #print "the target node is", node_id
    #print "the branch is", branch
    for x in branch:
        #print "this action is   ", x
        mydata=None
        if len(branch[x]["pre"]) == 0:
            mydata=Node_data(ready=True, branch = False, pre=branch[x]["pre"], dec = branch[x]["dec"])
        else:
            mydata=Node_data(ready=True, branch = False, pre=branch[x]["pre"], dec = branch[x]["dec"])
        
        tree.create_node(x, x, parent = node_id, data = mydata)
        #print "the length is", len(branch[x]["pre"])
        #print branch[x]["pre"]

#complete = False, ready=False, branch = False, pre="", dec=""
#mydata = Node_data(pre=decompose[1][x]["pre"], dec=decompose[1][x]["dec"])
        #    newTree.create_node(x, x, parent=newTree.root, data= mydata)

        
#update completeness
def complete_update(node, tree):
    
        
    if node.is_leaf(): return node.data._completeness
    child = node._fpointer #get the id of childrens
    for x in child:
        if complete_update(tree.get_node(x), tree): continue
        else:
            node.data._completeness = False
            return False
    
    node.data._completeness = True
    
    return True
    
#update readiness
#idea: from top to bottom, BFS
def readiness_update(root_id, tree):
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
            for x in pre_list:
                if tree.get_node(x).data._completeness == False:
                    cur_node.data._ready = False
                    break
        if cur_node.is_leaf() == False:
            child = cur_node._fpointer
            node_queue.extend(child)
     
        


    


class explaSet(object):
    explaset = deque([])
        #the prior_label is used to guarantee that the priors 
        #of goals are calculated only once
    prior_label = False
    def add_exp(self, e):
        self.__class__.explaset.append(e)
    
    ##get an explanation and remove it
    def pop(self):
        return self.explaset.popleft()    
    
    def length(self):
        return len(self.explaset)
    
    def print_explaSet(self):
        
        for x in self.explaset:
            print "--------------------------------"
            print "the explanation probability is:::: ", x._prob
            #print x._forest
            print "the current pending set is::", x._pendingSet
            print "the start action is", x._start_action
            print "~~~~~~~the tree structures are:"
            for y in x._forest:
                print "the goal name is:::", y._goalName
                for actions in y._pendingset:
                    print actions._pending_actions
                #print y._pendingset._pending_actions[0]
   
   
    def normalize(self):
        leng = len(self.explaset)
        my_sum=0
        for x in self.explaset:
            my_sum=my_sum+x._prob         
        '''
        if self.prior_label==False:
            for x in self.explaset:
                x._prob = x._prob*(float(1)/leng)
                my_sum = my_sum+x._prob
            self.prior_label=True   
        else: ##the priors have already been considered
            for x in self.explaset:
                my_sum = my_sum+x._prob
        '''       
        for x in self.explaset:
            x._prob = x._prob/my_sum
        
        
        
class Node_data():
    def __init__(self, complete = False, ready=False, branch = False, pre="", dec=""): 
            self._completeness = complete #complete or not
            ##this information will tell whether this step can be implemented
            ##according to the tree structure
            self._ready = ready #can be implemented in the next step or not
            self._pre = pre #its predecessors
            self._dec = dec #its decedants
            self._branch = branch #if the branching prob for this node has been considered
    
    #out put all the properties of the data instance
    def print_property(self):
        print "completeness:", self._completeness
        print "ready       :", self._ready
        print "predecessors:", self._pre
        print "decedants   :", self._dec
        print "branch fac  :", self._branch
    
        

class Method_my_data():
    def __init__(self, complete = False, ready=False, pre=[], dec=[]): 
            self._completeness = complete
            ##this information will tell whether this step can be implemented
            ##according to the tree structure
            self._ready = ready 
            self._pre = pre
            self._dec = dec            
            
    def setParamter(self, complete=False, ready=False, pre=[], dec=[]):
            self._completeness = complete
            ##this information will tell whether this step can be implemented
            ##according to the tree structure
            self._ready = ready 
            self._pre = pre
            self._dec = dec      
            
            
            
            
