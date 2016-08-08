import sys
sys.dont_write_bytecode = True

from tracking_engine import*




if __name__ == '__main__':
    
    ############some global variables######################
    #######################################################
    #if there is no notification, the engine still should run 
    #the whole update process if the generated random is bigger than
    #no_notif_trigger_prob
    no_notif_trigger_prob = 0
    
    #the sleep interval at each time the engine should sleep.  
    interval = 1
    
    tracking_engine = Tracking_Engine(no_notif_trigger_prob, interval)
    tracking_engine.start()
    tracking_engine.test()
    #tracking_engine.stop()
    #tracking_engine.__detest()
    
    print "I am good until now" 
    #tracking_engine = tracking_engine()



else:
    print 'I am being imported'    
