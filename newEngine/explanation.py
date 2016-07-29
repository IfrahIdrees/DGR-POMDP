import sys
from collections import deque
from treelib import Tree
sys.dont_write_bytecode = True


class Explanation(object):
    '''
    def __init__(self):
        self._prob=0
        self._forest=[] #this is a list of TaskNet;
        self._pendingSet=[] #this is list, each element has format of ["action_name", "prob"]
        '''
    
    def __init__(self, v=0, forest=[], pendingSet=[]):
        self._prob = v
        self._forest = forest
        self._pendingSet = pendingSet
    
        
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
    
    
    
    
class TaskNet(object):
    def __init__(self, goalName="", root=Tree(), expandProb = 1, pendingset=[]):
        self._goalName=goalName ##this is the goal name of the tree, it is a string;
        self._root = root
        self._expandProb=expandProb
        self._pendingset = pendingset
        
        #self.root=(some tree node)
        ##a list of actions that are possible for this tree structure


class explaSet(object):
    explaset = deque([])
    def add_exp(self, e):
        self.__class__.explaset.append(e)
    
    ##get an explanation and remove it
    def pop(self):
        return self.explaset.popleft()    
    
    def length(self):
        return len(self.explaset)
        
        
        
        
        
class Operator_my_data():
    def __init__(self, complete = False, ready=False): 
            self._completeness = complete
            ##this information will tell whether this step can be implemented
            ##according to the tree structure
            self._ready = ready  
            
