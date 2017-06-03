
# GoalRecognitionAndPlanning
Code for Thesis: 

Hierarchical Task Recognition and Planning in Smart Homes with Partial Observability

Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)

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

