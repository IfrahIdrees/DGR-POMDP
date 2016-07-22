from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.smart_home


class DB_Object(object):
    method = db.method
    operator=db.operator
    state=db.state
    


    def find_all_method(self): ## find all the method, and return as a list
        method=db.method
        return list(method.find())
        #retrun mlist
        
    def get_operator(self, op_name): ## return the specific action
        op = list(operator.find({"st_name":op_name}))
        return op[0]
    
    
    def get_object_state(self, ob_name): ##return the state of a specific object
        ob = list(state.find({"ob_name":ob_name}))
        return ob[0]
            

operator=db.operator
state = db.state
