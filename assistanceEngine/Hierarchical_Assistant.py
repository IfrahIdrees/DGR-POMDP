#########################################################################################
#Author: Dan Wang <d97wang@uwaterloo.ca>, Dec. 09, 2015
#Hierarchical_Assistant.py function
#Given the completed hierarchical tree, generate the possible next step and provide prompt
#the prompt can be in different level. The level of prompt should begin with highest level, 
#and go to detail level when nothing happened after later prompt(this part can be combined 
#with affective computing) 
###########################################################################################
#import Complete_Hierarchical_tree
import FuncforHierarActRec
import ClassforHierarActRec
import DK_grooming
import copy

def Hierarchical_prompt(C_Hierar_Trees):
    #print "\n Inside Hierarchical _prompt!"

    #complete tree under state_t1
    complete_tree = copy.deepcopy(C_Hierar_Trees)
    #prompt set is multiple dimension matrix. 
    #each complete tree has a prompt list in which different level of prompt are stored
    #for complete trees generate under same state changes, if the next step belongs to one
    #of the prompt list, other complete trees and their corresponding partial trees should be deleted
    #if next step doesn't belong to any of them, generate new partial tree and complete tree, but need
    #to record the time. 
    
    '''
    for x in complete_tree:
        print x._tree.show(line_type = "ascii")
    '''
    
    operators = DK_grooming.operators
    promptset = []
    
    #   print len(complete_tree)
    for treeclass in complete_tree:
        #print treeclass.root 
        
        tree = copy.deepcopy(treeclass._tree)
        #record the root ID of the tree, it is a label
        #it relate the prompt list with a specific complete tree
        #and also a partial tree
        #the element of a prompt list is dict (task_name:ID in the tree)
        promptlist = []
        prioritylist = []
        
        level_list = []
        level_list.append(tree.root) #only store the node ID
        promptlist.append(level_list)
        prioritylist.append(level_list)
        
        label = True
        while label:
            level_list = []
            level_priority_list = []
            checklist = promptlist[len(promptlist)-1]
            checkprioritylist = prioritylist[len(prioritylist)-1]
            leafnum = 0
            for x in checklist:
                currentnode = tree.get_node(x)
                #print "I am checking the childe of", currentnode.tag
                if currentnode.is_leaf() == True: #current node is leaf node
                    leafnum +=1
                elif currentnode.data._completeness == True:
                    pass
                else: #current node is not leaf
                    childID = currentnode.fpointer #get the child ID
                    #print "the number of child of is", len(childID)
                    if currentnode.data._childrenrelation == 0: #children are ordered
                        #put in order
                        childID = FuncforHierarActRec.put_in_sequence(childID, tree)
                        for i in range(0, len(childID)):
                            thisnode = tree.get_node(childID[i])
                            if thisnode !=None and thisnode.data._completeness == False:
                                #print "I am checking whether the wash face is true"
                                #print tree.get_node(childID[i]).tag
                                if x in checkprioritylist: #should update priority list
                                    level_priority_list.append(childID[i])
                                level_list.append(childID[i])
                                break    
                    else: #children are unordered
                        for child in childID:
                            if tree.get_node(child).data._completeness == False:
                                level_list.append(child)      
                        if x in checkprioritylist:
                            addone = False
                            for child in childID:
                                thechild = tree.get_node(child)
                                if thechild.tag not in operators:
                                    if thechild.data._completeness == False and thechild.data._start == True:
                                        level_priority_list.append(child)
                                        addone = True
                            if addone == False:
                                level_priority_list.append(childID[0])
                             
    
                                
            if len(checklist) == leafnum:
                label = False
            else:
                if len(promptlist)>0:
                    promptlist.append(level_list)
                if len(prioritylist)>0:
                    prioritylist.append(level_priority_list)
                    
        #print "the length of priority list is", len(prioritylist)
        prior_listvalue = False 
        #this is used to check whether the priority list still
        #has some leaf node that are not completed
        #----
        
        for level in prioritylist:
            for x in level:
                thisnode = tree.get_node(x)
                if thisnode.is_leaf() and thisnode.data._completeness == False:
                    prior_listvalue = True
        if prior_listvalue == False:
            prioritylist = promptlist
            
        #----
        
        #prioritylist = promptlist   
        promptThistree=ClassforHierarActRec.prompset(prioritylist, promptlist, tree, treeclass._splitlabel)                                          
        promptset.append(promptThistree)
        
        #print "after generate the prompt"
        #print tree.show(line_type = "ascii")
    
    '''
    print "--------------------------------------------------------"
    print "this is the prompt result"    
    print "***********output priority prompt set********************"
    treenum = 0
    for x in promptset:
        print "\n"
        
        print "Tree: ", treenum
        levelnum = 0
        print "Level         task_name         parent        ordered or not"
        for y in x._prior_prompt_set:
            for z in y:
                node = x._tree.get_node(z)
                parent = "null"
                ordered = -1
                if node.is_root()==False:
                    parent = node.bpointer
                    ordered = x._tree.get_node(parent).data._childrenrelation
                    parent = x._tree.get_node(parent).tag
                print levelnum, "        ", node.tag, "          ", parent, "              ", ordered
            levelnum = levelnum + 1
        treenum = treenum+1
    '''
    
    '''            
    print "*************output all possible prompt***************"
    treenum = 0
    for x in promptset:
        print "\n"
        print "Tree: ", treenum
        levelnum = 0
        print "Level         task_name         parent        ordered or not"
        for y in x._promp_set:
            #print "this level@@@@@@@@@@@@@@@@@"
            for z in y:
                node = x._tree.get_node(z)
                parent = "null"
                ordered = -1
                if node.is_root()==False:
                    parent = node.bpointer
                    ordered = x._tree.get_node(parent).data._childrenrelation
                    parent = x._tree.get_node(parent).tag
                print levelnum, "        ", node.tag, "          ", parent, "              ", ordered
            levelnum = levelnum + 1
        treenum = treenum + 1    
    '''
    
    return promptset                
