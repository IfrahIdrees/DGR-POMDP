"""------------------------------------------------------------------------------------------
Most part of this file is borrowed from "Bayesian Affect Control Theory"
Written by Jesse Hoey  jhoey@cs.uwaterloo.ca   http://www.cs.uwaterloo.ca/~jhoey 
----------------------------------------------------------------------------------------------"""

import numpy as np
import math
from numpy import linalg as LA
from bayesact.bayesactemot import *
import getopt
#sys.path.append("/home/d97wang/workspace/CS886/online_Recog_withemotion/bayesact/")
#sys.path.append("/home/d97wang/workspace/CS886/online_Recog_withemotion/bayesact/gui/")


class HierarAssistant(object):
    def __init__(self, args):
        
        self.fbfname ="bayesact/fbehaviours.dat"
        
        self.fifname="bayesact/fidentities.dat"     #identities file
        self.agent_gender="female"         # agent gender
        self.client_gender="male"          # client gender
        self.num_samples = 500
        self.gammae_value = 0.1            #for emotional agent - gamma value for observations of emotion???????
                                           # what's the difference between gammae and gamma
        self.gamma_value = 0.1             #the observation noise (set to 0-0.05 to mimic INTERACT)                          
        self.bvagent = 0.0001
        self.bvclient = 0.0001               #agent's belief about the client's ability to change identities - 
                                           #higher means it will shape-shift more
        self.agent_knowledge=2             #agent knowledge of client id:
                                              #0 : nothing
                                              #1 : one of a selection of  num_confusers+1 randoms
                                              #2 : exactly - use this to mimic interact
                                              #3 : same as 0 but also agent does not know its own id
        self.agent_id="tutor"              #possibly set the agent id to be something
        self.client_id = "elder"           #possibly set the client id to be something
        self.roughening_noise=self.num_samples**(-1.0/3.0) 
        self.use_pomcp=False               #use pomcp for planning (default use heuristic/greedy method)
        self.initial_turn="client"          #who goes first?
        self.last_prompt = []               #initially the last_prompt is None
        self.numcact=5                     #parameters for pomcp
                                              #number of continuous actions we wish to sample -
                                              #this is user-defined and is an important parameter
                                              #larger numbers mean bigger, slower, more accurate,  planning trees
        self.numdact=1                     #number of discrete (propositional) actions
                                           #this should be set according to the domain, and is 1 for this generic class
                                           #one discrete action really means no choice
        self.obsres=1.0                    #observation resolution when building pomcp plan tree
        self.actres=0.1                    #action resolution when buildling pomcp plan tree
        self.timeout=5.0                   #timeout used for POMCP
        
        self.learn_verbose=False           #do we print out all the samples each time
        self.plotter=None
        self.fbehaviours_agent=readSentiments(self.fbfname,self.agent_gender)
        #args is a python dict, store all the changeable parameters
        #---------------can change specific parameters from here-----------------------
        #-------------------------------------------------------------not completed yet
        
        for x in args:
            print args[x]
        #--------------------
        
        (agent_mean_ids,agent_cov_ids)=getIdentityStats(self.fifname,self.agent_gender)
        (client_mean_ids,client_cov_ids)=getIdentityStats(self.fifname,self.client_gender)        
        #the actual (true) ids drawn from the distribution over ids, if not set to something in particular
        self.agent_id=getIdentity(self.fifname,self.agent_id,self.agent_gender)
        if self.agent_id==[]:
            self.agent_id=NP.random.multivariate_normal(agent_mean_ids,agent_cov_ids)
        self.agent_id=NP.asarray([self.agent_id]).transpose()
        #print self.agent_id
        
        #here we get the identity of the client *as seen by the agent*
        self.client_id=getIdentity(self.fifname,self.client_id,self.agent_gender)
        if self.client_id==[]:
            self.client_id =  NP.random.multivariate_normal(client_mean_ids,client_cov_ids)
        self.client_id=NP.asarray([self.client_id]).transpose()
        #print self.client_id
        
        #get initial sets of parameters for agent
        (learn_tau_init,learn_prop_init,learn_beta_client_init,learn_beta_agent_init)=init_id(self.agent_knowledge,self.agent_id,self.client_id,client_mean_ids)
        
        #define these attributes for class
        self.learn_beta_client_init = learn_beta_client_init
        self.learn_beta_agent_init = learn_beta_agent_init
        self.learn_tau_init = learn_tau_init
        self.learn_prop_init = learn_prop_init
        
        ##initialize the agent
        self.learn_agent = EmotionalAgent(N=self.num_samples,alpha_value=1.0,
                                       gammae_value=self.gammae_value, gamma_value=self.gamma_value,
                                       beta_value_agent=self.bvagent,beta_value_client=self.bvclient,
                                       beta_value_client_init=self.learn_beta_client_init,beta_value_agent_init=self.learn_beta_agent_init,
                                       client_gender=self.client_gender,agent_gender=self.agent_gender,
                                       agent_rough=self.roughening_noise,client_rough=self.roughening_noise,use_pomcp=self.use_pomcp,
                                       init_turn=self.initial_turn,numcact=self.numcact,numdact=self.numdact,obsres=self.obsres,
                                       actres=self.actres,pomcp_timeout=self.timeout)
                                       
        self.learn_avgs=self.learn_agent.initialise_array(self.learn_tau_init,self.learn_prop_init,self.initial_turn)
        self.learn_avgs = self.learn_agent.getAverageState()
        
    def update_after_client(self, learn_observ, emotion):
        #the "learn_observ" is the observed behaviour of the patient (client)
        #the "emotion" is the observed emotion label of the patient (client), 
        #   it is a String
        print "the client action is", learn_observ, "emotion is", emotion
        #set the current turn to be client
        learn_xobserv = [0]   #0 stands for client turn, 1 stands for agent turn

        #print "|||||||||||||||before the client's action, the state and emotion is: "
        self.learn_avgs.print_val()
        
        agentEmotion = self.learn_agent.expectedEmotion("agent")  ##don't understand here, how to calculate emotion???????????????????
        clientEmotion = self.learn_agent.expectedEmotion("client")   ##get client emotion
        clientEmotionLabel = self.learn_agent.findNearestEmotion(clientEmotion)
        #print "agent is feeling: ",agentEmotion," which is : ",self.learn_agent.findNearestEmotion(agentEmotion)
        #print "agent thinks client is feeling: ",clientEmotion," which is: ",clientEmotionLabel

        learn_aab = []
        learn_paab = []
        fbeh = self.learn_agent.emotdict
        
        learn_eobserv=map(lambda x: float (x), [fbeh[emotion]["e"],fbeh[emotion]["p"],fbeh[emotion]["a"]])
        #print "??????????", learn_eobserv

        
        print "\n ||||||||||||||after the client action, the state and emotion is: "
        self.learn_avgs=self.learn_agent.propagate_forward(learn_aab,learn_observ,learn_xobserv,learn_paab,verb=self.learn_verbose,plotter=self.plotter,agent=eTurn.learner,eobserv=learn_eobserv)
        
        #self.learn_avgs.print_val()
        self.learn_avgs = self.learn_agent.getAverageState()
        self.learn_avgs.print_val()
        agentEmotion = self.learn_agent.expectedEmotion("agent")  ##don't understand here, how to calculate emotion???????????????????
        clientEmotion = self.learn_agent.expectedEmotion("client")   ##get client emotion
        clientEmotionLabel = self.learn_agent.findNearestEmotion(clientEmotion)
        print "agent is feeling: ",agentEmotion," which is : ",self.learn_agent.findNearestEmotion(agentEmotion)
        print "agent thinks client is feeling: ",clientEmotion," which is: ",clientEmotionLabel
        
    #this function return the suggested behaviour for the agent
    #the EPA value is returned, after that I will map the behaviour to 
    #specific detail level
    #after that the propagate_forward is used to update state    
    def get_agent_action(self):
        print "\n Now I want to get the proper action of the agent"
        learn_xobserv = [1] #it is agent turn
        agent_next_action=self.learn_agent.get_next_action(self.learn_avgs,exploreTree=True)
        learn_aab = agent_next_action[0]
        learn_paab = agent_next_action[1]
        
        
        
        #print "\n"
        aact=findNearestBehaviour(learn_aab,self.fbehaviours_agent) 
        print "\nsuggested action for the agent is :",learn_aab," closest label is: ",aact
        #because it is agent's turn, learn_observ and learn_eobserv should be None
        learn_observ = []
        learn_eobserv = []
        self.learn_avgs=self.learn_agent.propagate_forward(learn_aab,learn_observ,learn_xobserv,learn_paab,verb=self.learn_verbose,plotter=self.plotter,agent=eTurn.learner,eobserv=learn_eobserv) 
        return learn_aab
        
        
        
    def behaviour_map(self, aact_epa, prompt):
        #print "\n Now I will map the behaviour EPA to a specific kind of prompt", aact_epa
        #print "the generate epa value is", aact_epa
        #calcuate the level of the prompt
        #print "the length of the prompt is ", len(prompt)
        promptset = prompt[len(prompt)-1]
        tree_prompt = promptset[0]
        #it only output the prompts in the priority list
        level_prompts = tree_prompt._prior_prompt_set
        
        level_sum = len(level_prompts)
        #print "the length of the prompt set is", level_sum

        (help_words, help_detail) = self.get_prompt_level(aact_epa)
        help_level = math.ceil(level_sum*help_detail)
        print "\n The mapped help words is: ", help_words
        print "\n The mapped help level is: ", help_level
        level_record = 0
        if help_level>level_sum: #in this case, all levels of help should be present
            help_words = help_words + 'You are doing'
            for single in level_prompts:
                level_record = level_record+1
                for action in single:
                    the_task = tree_prompt._tree.get_node(action).tag
                    help_words = help_words + ' ' + the_task 
                if level_record < level_sum:
                    help_words = help_words + ' so you should do'
        else:
            for single in level_prompts:
                level_record = level_record+1
                if level_record == help_level:
                    for action in single:
                        the_task = tree_prompt._tree.get_node(action).tag
                        help_words = help_words + ' ' + the_task 
                    help_words = help_words + '.'
                    #print "\n-----the prompt is here!-----------------"
                    #print help_words
                    break  
        self.last_prompt = [help_words, help_detail]
        print "\n-----the prompt is here!-----------------"
        print help_words, "last_prompt level is: ",self.last_prompt[1], "\n" 
        

    def get_prompt_level(self, behaviour_epa):
        #this is the table for behaviour labels and EPA values
        dict = {'listen to': [2.18, 1.57, 0.11], 
                'congratulate': [2.48, 1.73, 0.9], 
                'prompt': [0.15, 0.32, 0.06], 
                'tell something to': [0.77, 0.66, 0.43],
                'remind': [1.63, 1.45, 0.01],
                'aid': [2.05, 1.95, 0.8],
                'instruct':[1.85, 1.65, 0.3], 
                'teach': [2.76, 2.39, 0.9],
                'comfort': [1.5, 1.7, -0.62],
                'cheer up': [2.35, 2.38, 1.59]}
        closest_label = self.get_closest_label(behaviour_epa, dict)
        print "\n The closest label of the behaviour is: ", closest_label
        if closest_label == 'listen to':
            help_words = ''
            help_level = 0
        elif closest_label == 'congratulate':
            help_words = 'wow you complete a hard task! You are so good!'
            help_level = 0
        elif closest_label == 'prompt':
            help_words = 'You should'
            help_level = 0.25
        elif closest_label == 'tell something to':
            help_words = 'You should'
            help_level = 0.5
        elif closest_label == 'remind':
            help_words = 'I think you forget to'
            help_level = 0.5  
        elif closest_label == 'aid':
            help_words = 'Could you'
            help_level = 0.75
        elif closest_label == 'instruct':
            help_words = 'You should'
            help_level = 0.75
        elif closest_label == 'teach':
            help_words = 'Ok, I think you are not familar with this task, I will help you. Now could you'
            help_level = 1
        elif closest_label == 'comfort':
            help_words = 'dont worry, you already did a good job. let me help to remind you what you are doing. '
            help_level = 0 #this is a special case, the computer will provide all level prompt.
        elif closest_label == 'cheer up':
            help_words = 'I believe you can do that! Now you are doing: '
            help_level = 2
        else:
            help_words = 'I do not know what to do now, take care'
            help_level = 0
         
        return (help_words, help_level)
        
    #this function will return the behaviour lable that 
    #has the closes epa value with the "behaviour_epa"
    def get_closest_label(self, behaviour_epa, dict):
        return_label = ''
        dist = 10000  #this number is big enough    
        for x in dict:
            this_dist = LA.norm(np.asarray(dict[x])-np.asarray(behaviour_epa))
            if dist > this_dist:
                dist = this_dist
                return_label = x
        return return_label

