
# Connection to mongodb

# admin UI: http://localhost:8081/

# localhost:27017
# database: loxia
# collection: sessions

from pymongo import MongoClient

client = MongoClient()

# Todo: get connection info from env file / vars, together with docker-compose?
client = MongoClient('mongodb://%s:%s@mongodb:27017/' % ("root", "example"))
db = client['loxia']
sessionsColl = db['sessions']

testPost = {"foo": "bar"}

recordId = sessionsColl.insert_one(testPost).inserted_id

print(recordId)
