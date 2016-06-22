

#Function: "dict_same" is used to compare two dict
#DataSource: the two dict come from the mongoDB database
#Caution: do not compare property "_id"
def dict_same(dict_1, dict_2):
    if len(dict_1)!=len(dict_2):
        return False
    keys = dict_1.keys()
    for x in keys:
        if x!="_id" and dict_1.get(x)!=dict_2.get(x):
            return False     
    return True

