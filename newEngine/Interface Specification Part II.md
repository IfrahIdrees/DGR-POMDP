Interface Specification Part II
===============================
By Dan Wang, start from Aug 26th, under updating


Checklist
---------

 - main.py
 - **Class** Tracking_Engine

main.py
-------

 - the entrance of the algorithm, create an instance of a **Tracking_Engine**, and start it. 
 - specify parameters:
	 - *no_notif_trigger_porb*: without notification, the probability of go through the whole updating procedures
	 - *interval*: sleep interval between two running of the algorithm
	 - *cond_satisfy*, cond_notsatisfy: specify conditional probability p(s_t | s_t-1, a_t)
	 - *delete_trigger*: the threshold that an explanation should be dropped. 

**Class** Tracking_Engine
---------------------

 - `def` __init__(self, no_trigger = 0, sleep_interval = 1, cond_satisfy=1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001)
	 - Initialize necessary parameters
 - `def` start(self):
	 - while loop forever
	 - case 1: has notification, go through the tracking engine algorithm
	 - case 2: has no notification, go through the tracking engine with probability of "**no_trigger**", sleep with probability of "**1-no_trigger**"
	 - tracking engine algorithm procedures:
		 - create ***ExplaSet*** instance
		 - explaInitialize(): Initialize *ExplaSet*
		 - action_posterior(): calculate the posterior probability of an step has happened for steps in the pending set
		 - update_state_belief(): update the belief state
		 - explaSet_expand(): expand the ExplaSet
		 - pendingset_generate(): generate the new pendingSet
		 - task_prob_calculate():calculate the probability of an task should happen in the next step, this is used for prompt. 