import sys
sys.dont_write_bytecode = True
import copy
from collections import deque
from database import *
from Explanation import *
from helper import *

db = DB_Object()




class explaSet(object):
    explaset = deque([])
    #the prior_label is used to guarantee that the priors 
    #of goals are calculated only once
    prior_label = False
    
    def __init__(self, cond_satisfy = 1.0, cond_notsatisfy = 0.0):
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
    
    
    def add_exp(self, e):
        self.__class__.explaset.append(e)
    
    ##get an explanation and remove it
    def pop(self):
        return self.explaset.popleft()    
    
    def length(self):
        return len(self.explaset)
    
    
    ##initialzie the explanation
    def explaInitialize(self):
        #if has been initialized, just return
        if self.__class__.prior_label is True:
            return
        #If has not, firstly put it into true
        self.__class__.prior_label=True
        
        goal = db.find_all_method()
        mypendingSet=[]
        mystart_action = []
        
        for x in goal:
            if len(x["start_action"])>0:
                for y in x["start_action"]:
                    if [y, 0] not in mypendingSet:
                        mypendingSet.append([y, 0])
                        mystart_action.append(y)
        ##provide prior prob for each action in the pending set
        prob = float(1)/(len(mypendingSet))
        for x in mypendingSet:
            x[1]=prob
        
        exp = Explanation(v=1, pendingSet=mypendingSet, start_action=mystart_action)
        self.__class__.explaset.append(exp)
        
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
########################################################################################    
########################################################################################
    ##calculate the posterior probability of for actions in the pending set#############
########################################################################################
#########################################################################################    
    def action_posterior(self):
        for expla in self.__class__.explaset:
            for action in expla._pendingSet:
                '''considered action priors here action[1]'''
                action[1]=action[1]*self.cal_posterior(action)
    
    def cal_posterior(self, action):
        op = db.get_operator(action[0])
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
            return enum
        key = title[len(va)]
        select_state = [x for x in beforeS if x["ob_name"]==key[0]]
        attr = select_state[0][key[1]]
        for x in attr:
            va.append(x)
            self.realMyDFS(enum, va, title, beforeS)
            va.remove(x)
        
    ##impliment the bayesian network calculation for one possible state
    #op: the operator in knowlege base, prob: the prior of the action
    def variable_elim(self, enum, op, title):
        new_prob_1 = 0 #this action happened
        new_prob_2 = 0 #this action does not happend
        for before in enum:
            for after in enum:
                p = self.bayesian_expand(before, after, op, title)
                new_prob_1 = new_prob_1 + p[0]
                new_prob_2 = new_prob_2 + p[1]
        return float(new_prob_1)/(new_prob_1+new_prob_2)
        
        
    #sv: an concrete state value, op: the operator in knowledge base
    #state_c: the notification        
    def bayesian_expand(self, before, after, op, title):
        #calculate p(s_t-1)
        ps_before = 1
        for i, s in enumerate(before):
            thisp = db.get_attribute_prob(s, title[i][0], title[i][1])
            ps_before = ps_before*float(thisp)
        
        #calculate p(o_t|s_t)
        po_s = 1
        for i, s in enumerate(after):
            thisp = db.get_obs_prob(s, title[i][0], title[i][1])
            po_s = po_s *float(thisp)    
        
        #calculate p(s|s_t-1, a_t)
        ps_actANDs_1 = self.get_ps_actANDs_1(before, after, op, title)
        ps_actANDs_2 = self.get_ps_actANDs_2(before, after)
        
        prob = []
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


###################################################################################
###################################################################################
###############update state belief according to action posteriors##################
###################################################################################
###################################################################################


    


            
            








    
            
            
            
