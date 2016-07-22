from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.smart_home


class DB_Object(object):
    def __init__(self):
        self._method = db.method
        self._operator = db.operator
        self._state = db.state
        self._sensor = db.sensor

    ## find all the method, and return as a list
    def find_all_method(self): 
        return list(self._method.find())
        
    ## return the specific action  
    def get_operator(self, op_name): 
        op = list(self._operator.find({"st_name":op_name}))
        return op[0]
    
    ##return the state of a specific object
    def get_object_state(self, ob_name): 
        ob = list(self._state.find({"ob_name":ob_name}))
        return ob[0]
            
    ##return the attribute value belief from belief state
    def get_attribute_prob(self, s, ob_name, attri_name):
        st = list(self._state.find({"ob_name":ob_name}))
        return float(st[0][attri_name][s])
        
        
    ##return the prob for p(obs|s)
    def get_obs_prob(self, s, ob_name, attri_name):
        sensor = list(self._sensor.find({"ob_name":ob_name, "attri_name":attri_name}))
        sensor = sensor[0]
        if sensor["value"][0]==s:
            return sensor["reliability"]
        else:
            return (1-sensor["reliability"])/(sensor["value"][1]-1)
                


