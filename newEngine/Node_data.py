import sys
sys.dont_write_bytecode = True

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
