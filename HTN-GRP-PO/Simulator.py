"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""


##########################################################################
# Simulate the state change in a real environment
##########################################################################


from helper import *
from database import *
import sys
sys.dont_write_bytecode = True
db = DB_Object()


# given the happened step, update the realState in database
def realStateANDSensorUpdate(
        step_name, output_file_name, real_step=True, is_wrong_step_or_belief=False):
    # print("Simulate step: ", step_name)
    if real_step:
        print("\nreal Simulate step: ", step_name, "\n")
        sep = "\t"

    #     with open(output_file_name, 'a') as f:
    #         #version changed in March 14, generate a table
    #         f.write(step_name + "\t")
    else:
        # print("mcts Simulate step: ", step_name)
        sep = "\t"

    #     with open("mcts"+output_file_name, 'a') as f:
    #         #version changed in March 14, generate a table
    #         f.write(step_name + "\t")

    with open(output_file_name, 'a') as f:
        f.write(step_name + sep)

    sensor_notification = []
    op = db.get_operator(step_name)
    effect = op["effect"]
    for obj in effect:
        for att in effect[obj]:
            if real_step:
                db.update_obj_Rstate(obj, att, effect[obj][att])
            if not is_wrong_step_or_belief:
                # in case of simulation we want the sensor_notification to be []
                # so dont even go in update_Sensor which based on sr decide whether
                # sensor notification is []
                # for laguaue we need a new function that updates R and sensor_value but not dependant on threshold
                # do we want to add this output somewhere?
                # we can add new file
                update_result = db.update_sensor_value(
                    obj, att, effect[obj][att], real_step)
                if update_result:
                    new_item = {}
                    new_item["object"] = obj
                    new_item["attribute"] = att
                    new_item["obj_att_value"] = effect[obj][att]
                    sensor_notification.append(new_item)

    return sensor_notification


def update_db(step_index, step_name, output_file_name):

    print("step index", step_index, "Corrective step name is ", step_name)

    with open(output_file_name, 'a') as f:
        f.write(
            "step index" +
            str(step_index) +
            "Corrective step name is " +
            step_name +
            "\n")

    sensor_notification = []
    op = db.get_operator(step_name)
    effect = op["effect"]
    for obj in effect:
        for att in effect[obj]:
            # if real_step:
            db.update_obj_Rstate(obj, att, effect[obj][att])
            # if not is_wrong_step_or_belief:
            # in case of simulation we want the sensor_notification to be []
            # so dont even go in update_Sensor which based on sr decide whether
            # sensor notification is []
            # for laguaue we need a new function that updates R and sensor_value but not dependant on threshold
            # do we want to add this output somewhere?
            # we can add new file
            sensor = list(db._sensor.find(
                {"ob_name": obj, "attri_name": att}))
            sensor = sensor[0]
            valueNum = sensor["value"][1]
            result = db._sensor.update_many(
                {"ob_name": obj, "attri_name": att},
                {
                    "$set": {
                        "value": [effect[obj][att], valueNum]
                    }

                }
            )

            if result:
                new_item = {}
                new_item["object"] = obj
                new_item["attribute"] = att
                new_item["obj_att_value"] = effect[obj][att]
                sensor_notification.append(new_item)

    return sensor_notification
