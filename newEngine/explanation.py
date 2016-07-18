


class Explanation(object):
    def __init__(self):
        self._prob=0
        self._forest=[] #this is a list of TaskNet;
        self.pendingSet={} #this is dict, each one with goalName:actionName 

class TaskNet(object):
    def __init__(self):
        self.goalName="" ##this is the goal name of the tree, it is a string;
        self.root=(some tree node)
        ##a list of actions that are possible for this tree structure
      
