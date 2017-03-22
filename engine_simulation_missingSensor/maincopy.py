##The new main function
import os
import sys
sys.dont_write_bytecode = True

from tracking_engine import*
from pymongo import MongoClient
client = MongoClient()
db = client.smart_home




if __name__ == '__main__':
    
    ############some global variables######################
    #######################################################
    #if there is no notification, the engine still should run 
    #the whole update process if the generated random is bigger than
    #no_notif_trigger_prob
    no_notif_trigger_prob = 0.5
 
    #the sleep interval at each time the engine should sleep.  
    interval = 1
    
    #the conditional probability of p(s|s_t-1, a_t)
    cond_satisfy = 1.0
    cond_notsatisfy = 0.0
    
    #the threshhold that an explanation is no longer maintain
    #delete_trigger = 0.00001
    delete_trigger = 0.001
    
    ##if there is a notification, the probability that nothing happend
    nothing_happen = 0.01
    
    ##the otherHappen triggering threshhold
    other_happen = 1.2
    
    file_num = 4
    #sensor_reliability = [None, 0.9, 0.95, 0.8]
    sensor_reliability = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #sensor_reliability = [None, 0.95, 0.9]
    sensor_reliability = [1, 2, 3, 4, 5, 6]
    #sensor_reliability = [10]
    #files = [1, 2, 3]
    #sensor_reliability = [-1, 0.5, -2]
    #for file_num in range(4, 8):
    for file_num in range(5, 7):
        for x in sensor_reliability:
            ##the output file name
            output_file_name = "Case" + str(file_num) + "_" + str(x) + ".txt"
            ##the input file name
            input_file_name = "Case" + str(file_num)
            #print "This is for ", input_file_name, "The output file is ", output_file_name
            for repeat in range(1, 21):

                #print output_file_name
                ##refresh the database
                db.method.drop()
                db.state.drop()
                db.operator.drop()
                db.sensor.drop()
                db.Rstate.drop()
                sensor_command = ""
                '''
                os.system("mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/method.json --jsonArray")
                os.system("mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/state.json --jsonArray")
                os.system("mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/operator.json --jsonArray")
                os.system("mongoimport --db smart_home --collection Rstate --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/realState.json --jsonArray")
                if x == None:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/sensor.json --jsonArray"
                else:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/sensor" + "_" + str(x) + ".json --jsonArray"
                    
                os.system(sensor_command)
                '''
                
                '''
                os.system("mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/method.json --jsonArray")
                os.system("mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/state.json --jsonArray")
                os.system("mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/operator.json --jsonArray")
                os.system("mongoimport --db smart_home --collection Rstate --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/realState.json --jsonArray")
                if x == None:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/sensor.json --jsonArray"
                else:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/sensor" + "_" + str(x) + ".json --jsonArray"
                os.system(sensor_command)
                '''
                os.system("mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/method.json")
                os.system("mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/state.json")
                os.system("mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/operator.json")
                os.system("mongoimport --db smart_home --collection Rstate --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/realState.json")
                if x == None:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/sensor.json"
                else:
                    sensor_command = "mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170310/sensor" + "_" + str(x) + ".json"
                os.system(sensor_command)
                
                with open(output_file_name, 'a') as f:
                    f.write('\n========================\n')
                    
                tracking_engine = Tracking_Engine(no_trigger = no_notif_trigger_prob, sleep_interval = interval, cond_satisfy=cond_satisfy, cond_notsatisfy = cond_notsatisfy, delete_trigger = delete_trigger, otherHappen = other_happen, file_name = input_file_name, output_file_name = output_file_name)
                tracking_engine.start()
            
            print "I am good until now" 
            ##tracking_engine = tracking_engine()
            


else:
    print 'I am being imported'    
