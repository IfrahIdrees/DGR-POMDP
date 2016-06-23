###############################################################
#Author: Dan Wang <d97wang@uwaterloo.ca>, Dec. 06, 2015
#Given the state change notification, target the just happened step
####################################################################

from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
import json
import pymongo
from helper import *
import json
from pprint import pprint

def step_recog():
    #connect to database
    client = MongoClient()
    db = client.smart_home
    noti_path = 'state_change_notification.json'
    state_change = get_notification(noti_path)
    step = find_step(state_change, db)
    update_database_state(state_change, db)
    return step
    

#######################Functions##############################
##############################################################
##open the notification file
def get_notification(noti_path):
    state_change = []
    with open(noti_path) as json_data:
        state_change.append(json.load(json_data))
        json_data.close()
    return state_change    
    
##target the step
def find_step(state_change, db):
    operator = db.operator
    stepSet = []
#Step1: search candidate steps in the database according to the first state change 
    x = state_change[0]
    queryKey = "effect."+x["name"]+"."+x["change"][0]
    stepSet = operator.find({queryKey:x["change"][2]})
    stepSet = list(stepSet)
       
#Step2: check if those candidate steps also contributes to other state change
    state_change_len = len(state_change)
        #filter the stepset according to effect length       
    stepSet = filter(lambda item: len(item["effect"])==state_change_len, stepSet)
        #check if state_change match the effect list
    stepSet = filter(lambda item: effect_list_compare(item["effect"], state_change) is True, stepSet)
    
#Step3: check their precondition if satisfied in the last step environment state
    stepSet = filter(lambda item: precond_check(item["precondition"], db) is True, stepSet)
    return stepSet
##compare the effect list "dict_effect" with the "state change"    
def effect_list_compare(dict_effect, state_change):
    for x in state_change:
        if x["name"] not in dict_effect:
            return False
        else:
            this_Effect = dict_effect[x["name"]]
            attribute_key = (this_Effect.keys())[0]
            if (attribute_key != x["change"][0]) or (this_Effect[attribute_key] != x["change"][2]):
                return False   
    return True
    
##to check if the precondtion of the step is satisfied    
def precond_check(dict_precond, db): 
    state = db.state 
    for x in dict_precond:
        target_object = state.find({"name":x})
        keys = dict_precond[x].keys()
        for k in keys:
            if k!="ability" and target_object[0][k]!=dict_precond[x][k]:
                return False
    return True
        
       
def update_database_state(state_change, db):
    state = db.state
    for x in state_change:
        print x["change"][0]
        print x["change"][2]
        
        result = state.update_many(
            {"name":x["name"]},
            {
                "$set":{x["change"][0]:x["change"][2]}
            }
        )
        print result.modified_count


#step_recog()


