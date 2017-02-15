import sys
sys.dont_write_bytecode = True
from termcolor import colored
import copy
from treelib import Tree
from treelib import Node
from TaskNet import *
from Node_data import *
from database import *
from helper import *
from TaskHint import *
from ExecuteSequence import *

db = DB_Object()

class Explanation(object):
    '''
    def __init__(self):
        self._prob=0
        self._forest=[] #this is a list of TaskNet;
        self._pendingSet=[] #this is list, each element has format of ["action_name", "prob"]
        '''
    
    def __init__(self, v=0, forest=[], pendingSet=[], start_task = {}):
        self._prob = v
        self._forest = forest
        self._pendingSet = pendingSet
        self._start_task = start_task #format {task1: 0, task2:1}, 0 stands for not started yet, 1 stands for ongoing
    
        
    def set_prob(self, v):
        self._prob = v
        
    def set_forest(self, forest):
        self._forest = forest
     
    def set_pendingSet(self, pendingset):
        self._pendingSet = list(pendingset)   
    
    def add_tasknet_ele(self, tasknet):
        self._forest.append(tasknet)
    
    def add_pendSet_ele(self, val):
        self._pendingSet.append(val)
                   
    def update_forest(self, forest):
        self._forest = forest
        
    def update_pendSet(self, pendingSet):
        self._pendingSet = pendingSet


    
    
#########################################################################################
#########################################################################################
###############generate new explanations based on one action###############################
#########################################################################################
#########################################################################################    
    #use to udpate the current explanation according to the input action_explanation
    #act_expla is the explanation for this observation, expla is the current explanation
    ##"egenerate_new_expla_part1" is used to generate explanations that add a new tree structure, a bottom-up process
    ##The bottom-up process depend on the previous state.     
    def generate_new_expla_part1(self, act_expla):
        new_explas = []
        #print "go into this function -----------------------!!!!!!!!!!!!!!!11"
        #exp = explaSet()
        find = False
        
        ##Case1 : drop an on-going unfinished task, start a new one. 
        tempstart_task = copy.deepcopy(self._start_task) 
        for start_task in tempstart_task:
            #print "check start_ task",start_task, act_expla[0]
            if tempstart_task[start_task] == 0: #inside this explanation, "start_task" has not been started
                target_method = db.find_method(start_task)
                if act_expla[0] in target_method["start_action"]:
                    #print "it is in start action"
                    find = True
                    #newstart_task = 
                    #self._start_task[start_task] = 1
                    newTaskNets = self.initialize_tree_structure(act_expla[0])
                    #print "the length of tasknet is", len(newTaskNets)
                    for g in newTaskNets:
                        #print "this tasknet", g._expandProb
                        #print "act prob", act_expla[1]
                        #print "original expla prob", self._prob
                        if tempstart_task[g._goalName] == 0:
                            tempstart_task[g._goalName] = 1
                            newstart_task = copy.deepcopy(self._start_task)
                            prob = act_expla[1]*g._expandProb*self._prob
                            if g._complete == True:
                                #newstart_task = list(self._start_task)
                                newstart_task[g._goalName] = 0
                                newexp = Explanation(v=prob, forest = list(self._forest), start_task=newstart_task)
                            else:
                                newforest = list(self._forest)
                                newforest.append(g)
                                newstart_task[g._goalName] = 1
                                #newstart_task = copy.deepcopy(self._start_task)
                                newexp = Explanation(v=prob, forest = newforest, start_task=newstart_task)
                            new_explas.append(newexp)
         
        if find==False:
            '''
            print colored('dangerous action, cannot figure out what the person is doing now', 'red'), act_expla[0]
            '''
            #print "dangerous action, cannot figure out what the person is doing now"
            #sys.exit(0)
            """
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
        return new_explas
        
    #use to udpate the current explanation according to the input action_explanation
    #act_expla is the explanation for this observation, expla is the current explanation
    ##"generate_new_expla_part2" is used to generate explanations by decomposing an existing tree structure. , a top-down process
    ##The top=down process depends on the current state. (after adding the effect of just happened action)
    def generate_new_expla_part2(self, act_expla):
        #print "Inside Explanation.py generate_new_expla", act_expla
        new_explas = []
        #print "go into this function -----------------------!!!!!!!!!!!!!!!11"
        #exp = explaSet()
        find = False
        ##Case2 : continue on an on-going task
            ##update existing tree structure, if the action exist in the 
            ##pending set of this tree structure
        for taskNet in self._forest:
            for taskNetPending in taskNet._pendingset:
                #print "Explanation.py, generate_new_expla(), the tasknetPending._pending_action:"
                #print taskNetPending._pending_actions
                if act_expla[0] in taskNetPending._pending_actions: 
                    #print "action exist in pending set"
                    find = True
                    
                    #get a new taskNet start
                    theTree = copy.deepcopy(taskNetPending._tree)
                    action_node = theTree.get_node(act_expla[0])
                    action_node.data._completeness = True
                    executed_sequence = ExecuteSequence(sequence = copy.deepcopy(taskNet._execute_sequence._sequence), effect_summary = copy.deepcopy(taskNet._execute_sequence._effect_summary))
                    executed_sequence.add_action(act_expla[0])
                    
                    #newTaskNet = taskNetPending.generate_new_taskNet(act_expla[0])
                    newTaskNet = TaskNet(goalName = theTree.get_node(theTree.root).tag, tree = theTree, expandProb = taskNetPending._branch_factor, execute_sequence = executed_sequence)
                    newTaskNet.update()
                    #get a new taskNet end
                    
                    newforest = list(self._forest)
                    newforest.remove(taskNet)
                    prob = act_expla[1]*newTaskNet._expandProb*self._prob
                    
                        ##this goal has already been completed
                        ##remove it and add its start action into 
                        ##the explanation start action list
                    if newTaskNet._complete==True:
                        newstart_task = copy.deepcopy(self._start_task)
                        newstart_task[newTaskNet._goalName] = 0
                        #newstart_action = list(self._start_action)
                        #newstart_action.append(db.get_start_action(newTaskNet._goalName))
                        newexp = Explanation(v=prob, forest = newforest, start_task=newstart_task)
                        
                        ##this goal has not been completed
                    else:
                        newforest.append(newTaskNet)
                        newstart_task = copy.deepcopy(self._start_task)
                        newexp = Explanation(v=prob, forest = newforest, start_task=newstart_task)
                    
                    new_explas.append(newexp)             
        if find==False:
            '''
            print colored('dangerous action, cannot figure out what the person is doing now', 'red'), act_expla[0]
            #sys.exit(0)
            '''
            """
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
        return new_explas
        
        
        
        
        
        
    ##generate a tree structure for the action_explanation
    ##this function is called only when the _forest parameter is null
    ##(with length of 0)
    ##Input: is only the action name (probability is not included)
    def initialize_tree_structure(self, action):
        task_net = []
        temp_forest = deque([])
        tree = Tree()
        opdata = Node_data(complete = True)
        tree.create_node(action, action, data=opdata)
        #tree.create_node(action, uuid.uuid4(), data=opdata)
        temp_forest.append([tree, 1])     
        
        while temp_forest:
            length = len(temp_forest)
            for i in range(length):
                thisTree = copy.deepcopy(temp_forest.popleft())
                #print "the probability for branch factor is fsdfdsfs", thisTree[1]
                tag = thisTree[0].get_node(thisTree[0].root).tag
                parents = db.get_parent_list(tag)
                if parents==False: print "error happend here please check"
                if len(parents)>0: 
                    for x in parents: #x must be an method
                        method = db.find_method(x)
                        decompose_choose = self.method_precond_check(method,tag)
                        for decompose in decompose_choose:
                            #print "the decompose is", decompose[0]
                            decompose[0]=thisTree[1]*decompose[0]
                            temptree = copy.deepcopy(thisTree[0])
                            temp_forest.append(self.my_create_new_node(x, decompose, temptree))
        
                elif len(parents)==0: #this tree already reached goal node
                    executed_sequence = ExecuteSequence(sequence = [], effect_summary = {})
                    executed_sequence.add_action(action)
                    my_goal = TaskNet(goalName=tag, tree=thisTree[0], expandProb=thisTree[1], execute_sequence = executed_sequence)
                    my_goal.update()
                    task_net.append(my_goal)
        
        return task_net        



    def method_precond_check(self, method, child):
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
        ##Step 3: return all the branches that include the specified child
        satisfy_branch = []
        #print method["subtasks"]
        #print "the check child is ", child
        for i, x in enumerate(method["subtasks"]):
            #print x
            find=False
            for y in x:
                if y==child:
                    find=True
            #find the child in this branch, attach it into the satisfy_branh 
            if find==True:
                satisfy_branch.append([prob[i], x])        
        return satisfy_branch    

       
    def my_create_new_node(self, parent, decompose, childTree):
        newTree = Tree()
        parent_data = Node_data(complete=False, ready = True, branch = True)
        #newTree.create_node(parent ,uuid.uuid4(), data=parent_data)
        newTree.create_node(parent, parent, data=parent_data)
        
        known_child = childTree.get_node(childTree.root)
        #print "the know child is", known_child
        #print decompose[1]
        for x in decompose[1]:
            #print x
            
            if x==known_child.tag:
                known_child.data._pre = decompose[1][x]["pre"]
                known_child.data._dec = decompose[1][x]["dec"]
                newTree.paste(newTree.root, childTree)
            else:
                mydata = Node_data(pre=decompose[1][x]["pre"], dec=decompose[1][x]["dec"])
                newTree.create_node(x, x, parent=newTree.root, data= mydata)
        
        #newTree.show(line_type = "ascii")
        #print "the probability for this decompose is", decompose[0]
        return [newTree, decompose[0]]   




#########################################################################################
#########################################################################################
###############generate the pending set for each explanation############################
###############based on the current tree structure #####################################
#########################################################################################
#########################################################################################

    def create_pendingSet(self):      
        if len(self._pendingSet)==0:
            self.set_pendingSet(self.real_create_pendingSet())
        else:
            self.set_pendingSet(self.normalize_pendingSet_prior())
        



                
    def real_create_pendingSet(self):
        #print expla._prob
        pendingSet = set()
        for taskNet in self._forest:
            for taskNetPending in taskNet._pendingset:
                for action in taskNetPending._pending_actions:
                    pendingSet.add(action)
        
        #if currently the pending set has no action, need to initialize from start tasks
        if len(pendingSet)==0:
            for start_task in self._start_task:
                if self._start_task[start_task] == 0:
                    theMethod = db.find_method(start_task)
                    for y in theMethod["start_action"]:
                        pendingSet.add(y)
        
            
        '''            
        for action in self._start_action:
            pendingSet.add(action)
        '''
        pendingSet1 = []
        prior = float(1)/len(pendingSet)
        for x in pendingSet:
            pendingSet1.append([x, self._prob*prior])
        
        return pendingSet1
        
        
    def normalize_pendingSet_prior(self):
        pendingSet =  self._pendingSet
        prior = float(1)/len(pendingSet)
        for x in pendingSet:
            x[1]=self._prob*prior
        
        return pendingSet 


#########################################################################################
#########################################################################################
###############generate task hint in levels #####################################
#########################################################################################
######################################################################################### 
    def generate_task_hint(self, taskhint):

        #########step1--------------------------------------
        ##get all node and their levels from this explanation's forest
        ##all those node should share the same prob.
        task_Name_Level = {}
        if len(self._forest)==0:
            task_Name_Level = {"nothing":[]}
        else:
            for taskNet in self._forest:
                for taskNetPending in taskNet._pendingset:
                    node_list = taskNetPending._tree.all_nodes()
                    #taskNetPending._tree.show(line_type = "ascii")
                    
                    #only select nodes whose completeness is False, and readiness is True
                    node_list = [x for x in node_list if x.data._completeness==False and x.data._ready==True]
                    
                    for node in node_list:
                        level_num = taskNetPending._tree.depth(node)
                        if node._tag in task_Name_Level.keys():
                            level_list = task_Name_Level.get(node._tag)
                            level_list.append(level_num)
                            new_dict = {node._tag:level_list}
                            task_Name_Level.update(new_dict)
                        else:
                            level_list = []
                            level_list.append(level_num)
                            new_dict = {node._tag:level_list}
                            task_Name_Level.update(new_dict)
   
        ###########Step2----------------------------------------------
        ##add the task_Name_Level dict to the TaskHint 
                               
        ##taskhint = TaskHint()
        ##taskhint.reset()
        for k,v in task_Name_Level.items():
            #print "this key is", k
            #print "this value is", v
            #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&77"
            taskhint.add_task(task_tag=k, expla_prob=self._prob, level = v)
        ##taskhint.print_taskhint()
                   
    
    ##################################################################################################
    ###         exception handling
    ##################################################################################################

    def repair_expla(self, sensor_notification):
        print 
        print "inside Explanation.py function: repair_expla"
        update_belief_state = False
        print "the length of forest is: ", len(self._forest)
        for taskNet in self._forest:
            label = taskNet.repair_taskNet(sensor_notification)
            if label == True:
                update_belief_state = True    
        
        if update_belief_state is True:
            return self._prob
        else:
            return 0.0
       
            
        
             
        


            
