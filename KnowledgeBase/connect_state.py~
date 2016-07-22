from datetime import datetime
from pymongo import MongoClient
import pymongo
from helper import *



#connect to mongoDB
client = MongoClient()
db = client.smart_home
state_1 = db.state_1
state_2 = db.state_2
operator = db.operator

state_change_list = []
step_list = []

#Function: compare the s(t-1) and s(t)
#Goal:Return all the objects whose state has been changed.

def compare_state():
    #return value, its a list
    #state_change_list = []
    
    #find the object whose state changed
    cursor_1 = state_1.find()
    for document in cursor_1:   
        cursor_2 = state_2.find({"name":document["name"]})
        if dict_same(cursor_2[0],document) is False:
            state_change_list.append(cursor_2[0])
    
    #return the found objects
    #return state_change_list 
    


#Function: Give "state_change_list", find the steps that can result in the change
#Goal: return all possible step combinations that contribute to the state change
#Attention: here do not consider the situation that: two steps occurred, and the second step destroy the precondition of the first step
def find_first_step():
    #state_change_list = compare_state()
    for x in state_change_list:
        #construct the query key
        xname = x["name"]
        xstate = x["state"]
        key = "effect."+xname+".state"
        #query all the steps who result in the target state of the object type(attention: type)
        stepSet = operator.find({key:xstate}) 
        step_list.extend(step_check(stepSet))
        print (step_list) 
        
                

   
#Function: Given state_1, an abstract step, target object, check if the step is possible
#           need to check precondition(satisfied or not), effects(all effects belongs to
#           the state_change_list)
def step_check(stepSet):
    stepSetList = []
    for step in stepSet:
        stepSetList.append(step)
    for step in stepSetList:
        #check effects
        effect = step["effect"]
        remove_label = False
        for obj in effect:
            if in_state_change_list(obj, effect[obj]) is False:
                #in this case, some effects of the step does not exist in the state change list
                #need to remove this step
                stepSetList.remove(step)
                remove_label = True
                break
        if remove_label is True:
            continue
        else:
            #effects satisfied, now need to check precondition
            precond = step["precondition"]
            # the precondition of this step is not satisfied
            #need to remove this step from the setSetList
            if precond_check(precond) is False: 
                stepSetList.remove(stet)
                break
               
    return stepSetList

    
    
#to check if an object exist in the state_change_list, and has the target state
def in_state_change_list(obj_name, obj_state):
    label = False
    state_keys = obj_state.keys()
    for x in state_change_list:
        if x["name"]==obj_name:
            label = True
            for key in state_keys:
                if obj_state[key] != x[key]:
                    return False
    if label is True:
        return True
    else:
        return False 
           
#to check if the precondition of a step is satisfied in the last time point state_1
def precond_check(precond):
    for x in precond:
        target_object = state_1.find({"name":x})
        precond_key = precond[x].keys()
        for key in precond_key:
            if key == "ability": ##hard code ability constraints here   
                if(compare_ability(target_object[0]["ability"], precond[x][key])) is False:
                    return False
            else: #it is not ability precondition
                if precond[x][key]!=target_object[0][key]:
                    return False 
    return True


#to check whether ability constraints satisfied
#we can add additional compare here
def compare_ability(ab1, pre_ab2):
    #print ("inside compare_ability")
    if pre_ab2[0] == ">=":
        return no_less_than(ab1, pre_ab2)
    return False


def no_less_than(ab1, pre_ab2):
    #print ("inside no less than")
    len_ab1 = len(ab1)
    for i in range(len_ab1):
        if ab1[i] < pre_ab2[i+1]:
           return False
    return True

compare_state()
find_first_step()





"""
cursor_2 = coll_2.find()
for document in cursor_2:
    print(document)
    
    """
####Find or Query data with Pymongo ####################
####example example example##############################
##---------query key:value pair
#cursor = coll.find({"borough": "Manhattan"})
##---------query by field
#cursor = coll.find({"address.zipcode": "10075"})
##----------query in an array
#cursor = db.restaurants.find({"grades.grade": "B"})
##----------specify conditions with operators
#cursor = db.restaurants.find({"grades.score": {"$gt": 30}})
#cursor = db.restaurants.find({"grades.score": {"$lt": 10}})
##-----------combine conditions
#cursor = db.restaurants.find({"cuisine": "Italian", "address.zipcode": "10075"})
#cursor = db.restaurants.find({"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]})

##-------------Sort Query results
"""
cursor = db.restaurants.find().sort([
    ("borough", pymongo.ASCENDING),
    ("address.zipcode", pymongo.ASCENDING)
    ])
"""  
"""  
for document in cursor:
    print(document)
"""    
    
    
 
"""

##example: insert data into the specific collection#####
#########################################################
result = db.restaurants1.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)





####################################################
##############update data with pymongo##################
##using update_one() and update_many()

result = coll.update_one(
    {"name":"Juni"},
    {
        "$set":{
            "cuisine":"American (New)"
        },
        "$currentDate": {"lastModified": True}
    }
)

print (result.matched_count)
print (result.modified_count)

##update the street field in the embedded address dcoument
result = coll.update_one(
    {"restaurant_id":"41156888"}, 
    {"$set":{"address.street":"East 31st Street"}}
)

print (result.matched_count)
print (result.modified_count)

##update multiple document, using update_many()
result = coll.update_many(
    {"address.zipcode": "10016", "cuisine": "Other"},
    {
        "$set": {"cuisine": "Category To Be Determined"},
        "$currentDate": {"lastModified": True}
    }
)

print (result.matched_count)
print (result.modified_count)



##replace a document
result = coll.replace_one(
    {"restaurant_id": "41704620"},
    {
        "name": "Vella 2",
        "address": {
            "coord": [-73.9557413, 40.7720266],
            "building": "1480",
            "street": "2 Avenue",
            "zipcode": "10075"
        }
    }
)
print (result.matched_count)
print (result.modified_count)






##################################################################3
############remove data with pymongo############################33
result = coll.delete_many({"borough":"Manhattan"})
print (result.deleted_count)

#drop a collection, including any indexes
db.restaurants.drop()






###################################################################
###################Data Aggregation with PyMongo#################
cursor = coll.aggregate(
    [
        {"$group": {"_id": "$borough", "count": {"$sum": 1}}}
    ]
)


for document in cursor:
    print (document)


"""




