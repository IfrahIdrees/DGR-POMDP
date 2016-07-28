"""import .json file into the database"""

mongoimport --db smart_home --collection state_1 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_1.json
mongoimport --db smart_home --collection state_2 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_2.json
mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/operators.json
mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state.json


'''import command for folder kbexa_uncertain_July18'''
mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July18/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July18/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July18/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July18/sensor.json


'''import command for folder kbexa_uncertain_July28'''
mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July28/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July28/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July28/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_July28/sensor.json

"""clear a collection"""
db.collection_name.remove({})

