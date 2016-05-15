"""
This is the overall control of activity recognition. 
Its functions: receive informations from sensors every "interval" time(3s for example)
and run the activity recognition algorithm 

Author: Dan Wang <d97wang@uwaterloo.ca>, Nov. 17, 2015
"""
import time
import copy
import statefile
import sys
#sys.path.append("/home/d97wang/workspace/CS886/online_Recog_withemotion/bayesact/")


from Action_recog import action_recog
from Hierarchical_Activity_recog import Hierarchical_Activity_recog
from Complete_Hierarchical_tree import Complete_Hierarchical_tree
from Hierarchical_Assistant import Hierarchical_prompt
from FuncforHierarActRec import search_in_prompt
from Complete_tree_update import Complete_tree_update
from affective_assistant import HierarAssistant

this_agent = HierarAssistant({})

interval = 10; #the sleep interval between sensor infor gathering
stop = False; # the user can control when to stop the assist of the system
last_prompt = {}   #this will record the last present prompt.
aact_epa = []
prompt = []        #this will record the current possible prompt. 

'''				   #not all of the prompts would be present
if len(prompt)==0:
	print "currently there is no prompt in the list"
'''
P_Hierar_Trees = []    #store the partial hierarchical trees
C_Hierar_Trees = []    #the expanded complete tree, only completed tasks are involved
#person, this parameter has no use now
person = 'grandpa'  
while (stop == False):
    #time.sleep(interval)
    print "Start: %s" % time.ctime() 
    #Mar 23rd, 2016------get state changes from keyboard input
    #this will indicate what the elder people has done
    object_state_name = (raw_input('Please input the object-state name:'))
    object_state_value = (raw_input('please input the current object-state value:'))
    if object_state_name=='' or object_state_name=='':
    	#in this case the client do nothing
    	if len(prompt) <= 0:   #in this case nothing happend, pass
    		pass
    	elif len(last_prompt)<=0:  #in this case, client should do something, but didn't;there is no prompt last step
    		print "the patient do nothing without prompt" #do nothing, without prompt
    		this_agent.update_after_client([-1.29, -0.32, -0.94])   ##I am using the word "forget" here
    	else:
    		print "the patient do nothing with prompt" #do nothing, withprompt, this is the worst case
    		this_agent.update_after_client([-1.29, -1.32, -1.94])
    	
    	
    	
    	print "generate new prompt here" #this function will update prompt, if last time no prompt this time give; if has prompt, this time go into detail level
    	aact_epa = this_agent.get_agent_action()
    	print aact_epa
    	
    	
    else: #state has changed
    	statefile.updatestate(object_state_name, object_state_value)
    	state_t = copy.deepcopy(statefile.state_t)
    	print "output the state"
    	print state_t.__dict__
    	
    	state_t1 = copy.deepcopy(statefile.state_t1)
    	print state_t1.__dict__
    	if state_t == state_t1: #No state changes, means the patient do nothing
    	    #here we don't need to consider all possibles since we already considered
    	    #it is here just because currently, we use raw input to simulate user action
    	    #this is also "has no state change!!!!!!!!!!!!!!!!!!!!!!"
    	    #but in this version, has no state change means has no input!!!!!
    	    print "has no state changes! output here!!"
    	    pass
    	else:
    		execute_operators = action_recog(state_t, state_t1)
    		if len(execute_operators) == 0: #has state changes but failed to recognize the action
    			print "Alert care-giver!" #what to do here????!!!!!!!!!!!!!!!?????????????!!!!!!
    		else: #recognize actions successfully
		        #print "recognised operators"
		        if len(prompt)== 0: #currently there is no prompt
		            #in this case, the last-prompt is None, but the patient has done something
		            #in this brunch we need to do following things:
		            #   (1)update affective state according to the patient's action
		            #   (2)generate potential prompt list
		            #   (3)generate the reasonable behaviour EPA value for agent and update affective state
		            #   (4)map the EPA value to a specific level of prompt, and specific kind of
		            #       text expression(rudely or kindly), and present to user
		            #   (5)update the last_prompt value for tracking
		            #-----------------------------------------------
		            #(1)update affective state according to the patient's action
		            print "the patient do something without prompt" #do something, without prompt
		            this_agent.update_after_client([0.5, 2, 1.5])   ##This should be very positive here
		            #-----------------------------------------------
		            #(2)generate potential prompt list
		            #generate the partially tree using Hierarchical_Activity_recog
		            P_Hierar_Trees = Hierarchical_Activity_recog(execute_operators, state_t, person)
		            #print "hierarchical recognized"
		            #decompose the partial tree to get complete tree
		            C_Hierar_Trees = Complete_Hierarchical_tree(P_Hierar_Trees, state_t1, person)
		            #print "complete tree success"
		            #get prompt
		            prompt.append(Hierarchical_prompt(C_Hierar_Trees)) #append rather than = %%%
		            #print "promptset succeed"
		            #------------------------------------------------
		            #(3)generate the reasonable behaviour EPA value for agent and update affective state
		            aact_epa = this_agent.get_agent_action()
		            print "the generated behaviour epa value is:", aact_epa
		            #--------------------------------------------------
		            #(4)map the epa value to a specific prompt and output
		            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$wait for implement here
		            print "\n"
		            print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		            print "provide prompt here" #how to present prompt#??????????????????????????!!!!!!!!!!!!
		            print "\n"
		        else: #exist prompt

		            
		            operators = execute_operators.keys()
		            print operators
		            operator = operators[0]
		            find_in_prompt = False
		            
		            #to check whether the recognized action exist in prompt list
		            for promptset in prompt:
		                for treeprompt in promptset:
		                    label = search_in_prompt(operator, treeprompt)
		                    if label != False: #found the node in prompt list
		                        storetreeprompt = copy.deepcopy(treeprompt)
		                        #update the record the the corresponding tree
		                        #mainly update the data of the tree
		                        storetreeprompt = Complete_tree_update\
		                        (label, storetreeprompt, state_t1, person)
		                        promptset = []
		                        promptset.append(storetreeprompt) #only store this tree, delete others
		                        find_in_promt = True
		                        break
		                    
		            if find_in_prompt == False:
		                #generate new prompt,parital tree, and complete tree
		                P_Hierar_Trees1 = Hierarchical_Activity_recog(execute_operators, state_t, person)
		                #print "hierarchical recognized"
		                #decompose the partial tree to get complete tree
		                C_Hierar_Trees1 = Complete_Hierarchical_tree(P_Hierar_Trees1, state_t1, person)
		                #print "complete tree success"
		                #get prompt
		                prompt.append(Hierarchical_prompt(C_Hierar_Trees1)) #append rather than = %%%
		                #print "promptset succeed"            
		            
		            else: # the just now action exist in prompt, using the updated complete tree generate new prompt
		                for promptset in prompt:
		                    completetreesnow = []
		                    for treeprompt in promptset:
		                        #print type(treeprompt) 
		                        #here is a little wired because Hierarchical_prompt working on multiple trees
		                        completetreesnow.append(copy.deepcopy(treeprompt._tree))
		                    prompt.remove(promptset)
		                    prompt.append(Hierarchical_prompt(completetreesnow))
		                    print "\n"
		                    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		                    print "provide prompt here" #how to present prompt#???????????????????   
		                    print "\n"                               
                
    
    
    #wait for a while and loop            
    print "End: %s" % time.ctime()
    time.sleep(interval)
    ################################################################
    wantstop = 'N' 
    #here get from user click on the user interface, if choose stop, will stop the whole process 
    ################################################################
    if wantstop == 'Y':
        stop = True
    elif wantstop == 'N':
        stop = False
    else:
        print "wrong input, the assistance process teminate!"
        break
    
