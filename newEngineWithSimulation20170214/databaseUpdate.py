import os
from pymongo import MongoClient
client = MongoClient()
db = client.smart_home

db.method.drop()
db.state.drop()
db.operator.drop()
db.sensor.drop()
db.Rstate.drop()

os.system("mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/method.json")
os.system("mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/state.json")
os.system("mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/operator.json")
os.system("mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/sensor_0.9.json")
os.system("mongoimport --db smart_home --collection Rstate --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/realState.json")

