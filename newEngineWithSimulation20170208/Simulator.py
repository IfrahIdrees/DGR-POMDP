import sys
sys.dont_write_bytecode = True

from database import *
from helper import *

db = DB_Object()


##given the happened step, update the realState in database
def realStateANDSensorUpdate(step_name):
    with open('result.txt', 'a') as f:
        f.write("\n\n")
        f.write("======================================================================================\n")
        new_line = "Simulate step happen:     " + step_name + "\n"
        f.write(new_line)
        
        
    
    #print
    #print
    #print "Simulate step happen:     ",step_name
    op = db.get_operator(step_name)
    effect = op["effect"]
    for obj in effect:
        for att in effect[obj]:
            db.update_obj_Rstate(obj, att, effect[obj][att])
            db.update_sensor_value(obj, att, effect[obj][att])
    return
    
##given the happened step, udpate the corresponding sensor value


