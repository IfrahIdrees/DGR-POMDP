# Knowledge Base #
##The state##
The state of the environment is stored in the mongoDB in a JSON format. Each object in the environment has an corresponding document in the mongoDB collections. The document includes all the related attributes of the physical object. An example of a document is presented in Figure 1. 

      Figure 1
            {           
            			"_id": "ObjectId('5760929718cc0f4a54f4d070')"
            		    "name":"faucet_1",
            		    "type":"faucet",
            		    "state":"on",
            		    "location":"wash_room"
            }
In the mongoDB, there are two state collections ***state_1*** and ***state_2***

 - ***state_1***: the environment state in time point ***(t-1)***
 - ***state_2***: the environment state in time point ***t***

##The step##
A step (also known as an operator) is a knowledge base explains the step name, its preconditions, effects, and associated objects in the environment. An example of a step is presented in Figure 2.

    Figure 2
    {
	    "_id":ObjectId('57683945db99da339bbf04dd')
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
 - ***effect***: explains how the step will change the state of the environment. (Similar to precondition)  

##MongoDB Collections##
 

 - state_1
 - state_2
 - operators
 - method

