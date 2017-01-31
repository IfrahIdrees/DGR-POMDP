"""To start mongoDB"""
mongo
"""To show all the dbs"""
show dbs
"""To use a db"""
use db_name
"""To show all the collections in the current db"""
show collections
"""To delete / drop a collection"""
db.collection_name.drop()

"""clear a collection"""
db.collection_name.remove({})

"""import .json file into the database"""

mongoimport --db smart_home --collection state_1 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_1.json
mongoimport --db smart_home --collection state_2 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_2.json
mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/operators.json
mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state.json


'''import command for folder kbexa_uncertain_20160718'''
mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160718/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160718/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160718/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160718/sensor.json


'''import command for folder kbexa_uncertain_20160728'''
mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160728/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160728/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160728/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160728/sensor.json

'''import command for folder kbexa_uncertain_20160815'''

mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160815/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160815/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160815/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20160815/sensor.json


'''import command for folder kbexa_uncertain_20170124'''

mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170124/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170124/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170124/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170124/sensor.json


'''import command for folder kbexa_uncertain_20170130'''
mongoimport --db smart_home --collection method --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/method.json

mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/state.json

mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/operator.json

mongoimport --db smart_home --collection sensor --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/sensor.json

mongoimport --db smart_home --collection Rstate --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/kbexa_uncertain_20170130/realState.json






