import copy

class State():
    """A state is just a collection of variable bindings."""
    def __init__(self):
        pass 
    #here not initialize the name because I need to compare state
    #if they have different name, it will be regarded as different 
    #even though all of their elements are the same.
#         self.__name__ = name
    """This is designed to compare state"""        
    def __eq__(self, other):
        if isinstance(other, self.__class__):    
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
class Method_my_data(): 
        def __init__(self): 
            self._completeness = False
            #record the completeness of the node
            #if children are ordered or unordered, the parent node is completed 
                #when all the children are done
            #if children relation are alternative, the parent node is completed 
                #when one of children is done
            self._childrenrelation = 1
            #define the relation of children
            #children relation = 0, ordered
            #children relation = 1, unordered
            self._completednum = 0
            #the number children
            self._order = 0
            #this has effect only when operators are ordered
            self._start = False
            #record whether this action is triggered
            self._split = False            

class Operator_my_data():
    def __init__(self): 
            self._completeness = False
            #record the completeness of the node
            self._order = 0
            #this has effect only when operators are ordered
class complete_tree():
    def __init__(self, tree, splitlabel):
        self._tree = copy.deepcopy(tree)
        self._splitlabel = splitlabel
        
class prompset():
    def __init__(self, prior_prompt_set, promp_set, tree, splitlabel):
        self._prior_prompt_set = prior_prompt_set
        self._promp_set = promp_set
        self._tree = tree
        self._splitlabel = splitlabel
    