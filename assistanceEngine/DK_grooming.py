import datetime
from treelib import Tree


####################################################################
#this is the domain knowledge for activity recognition. The domain knowledge
#include:(1)operator, (2)method, 
#(3)the tree for each method. The tree for each method here is only used for
#the initialization of activity recognition, many useful information are not stored

#the real tree is generated during the real activity recognition process

#In the tree there may be duplicate node, I modified the library to avoid to duplicate
#node checking
 
####################################################################

operators = {}
#this function is used to update the operators in the domain knowledge
def declare_operators(*op_list):  #function borrow from pyhop
    """
    Call this after defining the operators, to tell Pyhop what they are. 
    op_list must be a list of functions, not strings.
    """
    operators.update({op.__name__:op for op in op_list})
    return operators

methods = {} #it's a dict mapping string tasks to functions
def declare_methods(task_name,*method_list): #borrow from pyhop
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

#for each method, create a small tree, all those trees are stored in\
#the arraylist, "forest" 
forest = [] 
#------------------------------------------------------------------------#
#-------------------from here is domain knowledge------------------------#

#-------------------------------------------------------------------------
#----------------face_washing---------------------------------------------
def turn_on_faucet(state, person):
    if state.faucet['faucet'] == 'off' and state.person_loc['person_loc'] == 'wash_room':
        state.faucet['faucet'] = 'on'
        return state
    else: return False

def turn_off_faucet(state, person):
    if state.faucet['faucet'] == 'on' and state.person_loc['person_loc'] == 'wash_room':
        state.faucet['faucet'] = 'off'
        return state
    else: return False
    
def wash_face(state, person):
    if state.person_face['person_face'] == 'dirty' and state.person_loc['person_loc'] =='wash_room' and  state.faucet['faucet'] == 'on': 
        #here we need more sensors, like information from camera to verify the person wash_face
        state.person_face['person_face'] = 'clean'
        return state
    else: return False

#add these operators into the operator list
declare_operators(turn_on_faucet, turn_off_faucet, wash_face)

def face_washing(state,person):
    
    if state.person_loc['person_loc'] == 'wash_room':
        #x = py.person_loc['person_loc']
        return['ordered', 'nosplit',('turn_on_faucet', person),  #ordered means subtasks are ordered
                ('wash_face', person), ('turn_off_faucet', person)]
    return False

#declare method for face_washing
declare_methods('face_washing',face_washing)


def face_washing_tree():
    ## Create the the tree for face_washing
    tree = Tree()
    tree.create_node("face_washing", "face_washing")  # root node
    tree.create_node("turn_on_faucet", "turn_on_faucet", parent="face_washing")
    tree.create_node("turn_off_faucet", "turn_off_faucet", parent="face_washing")
    tree.create_node("wash_face", "wash_face", parent="face_washing")
    return tree

tree = face_washing_tree()
forest.append(tree)

#-------------------------------------------------------------------------#
#----------------toothbrushing---------------------------------------------#
#additional operator for prepare water
def add_water_cylinder(state, person):
    if state.cylinder_haswater['cylinder_haswater'] == 'False' and state.faucet['faucet'] == 'on' \
    and state.person_loc['person_loc'] =='wash_room':
        state.cylinder_haswater['cylinder_haswater'] = 'True'
        return state
    else:return False
    
declare_operators(add_water_cylinder)

#methods for prepare water
def prepare_water(state, person):
    if state.person_loc['person_loc'] == 'wash_room':
        return['ordered','nosplit',('turn_on_faucet', person),('add_water_cylinder', person), \
               ('turn_off_faucet', person)]
    return False

declare_methods('prepare_water',prepare_water)

def prepare_water_tree():
    ## Create the the tree for face_washing
    tree = Tree()
    tree.create_node("prepare_water", "prepare_water")  # root node
    tree.create_node("turn_on_faucet", "turn_on_faucet", parent="prepare_water")
    tree.create_node("add_water_cylinder", "add_water_cylinder", parent="prepare_water")
    tree.create_node("turn_off_faucet", "turn_off_faucet", parent="prepare_water")
    return tree

tree = prepare_water_tree()
forest.append(tree)

#operator for teeth brushing
def take_toothbrush(state, person): #this already exist
    if state.toothbrush_on['toothbrush_on'] == 'table' and state.person_loc['person_loc'] == 'wash_room':
        state.toothbrush_on['toothbrush_on'] = 'hand'
        return state
    else: return False
    
def put_paste(state, person):
    if state.toothbrush_haspaste['toothbrush_haspaste']=='False' and state.toothbrush_on['toothbrush_on'] == 'hand':
        state.toothbrush_haspaste['toothbrush_haspaste'] = 'True'
        return state
    else: return False 
     
def brush_teeth(state, person):
    if state.person_teeth['person_teeth'] == 'False' and state.toothbrush_on['toothbrush_on'] == 'hand' \
    and state.toothbrush_haspaste['toothbrush_haspaste'] == 'True' and state.cylinder_haswater['cylinder_haswater']=='True':
        state.person_teeth['person_teeth'] = 'True'
        state.cylinder_haswater['cylinder_haswater'] = 'False'
        state.toothbrush_haspaste['toothbrush_haspaste'] = 'False'
        return state
    else: return False
    
def putdown_toothbrush(state, person):
    if state.toothbrush_on['toothbrush_on'] == 'hand' and state.toothbrush_haspaste['toothbrush_haspaste'] == 'False':
        state.toothbrush_on['toothbrush_on'] = 'table'
        return state
    else: return False

declare_operators(take_toothbrush, put_paste, brush_teeth, putdown_toothbrush)

def toothbrushing(state, person):
    if state.person_teeth['person_teeth'] == 'False' and state.person_loc['person_loc'] == 'wash_room':
        return['ordered','nosplit', ('prepare_water', person), ('take_toothbrush', person), \
               ('put_paste', person), ('brush_teeth', person), ('putdown_toothbrush', person)]
    return False 


declare_methods('toothbrushing',toothbrushing)

def toothbrushing_tree():
    ## Create the the tree for face_washing
    tree = Tree()
    tree.create_node("toothbrushing", "toothbrushing")  # root node
    tree.create_node("prepare_water", "prepare_water", parent="toothbrushing")
    tree.create_node("take_toothbrush", "take_toothbrush", parent="toothbrushing")
    tree.create_node("put_paste", "put_paste", parent="toothbrushing")
    tree.create_node("brush_teeth", "brush_teeth", parent = "toothbrushing")
    tree.create_node("putdown_toothbrush", "putdown_toothbrush", parent ="toothbrushing")
    return tree

tree = toothbrushing_tree()
forest.append(tree)

#-------------------------------------------------------------------------#
#----------------hair combing---------------------------------------------#
#one of the operator for hair combing
def take_comb(state, person):
    if state.comb_on['comb_on'] == 'table' and state.person_loc['person_loc'] == 'wash_room':
        state.comb_on['comb_on'] = 'hand' 
        return state
    else: return False
    
def combing(state, person):
    if state.person_haircombed['person_haircombed'] == 'False' and state.comb_on['comb_on'] == 'hand':
        state.person_haircombed['person_haircombed'] = 'True'
        return state
    else: return False
    
def put_down_comb(state, person):
    if state.comb_on['comb_on'] == 'hand' and state.person_loc['person_loc'] == 'wash_room':
        state.comb_on['comb_on'] = 'table'
        return state
    else: return False

declare_operators(take_comb, combing, put_down_comb)

#methods for comb hair
def comb_hair(state, person):
    if state.person_haircombed['person_haircombed'] == 'False' and state.person_loc['person_loc'] == 'wash_room':
        return['ordered', 'nosplit',('take_comb', person),('combing', person),\
                ('put_down_comb', person)]
    return False

declare_methods('comb_hair',comb_hair)

def comb_hair_tree():
    ## Create the the tree for face_washing
    tree = Tree()
    tree.create_node("comb_hair", "comb_hair")  # root node
    tree.create_node("take_comb", "take_comb", parent="comb_hair")
    tree.create_node("combing", "combing", parent="comb_hair")
    tree.create_node("put_down_comb", "put_down_comb", parent="comb_hair")
    return tree

tree = comb_hair_tree()
forest.append(tree)

##method for grooming
def grooming(state, person):
    #using the current time and the location of the person to predict whether grooming is in process
    if datetime.datetime.now().time() < datetime.time(hour=23, minute = 30) and\
     state.person_loc['person_loc'] == 'wash_room':
        #print 'compare success'
        return ['unordered', 'nosplit', ('face_washing', person),('toothbrushing', person), ('comb_hair', person)]
    else: 
        #print 'compare failed'
        return False

declare_methods('grooming',grooming)

def grooming_tree():
    ## Create the the tree for face_washing
    tree = Tree()
    tree.create_node("grooming", "grooming")  # root node
    tree.create_node("face_washing", "face_washing", parent="grooming")
    tree.create_node("toothbrushing", "toothbrushing", parent="grooming")
    tree.create_node("comb_hair", "comb_hair", parent = "grooming")
    return tree

tree = grooming_tree()
forest.append(tree)
'''
print "##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
print "this is the domain knowledge for this problem"
print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
for x in forest:
    x.show(line_type = "ascii")
'''

