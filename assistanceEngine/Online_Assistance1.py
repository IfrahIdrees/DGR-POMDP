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
import client
#sys.path.append("/home/d97wang/workspace/CS886/online_Recog_withemotion/bayesact/")


from Action_recog import action_recog
from Hierarchical_Activity_recog import Hierarchical_Activity_recog
from Complete_Hierarchical_tree import Complete_Hierarchical_tree
from Hierarchical_Assistant import Hierarchical_prompt
from FuncforHierarActRec import search_in_prompt
from Complete_tree_update1 import Complete_tree_update
from affective_assistant import HierarAssistant

this_agent = HierarAssistant({})

interval = 1; #the sleep interval between sensor infor gathering
stop = False; # the user can control when to stop the assist of the system

aact_epa = []
prompt = []        #this will record the current possible prompt.
prompt1 = [] 

'''                   #not all of the prompts would be present
if len(prompt)==0:
    print "currently there is no prompt in the list"
'''
P_Hierar_Trees = []    #store the partial hierarchical trees
C_Hierar_Trees = []    #the expanded complete tree, only completed tasks are involved
#person, this parameter has no use now
person = 'grandpa' 
steps = 0 
while (stop == False):
    #time.sleep(interval)
    #print "Start: %s" % time.ctime() 
    control = (raw_input('Please input anything to continue:'))
    #Mar 23rd, 2016------get state changes from keyboard input
    #this will indicate what the elder people has done
    '''
    object_state_name = (raw_input('Please input the object-state name:'))
    object_state_name = object_state_name.split(',')
    #print object_state_name
    #print len(object_state_name)
    
    object_state_value = (raw_input('please input the current object-state value:'))
    object_state_value = object_state_value.split(',')
    #print len(object_state_value)
    
    
    user_emotion_state = (raw_input('please input your current emotion:'))
    '''
    (object_state_name, object_state_value, user_emotion_state) = client.simulate_action()
    if object_state_name == 'done':
        print steps
        break
    else:
        object_state_name = object_state_name.split(',')
        object_state_value = object_state_value.split(',')
    #print "the object is:", object_state_name
    #print "the state value is: ", object_state_value
    #print "the emotion is: ", user_emotion_state
    
    if object_state_name[0]=='' or object_state_name[0]=='':
        #in this case the client do nothing
        if len(prompt) <= 0:   #in this case nothing happend, pass
            pass
        elif this_agent.last_prompt[1] == 0:  #in this case, client should do something, but didn't;there is no prompt last step
            #print "the patient do nothing without prompt" #do nothing, without prompt
            this_agent.update_after_client([0, -2.32, -2.94], user_emotion_state)   #forget, but make evaluation neutral
        elif this_agent.last_prompt[1] == 0.25:
            this_agent.update_after_client([-0.86, 0.16, 0.16], user_emotion_state)   #renounce
        elif this_agent.last_prompt[1] == 0.5:
            this_agent.update_after_client([0.49, -0.06, -0.57], user_emotion_state)   #wait on
        elif this_agent.last_prompt[1] == 0.75:
            this_agent.update_after_client([-1.29, -0.32, -0.94], user_emotion_state)   #forget
        elif this_agent.last_prompt[1] == 1:
            this_agent.update_after_client([-1.58, -0.75, -1.44], user_emotion_state)   #ignore
        elif this_agent.last_prompt[1] >1:
            print "Alert care-giver! The elder is totally lost, need real caregiver's help!"
            break
        #print "generate new prompt here" #this function will update prompt, if last time no prompt this time give; if has prompt, this time go into detail level
        aact_epa = this_agent.get_agent_action()
        this_agent.behaviour_map(aact_epa, prompt)
        #print aact_epa
        
        
    else: #state has changed
        statefile.updatestate(object_state_name, object_state_value)
        state_t = copy.deepcopy(statefile.state_t)
        state_t1 = copy.deepcopy(statefile.state_t1)
        
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
                break
            else:
                
                operators = execute_operators.keys()
                print "\n the recognized action is: ", operators
                operator = operators[0]
                find_in_prompt = False
                prompt1 = []
                #################################################################
                ############-----from here, update prompt list-----##############
                #check whether the recognized action exist in the prompt list
                #print "from here update prompt list"
                #print "before check the exist or not, the legnth of prompt", len(prompt)
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
                            prompt1.append(promptset)
                            #print len(prompt1)
                            find_in_prompt = True
                            break
                     
                
                prompt = copy.deepcopy(prompt1)            
                if find_in_prompt == False: #should start a new tree
                    #print "\n the recognized action does not exist in the prompt list"
                    #(2)generate potential prompt list
                    #generate the partially tree using Hierarchical_Activity_recog
                    P_Hierar_Trees = Hierarchical_Activity_recog(execute_operators, state_t, person)
                    #print "hierarchical recognized"
                    #decompose the partial tree to get complete tree
                    C_Hierar_Trees = Complete_Hierarchical_tree(P_Hierar_Trees, state_t1, person)
                    #print "complete tree success"
                    #get prompt
                    prompt.append(Hierarchical_prompt(C_Hierar_Trees)) #append rather than = %%%
                    
                else: #should update an existing tree
                    #print "the recognized action exist in the prompt list"
                    #print len(prompt)
                    for promptset in prompt:
                        completetreesnow = []
                        for treeprompt in promptset:
                            #print len(promptset)
                            #print type(treeprompt)
                            #here is a little wired because Hierarchical_prompt working on multiple trees
                            #completetreesnow.append(copy.deepcopy(treeprompt._tree))
                            completetreesnow.append(treeprompt)
                        prompt.remove(promptset)
                        prompt.append(Hierarchical_prompt(completetreesnow))
                
                
                
                
                print "\n------------from here, affective state----------------"
                if find_in_prompt == False:
                    #print "the patient start a new thing with prompt"
                    this_agent.update_after_client([-0.24, 1.05, 0.74], user_emotion_state) #work
                elif this_agent.last_prompt[1] == 0:
                    #print "the patient do something without promt"
                    this_agent.update_after_client([1.16, 0.74, 0.41], user_emotion_state) #ask about something
                elif this_agent.last_prompt[1] == 0.25:
                    this_agent.update_after_client([2.2, 1.64, 0.75], user_emotion_state) #answer
                elif this_agent.last_prompt[1] == 0.5:
                    this_agent.update_after_client([1.53, 1.37, 0.68], user_emotion_state) #reply to
                elif this_agent.last_prompt[1] == 0.75:
                    this_agent.update_after_client([0.48, 0.27, 0.64], user_emotion_state) #mimic
                    #I change the evaluation part from "-0.74" to "0.48", because this is a good thing in this case
                elif this_agent.last_prompt[1] >= 1:
                    this_agent.update_after_client([0.58, -0.52, -0.95], user_emotion_state) #obey   
                
                aact_epa = this_agent.get_agent_action()
                #print "the generated behaviour epa value is:", aact_epa
                this_agent.behaviour_map(aact_epa, prompt)
                   

    #wait for a while and loop            
    #print "End: %s" % time.ctime()
    time.sleep(interval)
    ################################################################
    wantstop = 'N' 
    #here get from user click on the user interface, if choose stop, will stop the whole process 
    ################################################################
    steps = steps + 1
    if wantstop == 'Y':
        stop = True
    elif wantstop == 'N':
        stop = False
    else:
        print "wrong input, the assistance process teminate!"
        break
    
