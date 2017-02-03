import sys
sys.dont_write_bytecode = True


from pymongo import MongoClient
import pymongo
import random




client = MongoClient()
db = client.smart_home


class DB_Object(object):
    def __init__(self):
        self._method = db.method
        self._operator = db.operator
        self._state = db.state
        self._sensor = db.sensor
        self._Rstate = db.Rstate
    ########################method related#########################333
    #################################################################333    
    ## find all the method, and return as a list
    def find_all_method(self): 
        return list(self._method.find())
    ## find and return the specific method
    def find_method(self, m_name):
        method = list(self._method.find({"m_name":m_name}))
        if len(method)==0:
            return None
        else:
            return method[0]
    
    ##find and return the start actions of the given method
    ##because the given method is the tag of tree root, it must be a goal
        
    def get_start_action(self, m_name):
        method = list(self._method.find({"m_name":m_name}))
        return method[0]["start_action"]
    
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
        st = list(self._state.find({"ob_name":ob_name}))
        ##print st
        ##print attri_name
        ##print s
        return float(st[0][attri_name][s])
    
    ##find and return the attribute value belief from belief state
    ##according to method/operator's precondition!!!!!!!!!!!!!
    ##The difference with get_attribute_prob is that here need to consider
    ##the "ability attribute"
    def get_attribute_prob_1(self, s, ob_name, attri_name):
        #print "inside get_attribute_prob_1"
        #print s, " ", ob_name, " ", attri_name
        st = list(self._state.find({"ob_name":ob_name}))
        #print "the returned state is", st
        if attri_name!="ability":
            #print "the returned value is 1", float(st[0][attri_name][s])
            return float(st[0][attri_name][s])
        else:
            for x in st[0][attri_name]:
                y=x.split(",")
                if self.ability_check(s, y) == True:
                    #print "the returned value is 2 ", st[0][attri_name][x]
                    return st[0][attri_name][x]
                else:
                    #print "the returned value is 3", 1-st[0][attri_name][x]
                    return 1-st[0][attri_name][x]

            
        
    #can only check >= scenario!!!!!!!!!
    def ability_check(self, precond, state):
        for i, x in enumerate(state):
            if i==0: continue
            if float(state[i])<float(precond[i]): return False       
        return True

            
    
    
    #########################sensor reading related#########################
    ########################################################################    
    ##find and return the prob for p(obs|s)
    def get_obs_prob(self, s, ob_name, attri_name):
        #print "Inside database.py, get_obs_prob"
        #print "the ob_name                      ", ob_name
        #print "the attri_name                   ", attri_name
        sensor = list(self._sensor.find({"ob_name":ob_name, "attri_name":attri_name}))
        sensor = sensor[0]
        if sensor["value"][0]==s:
            return sensor["reliability"]
        else:
            return (1-sensor["reliability"])/(sensor["value"][1]-1)
    
    def update_sensor_value(self, ob_name, attri_name, value):
        sensor = list(self._sensor.find({"ob_name":ob_name, "attri_name":attri_name}))
        if len(sensor)!=1:
            print "inside udpate_sensor_value, the number of target ob_name is bad", len(objList)
            sys.exit(0)
        else:
            sensor = sensor[0]
            #print "before update the sensor is", sensor
            randomN = random.random()
            if(randomN<=sensor["reliability"]):
                #print "before update the sensor is", sensor
                valueNum = sensor["value"][1]
                result = self._sensor.update_many(
                    {"ob_name":ob_name, "attri_name":attri_name},
                    {
                        "$set":{
                            "value":[value, valueNum]
                        }
                    
                    }
                )
                
                newsensor = list(self._sensor.find({"ob_name":ob_name, "attri_name":attri_name}))
                #print "after update the sensor is:", newsensor[0]
                
    
    ########################parent node search related#####################
    #######################################################################
    
    
    ##find and return the parent list
    ##firstly search in the method collection
    ##if not find, search the operator collection
    def get_parent_list(self, name):
        #step1: search the method collection
        parent = list(self._method.find({"m_name":name}))
        #step2: search the operator collections
        if len(parent)==0:
            parent = list(self._operator.find({"st_name":name}))
        if len(parent)==0:
            return False
        return parent[0]["parent"]
        
        
        
    ######################belief state update#############################
    ######################################################################
    ##update belief state            
    def update_state_belief(self, ob_name, attri_name, attri_distri):
        '''
        print "inside database.py, update_state_belief:    ", ob_name, attri_name
        thestate =list (self._state.find({"ob_name":ob_name}))
        print "before state update, the distribution is", thestate[0]
        '''
        result = self._state.update_many(
            {"ob_name":ob_name},
            {
                "$set":{
                    attri_name:attri_distri
                }
            }
        )
        
        '''
        thestate =list (self._state.find({"ob_name":ob_name}))
        print "after state update, the distribution is", thestate[0]
        '''
        #print "then number of changes is", result.matched_count
      


    #######################real state update related##########################
    ##########################################################################
    
    ##get the object real state
    def get_obj_Rstate(self, ob_name):
        objList = list(self._Rstate.find({"ob_name":ob_name}))
        if len(objList)!=1:
            print "inside get_obj_Rstate, the number of target ob_name is bad", len(objList)
            sys.exit(0)
        else:
            return objList[0]
            
    ##update the object real state given the ob_name, attri_name, and attri_value        
    def update_obj_Rstate(self, ob_name, attri_name, attri_value):
        result = self._Rstate.update_many(
            {"ob_name":ob_name},
            {
                "$set":{
                    attri_name:attri_value
                }
            }
        )
        #print "the number of changes is", result.matched_count
