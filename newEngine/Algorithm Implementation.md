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
> Written with [StackEdit](https://stackedit.io/).