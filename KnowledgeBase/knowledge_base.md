# Knowledge Base #
##The state##
The ***last point*** state of the environment is stored in the mongoDB in a JSON format. Each object in the environment has an corresponding document in the mongoDB collections. The document includes all the related attributes of the physical object. An example of a document is presented in Figure 1. 

      Figure 1
            {
            		    "name":"faucet_1",
            		    "type":"faucet",
            		    "state":"on",
            		    "location":"wash_room"
            }


##State change notification##
Each time there is a state change, the sensor manager will notice the goal recognition engine. The state change notification message include following information:

 - the object whose state has been changed
 - the object's **current** attributes information
 - the object's **last time point** attributes information

***Assumption***: ***we assume that each state change notification only related to one step.*** If the engine failed to target one step according the change, it means something goes wrong. And then the caregiver should be alert. 

The format of state change notification is presented in Figure 2. If the occurred step changes the state of more than one objects, the the state change notification should present all changes in this format.  In this format, "name" tell which object, "change": tells the changed attribute and the associated "previous" and "current" state. In this example, it means **"faucet_1's state changed from on to off"**

    Figure 2
    {
	    "name":"faucet_1", (object name)
	    "change":["state","on", "off"] 
		    (object change [attribute, previous_state, current_state]) 
    }

##The step in Knowledge Base ##
A step (also known as an operator) is a knowledge base explains the step name, its preconditions, effects, and associated objects in the environment. An example of a step is presented in Figure 3. **(please notice that each *step in knowledge base* is an instance of an abstract step in the "Expert Database (ED)". An abstract step in ED has the same components with step instances in the knowledge base. The difference is that in an abstract step, objects occur in preconditions and effects are variables. Those variables are assigned specific values (environment object) when the caregiver constructing the knowledge base. )**

    Figure 3
    {
        "type":"step",
        "name":"turn_off_faucet",
        "precondition":{
            "faucet_1":{
                "state":"on",
                "location":"wash_room"  
            },
            "person_1":{
                "location":"wash_room",
                "ability":[">=", "0", "0.8", "0.4"]
            }
        },
        "effect":{
            "faucet_1":{
                "state":"off"  
            }
        }
    }


 - "***_id***" is a unique label for the step by the system
 - "***type***" indicates this is a step category. (In the knowledge base, it also includes ***task***)
 - "***precondition***": demonstrate under what kind of condition, this step can be executed
	 - one precondition begins with a concrete object in the environment, and then specify its required state
	 - constraint precondition: the first element of the list explains the constrain, like the ">=" in the example
	 - ability condition: [">=", "0", "0.8", "0.4"], the three number represent the required ability of "recall", ""recognition", and "affordance", separately. 
 - ***effect***: explains how the step will change the state of the environment. (Similar to precondition)  
	 - one effect begins with a concrete object in the environment, and then specify its state after the step. 
	 - one step can have effects on multiple objects. 


##MongoDB Collections##
 

 - state
 - operators
 - method





Knowledge Base with Uncertainty
===============================
In this project, two kinds of uncertainties are considered:
(1) Sensors are not 100% percent reliable.  So in the state change notification list, for each state change, there is a probability indicating the reliability of the sensor. This kind of reliability information will be used in two ways:

 - Calculate the probability of the corresponding actions has happened. 
 - Update the environment state information 

##The state##
The ***last point*** state of the environment is stored in the mongoDB in a JSON format. Each object in the environment has an corresponding document in the mongoDB collections. The document includes all the related attributes of the physical object. Each attribute describes all possible values and the corresponding possibility. An example of a document is presented in Figure 1. As we can see in this example, the "state" attribute has two possible values, "on" with probability 0.9, "off" with probability "0.1".  

      Figure 1
            {           
            		    "ob_name":"faucet_1",
            		    "ob_type":"faucet",
            		    "state":{
	            		    "on":0.9,
	            		    "off":0.1
	            		 },
            		    "location":{
	            		    "wash_room":1
            		    }
            }


##State change notification##
Each time there is a state change, the sensor manager will notice the goal recognition engine. The state change notification message include following information:

 - the object whose state has been changed
 - the object's **current** attributes information
 - the object's **last time point** attributes information
 - the corresponding sensor's **reliability**

***Assumption***: ***we assume that each state change notification only related to one step.*** If the engine failed to target one step according the change, it means something goes wrong. And then the caregiver should be alert. 

The format of state change notification is presented in Figure 2. If the occurred step changes the state of more than one objects, the the state change notification should present all changes in this format.  In this format, "name" tell which object, "change": tells the changed attribute and the associated "previous" and "current" state. In this example, it means **"faucet_1's state changed from on to off"**

    Figure 2
    {
	    "ob_name":"faucet_1",
	    "reliability":"0.9",
	    "attribute": "state",
	    "previous": "on",
	    "current": "off",
    }

##The *step* in Knowledge Base ##
A step (also known as an operator) is a knowledge base explains the step name, its preconditions, effects, and associated objects in the environment. An example of a step is presented in Figure 3. **(please notice that each *step in knowledge base* is an instance of an abstract step in the "Expert Database (ED)". An abstract step in ED has the same components with step instances in the knowledge base. The difference is that in an abstract step, objects occur in preconditions and effects are variables. Those variables are assigned specific values (environment object) when the caregiver constructing the knowledge base. )**

    Figure 3
    {
	    "type":"step",
	    "st_name":"turn_off_faucet_1",
	    "precondition":{
	        "faucet_1":{
	            "state":"on",
	            "location":"kitchen"  
	        },
	        "person_1":{
	            "location":"kitchen",
	            "ability":[">=", "0", "0", "0"]
	        }
	    },
	    "effect":{
	        "faucet_1":{
	            "state":"off"  
	        }
	    },
	    "parent":["wash_hand", "kettle_1_add_water"]
	    }
	}


 - "***_id***" is a unique label for the step by the system
 - "***type***" indicates this is a step category. (In the knowledge base, it also includes ***task***)
 - "***precondition***": demonstrate under what kind of condition, this step can be executed
	 - one precondition begins with a concrete object in the environment, and then specify its required state
	 - constraint precondition: the first element of the list explains the constrain, like the ">=" in the example
	 - ability condition: [">=", "0", "0.8", "0.4"], the three number represent the required ability of "recall", ""recognition", and "affordance", separately. 
 - ***effect***: explains how the step will change the state of the environment. (Similar to precondition)  
	 - one effect begins with a concrete object in the environment, and then specify its state after the step. 
	 - one step can have effects on multiple objects. 


##The *task* in Knowledge Base ##
A task (also known as a method) is a knowledge base artifact explains the task name, its preconditions, and decomposed sub-tasks. An example of a task(method) is presented in Figure 4. The format for the precondition part is the same as that of step. However, what kind of statement should be included into the precondition of a task should be determined by its children. In an actual case, the precondition is derived from its children according the rule defined in the care-giver interface knowledge building part. (See thesis latex file. ) 
Worth mentioning is that the sub-tasks part is a list. Each element of the list is one kind of decomposition of the parent node. There might exist multiple ways of decomposition for one parent node. For each decomposition solution, it includes following information: (1) the sub-task name, (2) the sub-task's predecessor within its parent's children, (3) the sub-task's successor within its parent's children. I am using this kind of format to express 
Another thing about task is that the "start_action" part has a null list. This is used for distinguish with goal. 

    Figure 4.
    {
	    "type":"method",
	    "m_name":"clean_hand",
	    "precondition":{
	        "hand1":{
	            "dirty":"yes",
	            "soapy":"no"  
	        },
	        "faucet1":{
	            "state":"on"
	        },
	        "person_1":{
	            "location":"wash_room",
	            "ability":[">=", "0", "0", "0"]
	        }
	    },
	    "subtasks":{[
	        "use_soap":{
	            "pre":[],
	            "dec":["rinse_hand"]
	        },
	        "rinse_hand":{
	            "pre":["use_soap"],
	            "dec":[]
	        }
	   }],
	   "parent":["wash_hand"],
	   "start_action":[]
	}



##The *goal* in Knowledge Base ##
A goal is the purpose the person aims to achieve when he/she implementing a series of actions. A goal has no parent, it is the 0 level node in the knowledge base. **Worth mentioning is that**, sometimes, a goal can be seen as a typical task.  For example, "wash-hand" can be an independent goal and also can be one of a composite task support for goal "grooming". However, a typical task can never be regarded as a goal. The format of a goal is quite similar to that of task, the only difference is that in a "goal" structure, there is a "start-action" property. This property is mainly used for **pending set initialization use**. Figure 5 gives an example of a goal. 

    {
	    "type":"method",
	    "m_name":"wash_hand",
	    "precondition":{
	        "hand1":{
	            "dirty":"yes",
	            "soapy":"no",  
	        },
	        "faucet1":{
	            "state":"off"
	        },
	        "person_1":{
	            "location":"wash_room",
	            "ability":[">=", "0", "0", "0"]
	        }
	    },
	    "subtasks":[{
	        "turn_on_faucet1":{
	            "pre":[],
	            "dec":["rinse_hand"]
	        },
	        "clean_hand":{
	            "pre":["turn_on_faucet1"],
	            "dec":["turn_off_faucet1"]
	        },
	        "turn_off_faucet1":{
	            "pre":["clean_hand"],
	            "dec":["dry_hand"]
	        },
	        "dry_hand":{
	            "pre":["turn_off_faucet1"],
	            "dec":[]
	        }
	    }],
	    "parent":[],
	    "start_action":["turn_on_faucet1"]
    }




##MongoDB Collections##
 

 - state
 - operators
 - method

