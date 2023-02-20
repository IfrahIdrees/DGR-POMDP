
# GoalRecognitionAndPlanning
Code for Thesis: 

Hierarchical Task Recognition and Planning in Smart Homes with Partial Observability

To cite this work:

Option 1: Dan Wang (2017). Hierarchical Task Recognition and Planning in Smart Homes with Partial Observability. UWSpace. http://hdl.handle.net/10012/12001

Option 2: Wang, D. and Hoey, J., 2017, November. Hierarchical Task Recognition and Planning in Smart Homes with Partial Observability. In International Conference on Ubiquitous Computing and Ambient Intelligence (pp. 439-452). Springer, Cham.

Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017) 

Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)

Association: Computer Science, University of Waterloo.

Research purposes only. Any commerical uses strictly forbidden.

Code is provided without any guarantees.

Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).


## Run

Entrance file: ../HTN-GRP-PO/main.py

## Knowledge Base

Folder: ../KnowledgeBase/

Include:

        knowledge base
        
        missing sensor set up files (folder /missing_sensor)
        
        sensor reliability set up files (folder /sensor_reliability)
        
        initial real state set up (realState.json)
        
        belief state set up (state.json)
        

To under stand the format of method and operator in knowledge base
refer "../HTN-GRP-PO/Interface Specification part III.md"

        
## Test Cases

Folder: ../TestCases

Include:

        single goal correct steps:          case 1-3
        
        multiple goals with shared steps:   case 4
        
        multiple goals correct steps:       case 5-6
        
        single goal wrong steps:            case 7-10
        
        multiple goals wrong steps:         case 11-12
        


## Performance Evaluation

Folder: ../PerformanceEvaluation

Include:

        The desired step output for each test cases
        
        the script that is used to compute the output accuracy

[Dec-26-22]
1. Added human and agent turns to MCTS so now alternate between human actions and the agent actions
2. fixed how to get explaset for explaSet_expand_part1()
3. pending set generates in simulation the next step but when real step not return correct thing
4. if goal complete in simulation you start a new goal which is different


[Jan-2-22]
1. Fixed the correct steps and multiple goals

Todo:
1. Add the wrong steps
2. Fix that multiple goals are opposite not 2 and 3.


[Jan-8-22]
1. Fixed the correct steps and single goals now with reward back propogation
2. final action choice implementated after MCTSA
3. fixed simulate function

Todo:
1. Fix action/observation node added correctly in the self.children.
2. Fix multiple goal situation, the goal and next_human_action not propogated correctly.

[Jan13]
when new goal 9,0 for some reason main root node is not in self.children.
step number is not propogating consistently

[Jan14]
1. Fixed the expand_action for all actions
2. in monte carlo tree search adding argument to keep track of the first step
3. Tried to fix the multi-goal bu adding condition in the 
current_goal==0

Todo:
1. Fix that action node for every observation node in children
2. rootnode is not in self.children 
3. multigoal is giving error sometimes so not properly fixed.

Last error:
real Simulate step:  open_coffee_box_1 
ROLL OUT #  4
here

Starting select
mcts Simulate step:  open_tea_box_1

Starting Simulation

[Jan 22]
1. added result automation pipeline for two domains
1. Fixed that action node for every observation node in children

Todo:
2. rootnode is not in self.children 
3. multigoal is giving error sometimes so not properly fixed.




pid: [1] 33008
[1] 7960

nohup python main.py --agent_type pomdp --max_depth 17 --num_sims 7 --d 0.95 --e 1 --wp -5 --qr 5 --qp -5 --domain kitchen &
[1] 27984


Jan 25
1. Fixed the argument issues for the action node during simulation and selection
2. fixed step_reward to include the action_arguments
3. observation node should have action_node as zero
4. added preferred action heuristic
5. corrected the result renaming for tian
6. do not ask question for first step

Todo:
1. not working for case 6 -previous_goal remains as -1
2. action argument for wrong step is not, right.

sudo service mongod start

Jan 28
1. Fixed the explaset copy
2. adding pending set generate in select


Todo:
1. fix action argument when other_happen > threshold, action is wrong
2. when other_happen > and feedback is yes we correct the belief

Jan 28
1. fixed_always_kitchen
2. when other_happen > and feedback is yes we correct the belief

Todo:
1. then htn block
2. fix action argument when other_happen > threshold, action is wrong

Jan 29
1. fixed all the cases working for kitchen domain
2. partial block domain fix

Todo:
1. make htn fixed_always work for block domain - so change dataset
2. change the turn_on_function for block domain.
2. fix action argument when other_happen > threshold, action is wrong


Feb 2
1. Fixed the mcts_node variables and __hash__ function. All the observation node with different sample from same belief are considered as one node
2. changed root_node.sample as well.
3. pending_set generate adds pending_set variable in the mcts_node
4. handle the case when the sampled node is the least probable node and the children are 0. In that case the action is a predefined chosen action and step reward is called.
5. node.set_node_info() is set after every select step.
6. step reward is improved to incorporate otherhappen > threshold as well.
7. included other happen in the simulation action selection too.
8. modified uct select to randomly select action if multiple action node have same reward

TODO:
1. see if node.set_info should be added after every  simulation step.
2. fix oracle for kitchen domain
3. work on pomdp-transition function for block domain.


Feb 3
1. Fixed the config.positive_feedback for belief update

Todo:
1. see if node.set_info should be added after every  simulation step.
2. fix oracle for kitchen domain
3. work on pomdp-transition function for block domain.

[1] 12725

Fb 4:
changed step_reward, 
argument of step_reward in tracking engine, 
changed the max function for choose
ask question at last step.


feb 5:
deleted delete trigger for the block domain 
changed the updated with feedback for pomdp

"block": {
        "Single Goal, Correct Steps": [1,2,3,4,5],
        "Multiple Goal, Correct Steps": [6,7,8,9,10],
        "Single Goal, Wrong Steps": [11,12,13,15,23,24,25,26,27,28,29],
        "Multiple Goal, Wrong Steps": [14,16,17,18,19,22,30],
    }

feb 5:
self.start_task is updated in explaset
moved the root_node outside for loop

old .111
case 5 gives error at ON
.142
16 gives error at UN
self
21 gives error at pickup A


block with 0.01
wrong trend for 2, 5, 6,12,13,15

feb 14:
1. re-initialize the self.start_task for every step
2. added the fixed_actions
3. nothing should change the HTN/always fixed for kitchen/blocks domain




feb 20:
1. Add delta to config
2. changed update_with_language_feedback to update based on pending set in explaset and not execute sequence
4. also in update_with_language we shift the step to no if the other_happen is > self.threshold
5. moved the the language feedback update to a position before the other_happen > threshold logic is called
6. changed the logic when inside otherHappen > self.other_happen_threshold for fixed always ask
7. if action_name is ask clarification question and feedback is positive then make the following changes:
        a. change update_db to realStateANDSensorUpdate and do another detection
        b. again do exp.action_posterior() and use the new otherHappen and check against threshold
        c. so explaset is not called always inside otherhappen


8. update without language is same as before and we multiple with 1-p_l
9. add corrective_action in argument in realstateandsensor update, its used for only writing to file.
10. changed other_happen_threshold variable in tracking engine


TOdo:
correct goal accuracyfor the following: 
fixed_always: 1 wrong , 6 wrong, 8 0.8 lower
htn: 12 0.9 and 0.8 has issue in htn where dry_hand becomes 0.
