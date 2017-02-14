################################################################################################
####                    This file simulate the actions related to care-giver                ####
################################################################################################

#exit the agent tracking process due to sensor die
def call_for_caregiver_sensor_cause(bad_sensor):
    print "Some sensor is not working well now. Please fix them"
    print "The non-working sensors are":
    for sensor in bad_sensor:
        print sensor["object"], "-----", sensor["attribute"]
    exit(0)
