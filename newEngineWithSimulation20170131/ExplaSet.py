import sys
sys.dont_write_bytecode = True
import copy
from collections import deque
from database import *
from Explanation import *
from helper import *
from TaskHint import *

db = DB_Object()




class explaSet(object):
    def __init__(self, cond_satisfy = 1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001, non_happen = 0.0001):
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger
        self._explaset = deque([])
        self._action_posterior_prob = {} #this is the action level reasoning result from observation
        self._non_happen = non_happen
        #self._start_action = {} #format: {action1: 0, action2:1}, 0 stands has not been execute, 
    
    def add_exp(self, e):
        #print "inside add_exp((((((((((((((((((((((((((((((((((((((((((((((99"
        #print e._prob
        #print self._delete_trigger
        if e._prob > self._delete_trigger:
            self._explaset.append(e)
        #print e._prob > self._delete_trigger
        #self._explaset.append(e)
    
    def pop(self):
        #get an explanation and remove it
        return self._explaset.popleft()    
    
    def length(self):
        return len(self._explaset)
    def get(self, index):
        return self._explaset[len(self._explaset) - index]    
    
    def explaInitialize(self):
        #initialzie the explanation. At very beginning, the explanation is "nothing happend"
        #It's pendingSet is all the start actions of all the method in the database
        goal = db.find_all_method()
        mypendingSet=[]
        mystart_task = {}
        
        for x in goal:
            if len(x["start_action"])>0:
                mystart_task[x["m_name"]] = 0 #this task has not started yet
                for y in x["start_action"]:
                    if [y, 0] not in mypendingSet:
                        mypendingSet.append([y, 0])
                        #self._start_action[y] = 0
                        #mystart_action[y] = 0.append(y)
        ##provide prior prob for each action in the pending set
        prob = float(1)/(len(mypendingSet))
        for x in mypendingSet:
            x[1]=prob
        exp = Explanation(v=1, pendingSet=mypendingSet, start_task = mystart_task)    
            
        
        #exp = Explanation(v=1, pendingSet=mypendingSet, start_action=mystart_action)
        self._explaset.append(exp)
        
    def print_explaSet(self):
        
        for index in range(len(self._explaset)):
            x = self._explaset[index]
            print
            print "--------------Explanation ",(index+1), "------------------"
            print "The probability:                         ", x._prob
            print "The current pending set is:              ", x._pendingSet
            print "The tasks ongoing are:                   ", x._start_task
            #print "The toppest task level explanation is:   "
            for y in x._forest:
                print
                print "Goal Name:                           ", y._goalName
                for actions in y._pendingset:
                    print "The pendingSet for this Goal:    ", actions._pending_actions
                #print y._pendingset._pending_actions[0]
        print
    #Functionality: remove explanations with prob smaller than delete_trigger
    #Normalize the remaining explanations
    def normalize(self):
        '''
        for x in self._explaset:
            if x._prob<=self._delete_trigger:
                self._explaset.
        '''
        leng = len(self._explaset)
        my_sum=0
        for x in self._explaset:
            my_sum=my_sum+x._prob         
        '''
        if self.prior_label==False:
            for x in self._explaset:
                x._prob = x._prob*(float(1)/leng)
                my_sum = my_sum+x._prob
            self.prior_label=True   
        else: ##the priors have already been considered
            for x in self._explaset:
                my_sum = my_sum+x._prob
        '''
        if my_sum == 0.0:
            return       
        for x in self._explaset:
            x._prob = x._prob/my_sum   
########################################################################################    
########################################################################################
    ##calculate the posterior probability of for actions in the pending set#############
########################################################################################
#########################################################################################    
    def action_posterior(self):
        self._action_posterior_prob = {}
        for expla in self._explaset:
            #add actions in pending set
            for action in expla._pendingSet:
                if action[0] in self._action_posterior_prob:
                    self._action_posterior_prob[action[0]] = self._action_posterior_prob[action[0]] + action[1]
                else:
                    self._action_posterior_prob[action[0]] = action[1]
                #self._action_level_expla[action[0]] = 1
            
                    
        print "Now the action_posterior_prob is", self._action_posterior_prob                    
        for k in self._action_posterior_prob:
            print "This k is        ", k
            self._action_posterior_prob[k] = self._action_posterior_prob[k] * self.cal_posterior(k)      
        #print "inside action_posterior(), the _action_level_expla is updated==================="
        #print self._action_posterior_prob
        
    def cal_posterior(self, action):
    
        #print "we want to calculate the posterior for --------------", action
        op = db.get_operator(action)
        #print "the operator is~~~~~~~~~~~~~~~~`"
        #print op   
        
        beforeS = []
        title = []
        for x in op["precondition"]:
            beforeS.append(db.get_object_status(x))
        
        for x in beforeS:
            for y in x:
                if y!="ob_name" and y!="ob_type" and y!="_id":
                    title.append([x["ob_name"], y])     
                    
        #enum: state enumeration       
        enum = self.myDFS(title, beforeS)
        new_prob=self.variable_elim(enum, op, title)
        '''
        if(new_prob<self._delete_trigger):
            return 0.0
        '''     
        return new_prob
    
    
                
    
    
    ##dfs is used to generate the enumeration of all possible
    ##state combinations    
    def myDFS(self, title, beforeS):
        enum = []
        va = []
        self.realMyDFS(enum, va, title, beforeS)
        return enum
    
    def realMyDFS(self, enum, va, title, beforeS):
        if len(va)==len(title):
            enum.append(list(va))
            return ##enum
        key = title[len(va)]
        select_state = [x for x in beforeS if x["ob_name"]==key[0]]
        attr = select_state[0][key[1]]
        for x in attr:
            va.insert(len(va), x)
            ##va.append(x)
            self.realMyDFS(enum, va, title, beforeS)
            va.pop()
            ##va.remove(x)
        
    ##impliment the bayesian network calculation for one possible state
    #op: the operator in knowlege base, prob: the prior of the action
    def variable_elim(self, enum, op, title):
        print "the length for title is=======================", len(title)
        print "the length for enum is========================", len(enum)
        #print enum
        #print "the title is======================"
        #print title
        new_prob_1 = 0 #this action happened
        new_prob_2 = 0 #this action does not happend
        for before in enum:
            for after in enum:
                p = self.bayesian_expand(before, after, op, title)
                new_prob_1 = new_prob_1 + p[0]
                new_prob_2 = new_prob_2 + p[1]
        #print "new_prob_1", new_prob_1
        #print "new_prob_2", new_prob_2        
        return float(new_prob_1)/(new_prob_1+new_prob_2)
        
        
    #sv: an concrete state value, op: the operator in knowledge base
    #state_c: the notification        
    def bayesian_expand(self, before, after, op, title):
        '''
            if op["st_name"] == "rinse_hand":
                print "this is for rinse hand========================"
                print before
                print after
        ''' 
        #calculate p(s_t-1)
   
        ps_before = 1
        for i, s in enumerate(before):
            thisp = db.get_attribute_prob(s, title[i][0], title[i][1])
            ps_before = ps_before*float(thisp)
        '''
        if op["st_name"] == "rinse_hand":    
            print "now ps_before is===================", ps_before    
        '''
        #calculate p(o_t|s_t)
        po_s = 1
        for i, s in enumerate(after):
            thisp = db.get_obs_prob(s, title[i][0], title[i][1])
            po_s = po_s *float(thisp)    
        '''
        if op["st_name"] == "rinse_hand":
            print "now po_s is=======================", po_s
        '''
        #calculate p(s|s_t-1, a_t)
        ps_actANDs_1 = self.get_ps_actANDs_1(before, after, op, title)
        ps_actANDs_2 = self.get_ps_actANDs_2(before, after)
        '''
        if op["st_name"] == "rinse_hand":    
            print "now ps_actANDs_1 is ==============", ps_actANDs_1
            print "now ps_actANDs_2 is ===============", ps_actANDs_2
        '''
        
        prob = []
        #print "ps_before", ps_before
        #print "po_s", po_s
        #print "ps_actANDs_1", ps_actANDs_1
        #print "ps_actANDs_2", ps_actANDs_2
        
        prob.append(float(ps_before)*po_s*ps_actANDs_1)
        prob.append(float(ps_before)*po_s*ps_actANDs_2)
        
        return prob

    #calculate p(s|s_t-1, a_t) happen    
    def get_ps_actANDs_1(self, before, after, op, title):   
        bef = list(before)
        af = list(after)
        #check precondition
        prob = 1
        precond = op["precondition"]
        for ob in precond:
            for attri in precond[ob]:
                index = title.index([ob, attri])
                if attri=="ability":
                    ability_list = bef[index].split(",")
                    if compare_ability(ability_list, precond[ob][attri]) is False:
                        print "return not satisfy because of ability not enough "
                        return self._cond_notsatisfy
                else:
                    if precond[ob][attri]!=bef[index]:
                        return self._cond_notsatisfy
      
        ##check effect
        effect = op["effect"]
        for ob in effect:
            for attri in effect[ob]:
                index=title.index([ob, attri])
                bef[index]=effect[ob][attri]
        if bef!=af:  
            return self._cond_notsatisfy
            
        return self._cond_satisfy


    #calculate p(s|s_t-1, a_t) not happen
    def get_ps_actANDs_2(self, before, after):
        if before==after: return self._cond_satisfy
        else: return self._cond_notsatisfy


#########################################################################################
#########################################################################################
###############expand the explanation Set, each explanation can be extended into multiple explanations. Based on which actions has happened###############################
#########################################################################################
#########################################################################################
    '''
    def explaSet_expand(self):
        #print "inside explaSet_expand"
        #print self._action_posterior_prob
        length = self.length()
        #print "inside explaSet_expand, the length is", self.length()
        for i in range(length):
            x = self.pop()
            
            for action in self._action_posterior_prob:
                #case1: nothing happened: update the prob of the explanation, 
                #do not need to update tree structure. 
                if action == "nothing":
                    newstart_task = copy.deepcopy(x._start_task)
                    newexpla = Explanation(v=x._prob*self._action_posterior_prob[action], forest = x._forest, pendingSet = x._pendingSet, start_task = newstart_task)
                    self.add_exp(newexpla) 
                else:
                #case2:something happend, need to update the tree structure
                    #print "this action is", action
                    #print "the prob of this action is", self._action_posterior_prob[action]                    
                    new_explas = x.generate_new_expla([action, self._action_posterior_prob[action]])
                    #print "after generate new, the result is!!!!"
                    #print new_explas
                    for expla in new_explas:
                        #print "the prob is", expla._prob
                        #print "the start task is", expla._start_task
                        self.add_exp(expla)
     ''' 
    ##"explaSet_expand_part1" is used to generate explanations that add a new tree structure, a bottom-up process
    ##The bottom-up process depend on the previous state.     
    def explaSet_expand_part1(self, length):
        for i in range(length):
            x =   self.get(i+1)
            for action in self._action_posterior_prob:
                #case1: nothing happened: update the prob of the explanation, 
                #do not need to update tree structure. 
                if action == "nothing":
                    newstart_task = copy.deepcopy(x._start_task)
                    newexpla = Explanation(v=x._prob*self._action_posterior_prob[action], forest = x._forest, pendingSet = x._pendingSet, start_task = newstart_task)
                    self.add_exp(newexpla)
                                 
                else:
                    #case2:something happend, need to update the tree structure
                    #print "this action is", action
                    #print "the prob of this action is", self._action_posterior_prob[action]                    
                    new_explas = x.generate_new_expla_part1([action, self._action_posterior_prob[action]])
                    #print "after generate new, the result is!!!!"
                    #print new_explas
                    for expla in new_explas:
                        #print "the prob is", expla._prob
                        #print "the start task is", expla._start_task
                        #only those explanations with prob bigger than self._delete_trigger
                        #can be added into the explanation queue
                        self.add_exp(expla)
                        
        
        return
    ##"explaSet_expand_part2" is used to generate explanations by decomposing an existing tree structure. , a top-down process
    ##The top=down process depends on the current state. (after adding the effect of just happened action)
                        
    def explaSet_expand_part2(self, length):
        for i in range(length):
            x =   self.pop()
            for action in self._action_posterior_prob:
                if action == "nothing":
                    continue
                
                #case2:something happend, need to update the tree structure
                #print "this action is", action
                #print "the prob of this action is", self._action_posterior_prob[action]                    
                new_explas = x.generate_new_expla_part2([action, self._action_posterior_prob[action]])
                #print "after generate new, the result is!!!!"
                #print new_explas
                for expla in new_explas:
                    #print "the prob is", expla._prob
                    #print "the start task is", expla._start_task
                    self.add_exp(expla)          
        return
                
    '''                  
    def explaSet_expand1(self):
        length = self.length() 
        for i in range(length):
            x = self.pop()  #get an explanation and remove it
            act_expla = self.action_level_explanation(x._pendingSet)
        for y in act_expla:
            #case1: nothing happened: update the prob of the explanation, 
            #do not need to update tree structure. 
            if y[0]=="nothing":
                newexpla = Explanation(v=x._prob*y[1], forest = x._forest, pendingSet = x._pendingSet, start_action = x._start_action)
                self.add_exp(newexpla) 
                #v=0, forest=[], pendingSet=[]
            #case2:something happend, need to update the tree structure as well
            else:
                new_explas = x.generate_new_expla(y)
                for expla in new_explas:
                    self.add_exp(expla)
                #generate_new_expla(y, x)

        return
        '''


    #calculate the prob of nothing happen, 
    #normalize on something happen
    #delete action with prob<delete_trigger    
    def action_level_explanation(self, pendingset):
        nothing_happen = 1
        prob_sum = 0
        ##calculate the prob of nothing happen
        for x in pendingset:
            prob_sum = prob_sum + x[1]
            nothing_happen = nothing_happen*(1-x[1])
        #print "nothing happend is", nothing_happen
        
        ##normalize the prob of something happen prob
        act_expla = []
        some_happen = 1-nothing_happen
        act_expla.append(["nothing", nothing_happen])
        for x in pendingset:
            if prob_sum==0.0 or some_happen==0.0:
                act_expla.append([x[0], 0.0])
            else:
                act_expla.append([x[0], x[1]/prob_sum*some_happen])
        
        ##delete some action whose prob<delete_trigger and normalize
        act_expla = [x for x in act_expla if x[1]>=self._delete_trigger]
        act_expla = my_normalize(act_expla)
        
        return act_expla    

            
#########################################################################################
#########################################################################################
###############generate the pending set for each explanation############################
###############based on the current tree structure #####################################
#########################################################################################
#########################################################################################            
    def pendingset_generate(self):
        self.normalize()
        for expla in self._explaset:
            expla.create_pendingSet()
           



#########################################################################################
#########################################################################################
###############Calculate the probability of node in each explanation, and output the probabilities of tasks, and average level...........#####################################
#########################################################################################
######################################################################################### 
    def task_prob_calculate(self):
        #print "go into task prob _calculate"
        taskhint = TaskHint()
        taskhint.reset()
        for expla in self._explaset:
            expla.generate_task_hint(taskhint)
        ##taskhint = TaskHint()
        taskhint.average_level()
        #taskhint.print_taskhint()    


            
