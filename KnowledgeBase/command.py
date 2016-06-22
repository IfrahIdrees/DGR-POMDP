"""import .json file into the database"""

mongoimport --db smart_home --collection state_1 --drop --file ~/Documents/learn_pymongo/state_1.json
mongoimport --db smart_home --collection state_2 --drop --file ~/Documents/learn_pymongo/state_2.json
mongoimport --db smart_home --collection operator --drop --file ~/Documents/learn_pymongo/operators.json




"""clear a collection"""
db.collection_name.remove({})

