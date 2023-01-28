
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