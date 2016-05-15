
import copy
import random
import uuid
from FuncforHierarActRec import updatedata
import DK_grooming
import ClassforHierarActRec


def Complete_tree_update(label, prompttree, state_t1, person):
    #label is the ID of the just completed action.
    #update the completeness data of the tree
    #print "this is inside compelte tree update"

    splitlable = True
    label1 =label
    tree = copy.deepcopy(prompttree._tree)
    
    node = tree.get_node(label)
    
    node.data._completeness = True
    
    while (label != tree.root):
        #print "in this while loop, need update the completeness of tasks"
        node = tree.get_node(label)
        parent  = node.bpointer
        #print "the checking node is", tree.get_node(parent).tag
        updatedata(tree.subtree(parent))
        label = parent
    
    #update the tree structure, because now the state has changes
    #some branches might became infeasible  
    checknodeID = [] #only store the ID for these node
    checknodeID.append(tree.root)
       
    while checknodeID:
        nodeID = random.choice(checknodeID)
        #print "inside while"
        #print tree.get_node(nodeID).tag
        if tree.get_node(nodeID).data._completeness == True:
            #print tree.get_node(nodeID).tag, "is removed"
            checknodeID.remove(nodeID)
            
        elif tree.get_node(nodeID).tag in DK_grooming.operators:
            #print "this is an atomic task"
            #check if precondition is satisfied
            operator = DK_grooming.operators[tree.get_node(nodeID).tag]
            statenow = copy.deepcopy(state_t1)
            thisparent = tree.get_node(nodeID).bpointer
            thisparent = tree.get_node(thisparent)
            ##########################################################################################################
            #if operator(statenow, person) == False and thisparent.data._start == False:  #precondition unsatisfied  #
             #   print "this node is removed from the tree"                                                         #
              #  tree.remove_node(nodeID)                                                                           #
              #######################################################################################################                     
            checknodeID.remove(nodeID)
 
            
        elif tree.get_node(nodeID).data._start == True:
            #print "this task already started"
            #print tree.get_node(nodeID).tag
            if tree.get_node(nodeID).data._split == False:
                splitlable = False
                
           
            children = tree.get_node(nodeID).fpointer
            
                
            #print "the started task has the number of children", len(children)
            checknodeID.remove(nodeID)
            
            for x in children:
                #print "the child are", tree.get_node(x).tag
                checknodeID.append(x)
            
        else:
            #print "this task is composite, and has not start"
            method = DK_grooming.methods[tree.get_node(nodeID).tag][0]
            subtask = method (copy.deepcopy(state_t1), person)
            #print "the number of subtask is", len(subtask)
            thisparent = tree.get_node(nodeID).bpointer
            thisparent = tree.get_node(thisparent)
            if subtask == False and thisparent.data._start == False: # precondition no longer satisfy
                #print "I am removeing this childr"
                
                tree.remove_subtree(nodeID)
                checknodeID.remove(nodeID)
                
            elif subtask !=False: #precondition satisfied
                #firstly, clear its children and then re-decompose
                #print "this tasks precondition satisfied now", nodeID
                #print len(tree.get_node(nodeID).fpointer)
                while len(tree.get_node(nodeID).fpointer) > 0:
                    children = tree.get_node(nodeID).fpointer
                    #print "the node is", tree.get_node(children[0]).tag
                    tree.remove_subtree(children[0])
                    
              
                #add current subtasks (because under different state, might choose different subtasks)
                if subtask[0] == "ordered":
                    #print "this tree is ordered", tree.get_node(nodeID).tag                 
                    tree.get_node(nodeID).data._childrenrelation = 0
                    if subtask[1] == 'split':
                        tree.get_node(nodeID).data._split = True
                        #paste other subtasks into the tree 
                        for i in range(2, len(subtask)):
                            if subtask[i][0] in DK_grooming.operators:
                                childdata = ClassforHierarActRec.Operator_my_data()
                                childdata._order = i-1
                                childID = uuid.uuid4()
                                tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)                            
                                checknodeID.append(childID)
                            else:
                                childdata = ClassforHierarActRec.Method_my_data()
                                childdata._order = i-1
                                childID = uuid.uuid4()
                                tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)                                
                                checknodeID.append(childID)
                    else: #unordered
                        if subtask[1] == 'split':
                            tree.get_node(nodeID).data._split = True
                        for i in range(2, len(subtask)):
                            if subtask[i][0] in DK_grooming.operators:
                                childdata = ClassforHierarActRec.Operator_my_data()
                                childID = uuid.uuid4()
                                tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)
                                checknodeID.append(childID) 
                            else:
                                childdata = ClassforHierarActRec.Method_my_data()
                                childID = uuid.uuid4()
                                tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)
                                checknodeID.append(childID)
                    
            checknodeID.remove(nodeID) 
    prompttree._prior_prompt_set = []
    prompttree._promp_set = []
    #tree.show(line_type = "ascii")

    
    while (label != tree.root):
        #print "in this while loop, need update the completeness of tasks"
        node = tree.get_node(label)
        #print node.tag

        parent  = node.bpointer
        #print tree.get_node(parent).tag
        updatedata(tree.subtree(parent))
        label = parent
         
    prompttree._tree = copy.deepcopy(tree)
    prompttree._splitlabel = splitlable    
    
    return prompttree                
