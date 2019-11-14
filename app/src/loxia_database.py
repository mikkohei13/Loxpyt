
# Connection to mongodb

# admin UI: http://localhost:8081/

# localhost:27017
# database: loxia
# collection: sessions

from pymongo import MongoClient

class db():

  def __init__(self):
    # pass ??
#    self._client = MongoClient()

    # Todo: get connection info from env file / vars, together with docker-compose?
    client = MongoClient('mongodb://%s:%s@mongodb:27017/' % ("root", "example"))

    db = client['loxia']
    self._sessionsColl = db['sessions']
    self._filesColl = db['files']

  def saveSession(self, data):
    recordId = self._sessionsColl.insert_one(data).inserted_id
    print(recordId)
    print("Inserted session")

  def saveFile(self, data):
    recordId = self._filesColl.insert_one(data).inserted_id
    print(recordId)
    print("Inserted file")



# testPost = {"foo": "bar"}


# print(recordId)


