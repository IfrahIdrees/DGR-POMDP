Algorithm Implementation record
-------------------------------
#Summary#
 This document record the progress of implementing the goal recognition algorithm, including details and modifications during each stage.
 
##July 18##

 - **explaSet**=[]: explanations for all the previous observations. Before initialization, this set has a length of 0, at this case, we need to initialize the explaSet according to the knowledge base;
 - *code knowledge base example according to the drawn dia figure*, complete the hand washing part.
 <p align="center">
  <img src="../images/knowledge_base_example.png" width="450"/>
</p>

##July 19##
 - Initialize the explanation set (explaSet)
	 - Step 1: search in "method" collection who has a property of "start_action"
	 - Step 2: for all the returned entries, check if their preconditions are satisfied in the current state
	 - Step 3 : generate the pending set and initialize the explaSet.
 - Initialize the explanation Set (explaSet): didn't finish, only store the updated knowledge base into mongoDB

##July 20##
 - realize explaSet initialization. 

##July 21##
 - create a database class, inside this class, all database related search and operations are included. 
 - calculate action posterior prob based on s(t-1), and o(t), for a given action:
	 - Step 1,  create a list for all it's related object attribute
	 - Step 2, create a list of all possible attribute value combination
	 - Step 3, Bayesian variable elimination to calculate posterior(a)

##July 22##
 - define p(s_t|s_t-1, a_t)
	 - assume that if an action has been implemented, it will ben 100% succeed. 
	 - So **if** precondition(a_t) is satisfied in s_(t-1), and effects(a_t) is satisfied in (s_t), p(s_t|s_t-1, a_t)=1, **else**,  p(s_t|s_t-1, a_t)=0. 
 - calculate p(a_t) give observation
	 - The final p(a_t)[variable elimination] is given by normalizing on (**a_t happened**) and (**a_t not happen**)
	 - for the whole explanation set, calculate **prior(a_t)*posterior(a_t)[variable elimination]**, and then normalize over all the actions in all of the pending set
 - move notification to a class, every time the engine need notification, get it from the class instance.
 - *need to finish belief state update*


##July 26##

 - implement belief state update (changed....see July 28)
	 - when updating, only update those states that occurs in the effect list of the pending sets. Other's remain the same
	 - finished
 - change **explaSet** to a class. 


##July 27##

 - When to trigger the engine?  According to " **no_notif_trigger_prob**"
	 - If **there is** some notification: trigger definitely
	 - If **there is no** notification: 0.9 cases sleep, 0.1 run the activity tracking process. 

 - Update the explanation set, including three steps:
	 - step 1: update the tree structure (not finished)

 - **Revision**:
	 - For each explanation, it has a pending set. Within the pending set, there are one or more than one actions. Because sensor probabilities are considered, we need to consider "**nothing happened**" scenario. 
	 - How to calculate the probability of "**nothing happened**"? If the pending set is [a_1, a_2, a_3, non]:
		 - (1) Calculate the probability of each action "**happened**"
		 - (2) Calculate the probability of "nothing happened", multiply the corresponding not-happen-prob of each action.
		 - (3) Calculate the probability of {one actions happens, two actions happens, three actions happens and so on..}
		 - (4) Step (1)(2)(3) generated the explanations for the current observation. It is something like [a1, p1; a2, p2; a2, p3; a1, a2, p12; a1, a3, p13; a2, a3, p23; a1, a2, a3, p123; non, pn ]  (**example**)
		 - (5) For each case in the action level observation explanation, update and expand the current explanation into new explanations. In this example, the explanation will generate 8 different new explanations. (when calculate the posterior (new) probability for those new explanations, be sure use the parent explanation's prior probability multiply by branch factor nodes. )
		 - (6) finally for all explanations, normalize them.  

 - Tomorrows goal:
	 - finish action level explanation calculating
	 - add a new task and test (expand the knowledge base)
	 - begin the tree structure update (should begin with initialization)


##July 28##

 - add new knowledge-base, including corresponding sensor, state, operator, and method
 - **revision the state update algorithm**.
	 - when updating, only update those states that occurs in the effect list of the pending sets. Other's remain the same.(this is kind of *approximation*)
	 - Using the **formula** in my book
	 - Step 1: generate the list of actions in the pending set of all explanations. The probability of those actions should be updated: **action_prob*exp_prob**
	 - Step 2: Calculate the probability of nothing happened. noth_prob = multiply(1-a_i)
	 - Step 3: Calculate the probability of state according to the formula in my book and normalize.
 - Fix bugs


##July 29##

 - action level explanation calculation (completed)
	 - Assumption: each step **at most one** action happen.
	 - if the pending set (a1, a2, a3), the prob of **nothing happened** is multiple(1-ai)
	 - then the probability of something happened is (1-nothing happened)
	 - normalize on something happened to make it sum to (1-nothing happened)  
 - start hierarchical tree construct (not finish), tomorrow, generate tree structure based on domain knowledge and precondition check. 


##July 30##

break ha ha ha ha ha

##July 31##

 - **Revise database collection for method and operator**: add new property"**parent**", this information is used for bottom up process.
 -  initialize_tree_structure(action_name): This function is used to generate all possible tree structures that can explain the given action_name(which is just happened. )
 - bottom up process
 - when add a new parent nodes into the tree structure:
	 - step 1: calculate the number of alternative branches
	 - Step 2: calculate the probability of each alternative branches(based on there precondition )
	 - Step 3: Normalize their probability
	 - Step 4: only return the branches whose subtasks contains the given child-node.
 - For each possible decomposition, add the corresponding tree structure into the existing tree structure.  Need to add the **pre** and **dec** node in the node data parameter.   

  
  
##August 1##

 - **For initialization**, it means before that there is no tree structure at all. (**completed**)
	 - Firstly calculate all possible tree structures and multiply by **action level prob** and **branching factor prob**. 
	 - Secondly, update the explanation probability using prior. In this project I am using evenly distributed probability. the function is (explanation.py - class explaSet - add_goal_priors)
 
 - **Fix a bug**: when generating new explanations based on the existing one, be remember to use copy.deepcopy() for tree structures. 

 - **Update the node completeness:**
	 - general idea: DFS and recursion
	 - a parent node is completed if and only if all of its children are completed
	 - stop criteria: leaf node 

 - **Update the readiness of node**
	 - general idea: BFS
	 - for each level for each node:
		 - if it is goal node, ready is **true**
		 - if it is non-goal node, if it's pre is null, ready is the node's **parent's ready status**
		 - if it is non-goal node, if it's pre is not null, 
			 - if all pre node are completed, the node ready is **True**
			 - otherwise, the node is ready is **False**

##August 2##

 - Update the pending set for taskNet (finished)
	 - pending set is a list, each element has the structure of [tree, prob, pending]
	 - only expand leaf node in the tree:
		 -  who is a method
		 -  who data._ready = True
		 -  who data._completeness = False
	 - When no leaf node can be expand in the tree, generate its corresponding pending actions. filter leaf nodes whose data._ready = True, and data.completeness = False
 - Pending Set of a TaskNet is different from the pending set of an explanation. It stores the next decomposition information for the current tree structure. So It is associated with the next happen action. 
 - When an action is identified to happened, just use the corresponding tree structure in the TaskNet pending set. 

	 
##August 3##
 
 - **Revision explanation initialization**: When initialize the explanation set, also initialize the start_action list. This list will be updated on the fly. The current tree structure and the start_action list will be used for generating the new pending set for one explanation. (finished)
 - **explanation_expand**(): ***finished***. For each action in the action_level explanation:
	 - if it is nothing happen, create new explanation, only update prob.
	 - if it is something happen, for each possible happened action:
		 - for each existing explanation in the last step:
			 - for each TaskNet in that explanation
				 - If this action exist in the pendingset of this TaskNet, generate new explanation 
		 - if the action exist in the start_action list of the explanation, 
			 - initialize TaskNet for that action
			 - generate new explanation based on each of the TaskNet from initialization
	 - If something happen, but cannot find in the explanation in the above mentioned step
		 - this is an error action (dangerous action) 
 - **Generate_new_expla**: Do not update pending set, it will be initialized as null. 
	 - one exception is "nothing happened", in this case, pending set will be copied from the parent explanation. 
	 - This difference will be useful for figure out which explanation need to be generate new pending set. 
 - **TaskNet_update()**:
	 -  Every time a new taskNet is generated, update it. 
	 - This will update the completeness of each node, the readiness of each node, and the TaskNetPendingSet (The next step decomposition results from this TaskNet). 
	 - TaskNet is updated before using it generate new explanations. 
	 - This guaranteed that all TaskNet in the explaSet is updated. 
	 
 - **Update_state_belief:  Revision**.  
	 - Combine shared pending set actions by different explanations, after calculate the probability of nothing happened. (**finished**)
	 - It's better to normalize on other actions.(didn't do this step) 
 - **Generating new pendingSet**: (**finished**)
	 - firstly normalize on all explanation
	 - produce the new pending set based on the TaskNet and start_action list
	 - Assign probability for them. 
		 - for explanation who has pending set already, normalize them based on the expla._prob
		 - for explanation who do not has pending set, create pending set and normalize them based on the expla_prob. 


##August 4, 5, 6, 7##
didn't make any progress

##August 8##
TA proctoring
Rearrange code(didn't finish)
##August 9##
TA marking
##August 10##
G1 testing
##August 11##
Other staff
##August 12##



##August 15##

 - add new knowledge base action level
 - **Important modification:**: need to check precondition produce method, for ordered steps. p1Up2Up3 - P2you know jagdjalksd
 - need to consider the water has been heated, water cold/water hot
 - state 闭环检测（begin from what, should come back to what）



##Pending things
 - Calculate the probability for goals and inner nodes in the tree. Because the desired assistance is hierarchical, only provide the probability of goals is not enough. We also need to calculate the probability of inner nodes in the tree structure.   
 - Rearrange the code in a clear manner
 - Test the algorithm
 - creating new knowledge base  and test the algorithm. 