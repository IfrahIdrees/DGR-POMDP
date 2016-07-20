from pymongo import MongoClient
import pymongo

def explaSetInit(explaSet):
    client = MongoClient()
    db = client.smart_home
    method=db.method
    goal = list(method.find())
    explaSet = [x["start_action"] for x in goal if len(x["start_action"])>0]
    


