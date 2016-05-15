#Aril 12th 2016
#This is the client simulator

import random
import client
#1
face_washing = [['faucet', 'on'],['person_face','clean'],['faucet', 'off']]

#2
teeth_brushing = [['faucet', 'on'], ['cylinder_haswater', 'True'],['faucet','off'],['toothbrush_on','hand'],['toothbrush_haspaste', 'True'],['person_teeth,cylinder_haswater,toothbrush_haspaste','True,False,False'],['toothbrush_on', 'table']]

#3
comb_hair = [['comb_on', 'hand'], ['person_haircombed','True'], ['comb_on', 'table']]



current_task = []
pool = [1, 2, 3]
label = True

def simulate_action():
    emotion = ''
    object_name = ''
    object_state = ''
    if len(client.current_task) == 0:
        if len(client.pool) == 0:
            print "the job has done"
            return ('done', 'done', 'done')
        else:
            num = random.choice(client.pool)
            client.pool.remove(num)
            if num == 1:
                client.current_task = client.face_washing
            elif num == 2:
                client.current_task = client.teeth_brushing
            else:
                client.current_task = client.comb_hair
    #print "the current task is", client.current_task
    
    if random.random() <= 0.6:  #in this case, the client will do something
        #print "the client did something"
        #firstly generate emotion
        if client.label == True:
            emotion = 'confident'
        else:
            #emotion = 'happy'
            emotion = 'independent'
            client.label = True
        this_change = client.current_task[0]
        #print "this_change is", this_change
        object_name = this_change[0]
        object_state = this_change[1]
        client.current_task.remove(this_change)
    else: #in this case, the client will do nothing
        #firstly generate emotion
        if client.label == True:
            #emotion = 'worried'
            #emotion = 'frustrated'
            emotion = 'upset'
            client.label = False
        else:
            emotion = 'frustrated'
            #emotion = 'depressed'
    #print "after updateing, the current task is", client.current_task                
    return (object_name, object_state, emotion)
    
  
  



