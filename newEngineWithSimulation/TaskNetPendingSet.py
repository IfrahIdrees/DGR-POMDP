import sys
sys.dont_write_bytecode = True

from treelib import Tree
from treelib import Node
from TaskNet import *


class TaskNetPendingSet(object):
    def __init__(self, tree = Tree(), branch_factor = 1, pending_actions = []):
        self._tree = tree
        self._branch_factor = branch_factor
        self._pending_actions = pending_actions
   
   
    #the action exist in the pending_actions of the TaskNetPendingSet,
    #and now this action has happened. generate a new TaskNet based on 
    #this decomposition.
    def generate_new_taskNet(self, action):
        theTree = self._tree
        action_node = theTree.get_node(action)
        action_node.data._completeness = True
        newTaskNet = TaskNet(goalName = tree.get_node(tree.root).tag, tree = theTree, expandProb = taskNetPendingSet._branch_factor)
        newTaskNet.update()
        return newTaskNet
