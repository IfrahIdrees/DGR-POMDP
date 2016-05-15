#this file store the state in time t and time t+1
#
#In a simulation mode, state are obtained based on sensors
#
#Getting signal form sensor-->signal analysis-->state at time t+1


#-------------------log Mar 23 2016---------------------------
#change the element name of state in order to identify input
#input is from keyboard to simulate the artificial change of 
#state. changes as follows:
#

"""
state_t.loc-->state_t.person_loc = {'person_loc':'wash_room'}
state_t.teeth-->state_t.person_teeth = {'person_teeth':False}
state_t.face-->state_t.person_face = {'person_face':'dirty'}
state_t.faucet = {'faucet':'off'} No change
state_t.on -->state_t.toothbrush_on = {'toothbrush_on':'table'}
state_t.haspaste-->state_t.toothbrush_haspaste ={'toothbrush_haspaste':False}
state_t.haswater-->state_t.cylinder_haswater ={'cylinder_haswater':False}
state_t.combon-->state_t.comb_on = {'comb_on': 'table'}
state_t.haircombed-->state_t.person_haircombed = {'person_haircombed':False}

initial thing
state_t = State()
state_t.loc = {'grandpa':'wash_room'}
state_t.teeth = {'grandpa':False}
state_t.face = {'grandpa':'dirty'}
state_t.faucet = {'faucet':'off'}
state_t.on = {'toothbrush':'table'}
state_t.haspaste ={'toothbrush':False}
state_t.haswater ={'cylinder':False}
state_t.combon = {'comb': 'table'}
state_t.haircombed = {'grandpa':False}
"""



from ClassforHierarActRec import State
import copy
import statefile

##situation awareness at time t
state_t = State()
state_t.person_loc = {'person_loc':'wash_room'}
state_t.person_teeth = {'person_teeth':'False'}
state_t.person_face = {'person_face':'dirty'}
state_t.faucet = {'faucet':'off'}
state_t.toothbrush_on = {'toothbrush_on':'table'}
state_t.toothbrush_haspaste ={'toothbrush_haspaste':'False'}
state_t.cylinder_haswater ={'cylinder_haswater':'False'}
state_t.comb_on = {'comb_on': 'table'}
state_t.person_haircombed = {'person_haircombed':'False'}


##situation awareness at time t+1
state_t1 = State()
state_t1.person_loc = {'person_loc':'wash_room'}
state_t1.person_teeth = {'person_teeth':'False'}
state_t1.person_face = {'person_face':'dirty'}
state_t1.faucet = {'faucet':'off'}
state_t1.toothbrush_on = {'toothbrush_on':'table'}
state_t1.toothbrush_haspaste ={'toothbrush_haspaste':'False'}
state_t1.cylinder_haswater ={'cylinder_haswater':'False'}
state_t1.comb_on = {'comb_on': 'table'}
state_t1.person_haircombed = {'person_haircombed':'False'}

def updatestate(object_state_name, object_state_value):
    #print "before update"
    #print statefile.state_t.__dict__
    #print statefile.state_t1.__dict__
    statefile.state_t = copy.deepcopy(statefile.state_t1)
    length = len(object_state_name)
    for x in range(0, length):
        statefile.state_t1.__dict__[object_state_name[x]][object_state_name[x]] = object_state_value[x]
    return
    
'''
def updatestatewithout():
	state_t = copy.deepcopy(state_t1)
	return

'''


