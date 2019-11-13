
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
    self._client = MongoClient('mongodb://%s:%s@mongodb:27017/' % ("root", "example"))

    self._db = self._client['loxia']
    self._sessionsColl = self._db['sessions']

  def saveSession(self, data):

    # Todo: not a session, but a file
    # Todo: file id must be calculated manually, so that if same file entered multiple times -> no duplicates
    
    recordId = self._sessionsColl.insert_one(data).inserted_id
    print(recordId)
    print("Finished db")



# testPost = {"foo": "bar"}


# print(recordId)


