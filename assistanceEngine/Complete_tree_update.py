
import copy
import random
import uuid
from FuncforHierarActRec import updatedata
import DK_grooming
import ClassforHierarActRec


def Complete_tree_update(label, prompttree, state_t1, person):
    #label is the ID of the just completed action.
    #update the completeness data of the tree
    print "this is inside compelte tree update"
    splitlable = True
    label1 =label
    tree = copy.deepcopy(prompttree._tree)
    node = tree.get_node(label)
    print node.tag
    node.data._completeness = True
    
    while (label != tree.root):
        print "in this while loop, need update the completeness of tasks"
        node = tree.get_node(label)
        print node.tag

        parent  = node.bpointer
        print tree.get_node(parent).tag
        updatedata(tree.subtree(parent))
        label = parent
    
    #update the tree structure, because now the state has changes
    #some branches might became infeasible  
    checknodeID = [] #only store the ID for these node
    checknodeID.append(tree.root)
    while checknodeID:
        nodeID = random.choice(checknodeID)
        print "inside while"
        print tree.get_node(nodeID).tag
        #print tree.get_node(nodeID).data._start
        if tree.get_node(nodeID).data._completeness == True:
            print tree.get_node(nodeID).tag, "is removed"
            checknodeID.remove(nodeID)
            
        elif tree.get_node(nodeID).tag in DK_grooming.operators:
            #check if precondition is satisfied
            operator = DK_grooming.operators[tree.get_node(nodeID).tag]
            statenow = copy.deepcopy(state_t1)
            if operator(statenow, person) == False:  #precondition unsatisfied
                tree.remove_node(nodeID)                     
            checknodeID.remove(nodeID)
            
        elif tree.get_node(nodeID).data._start == True:
            print "this task already started"
            print tree.get_node(nodeID).tag
            if tree.get_node(nodeID).data._split == False:
                splitlable = False
            children = tree.get_node(nodeID).fpointer
            checknodeID.remove(nodeID)
            for x in children:
                checknodeID.append(x)
        else:
            method = DK_grooming.methods[tree.get_node(nodeID).tag][0]
            subtask = method (copy.deepcopy(state_t1), person)
            if subtask == False: # precondition no longer satisfy
                tree.remove_subtree(nodeID)
                checknodeID.remove(nodeID)
                
            else: #precondition satisfied
                #clear its children
                print "this tasks precondition satisfied now", nodeID
                print tree.get_node(nodeID).fpointer
                children = tree.get_node(nodeID).fpointer
                for x in children:
                    tree.remove_subtree(x)
                #add current subtasks (because under different state, might choose different subtasks)
                if subtask[0] == "ordered":                 
                    tree.get_node(nodeID).data._childrenrelation = 0
                    if subtask[1] == 'split':
                        tree.get_node(nodeID).data._split = True
                        #paste other subtasks into the tree 
                        for i in range(2, len(subtask)):
                            if subtask[i][0] in DK_grooming.operators:
                                operator = DK_grooming.operators[subtask[i][0]]
                                statenow = copy.deepcopy(state_t1)
                                if operator(statenow, person) == False:  #precondition unsatisfied
                                    break
                                else:
                                    childdata = ClassforHierarActRec.Operator_my_data()
                                    childdata._order = i-1
                                    childID = uuid.uuid4()
                                    tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)                            
                                    checknodeID.append(childID)
                            else:
                                childmethod = DK_grooming.methods[subtask[i][0]][0]
                                if childmethod(state_t1, person) == False:
                                    break
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
                                operator = DK_grooming.operators[subtask[i][0]]
                                statenow = copy.deepcopy(state_t1)
                                if operator(statenow, person) == False:  #precondition unsatisfied
                                    pass
                                else:
                                    childdata = ClassforHierarActRec.Operator_my_data()
                                    childID = uuid.uuid4()
                                    tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)
                                    checknodeID.append(childID) 
                            else:
                                childmethod = DK_grooming.methods[subtask[i][0]][0]
                                if childmethod(state_t1, person) == False:
                                    pass
                                else:
                                    childdata = ClassforHierarActRec.Method_my_data()
                                    childID = uuid.uuid4()
                                    tree.create_node(subtask[i][0], childID, parent=nodeID, data= childdata)
                                    checknodeID.append(childID)
                    
            checknodeID.remove(nodeID) 
    prompttree._prior_prompt_set = []
    prompttree._promp_set = []
    #tree.show(line_type = "ascii")
    print tree.get_node(label1).tag
    print tree.get_node(label1).data._completeness
    
    
    prompttree._tree = copy.deepcopy(tree)
    prompttree._splitlabel = splitlable    
    
    return prompttree                
