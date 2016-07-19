
import pymongo

def explaSetInit(explaSet):
    client = MongoClient()
    db = client.smart_home
    method=db.method
    step = find_step(state_change, db)
    update_database_state(state_change, db)
    return step
    for i in range(10):
        explaSet.append(i)
    return explaSet


