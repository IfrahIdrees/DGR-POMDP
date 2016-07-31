import sys
sys.dont_write_bytecode = True


from pymongo import MongoClient
import pymongo
from helper import compare_ability

client = MongoClient()
db = client.smart_home


class DB_Object(object):
    def __init__(self):
        self._method = db.method
        self._operator = db.operator
        self._state = db.state
        self._sensor = db.sensor
    ########################method related#########################333
    #################################################################333    
    ## find all the method, and return as a list
    def find_all_method(self): 
        return list(self._method.find())
    ## find and return the specific method
    def find_method(self, m_name):
        method = list(self._method.find({"m_name":m_name}))
        return method[0]
    
    
    ########################operator related###############################
    #######################################################################    
    ## find and return the specific action  
    def get_operator(self, op_name): 
        op = list(self._operator.find({"st_name":op_name}))
        return op[0]
    
    
    ###########################belief state related#################################
    #########################################################################
    ##find and return the state of a specific object
    def get_object_status(self, ob_name): 
        ob = list(self._state.find({"ob_name":ob_name}))
        return ob[0]
    
    ##find and return the all possible values for a specific attribute of an object     
    def get_object_attri(self, ob_name, attri_name):
        st = list(self._state.find({"ob_name":ob_name}))
        return (st[0][attri_name])        
    
            
    ##find and return the attribute value belief from belief state
    def get_attribute_prob(self, s, ob_name, attri_name):
        #print s, "  ", ob_name, "   ", attri_name
        st = list(self._state.find({"ob_name":ob_name}))
        if attri_name == "ability":
            if compare_ability(s, st[0][attri_name]) == True: return 1.0
            else: return 0.0
        
        #print st
        return float(st[0][attri_name][s])
        
        
    ##find and return the prob for p(obs|s)
    def get_obs_prob(self, s, ob_name, attri_name):
        sensor = list(self._sensor.find({"ob_name":ob_name, "attri_name":attri_name}))
        sensor = sensor[0]
        if sensor["value"][0]==s:
            return sensor["reliability"]
        else:
            return (1-sensor["reliability"])/(sensor["value"][1]-1)
    
    ##find and return the parent list
    ##firstly search in the method collection
    ##if not find, search the operator collection
    def get_parent_list(self, name):
        #step1: search the method collection
        parent = list(self._method.find({"m_name":name}))
        if len(parent)==0:
            parent = list(self._operator.find({"st_name":name}))
        if len(parent)==0:
            return False
        return parent[0]["parent"]
        
        
        #step2: search the operator collections
        
    
    
    
    
    
    ##update belief state            
    def update_state_belief(self, ob_name, attri_name, attri_distri):
        result = self._state.update_many(
            {"ob_name":ob_name},
            {
                "$set":{
                    attri_name:attri_distri
                }
            }
        )
        
        print "then uber of changes is", result.matched_count
      


