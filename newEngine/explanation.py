


class Explanation(object):
    def __init__(self):
        self._prob=0
        self._forest=[] #this is a list of TaskNet;
        self._pendingSet=[] #this is list, each element has format of ["action_name", "prob"]
        
    def set_prob(self, v):
        self._prob = v 
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
    def __init__(self):
        self.goalName="" ##this is the goal name of the tree, it is a string;
        #self.root=(some tree node)
        ##a list of actions that are possible for this tree structure


class explaSet(object):
    explaset = []
    def add_exp(self, e):
        self.__class__.explaset.append(e)
    
        
        
