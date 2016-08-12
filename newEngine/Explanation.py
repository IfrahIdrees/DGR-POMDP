



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
                   
    def update_forest(self, forest):
        self._forest = forest
        
    def update_pendSet(self, pendingSet):
        self._pendingSet = pendingSet
