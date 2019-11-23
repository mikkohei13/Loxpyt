
# Connection to mongodb

# admin UI: http://localhost:8081/

# localhost:27017
# database: loxia
# collection: sessions

from pymongo import MongoClient
import datetime
import pprint
import random # debug

class db():

  def __init__(self):
    # pass ??
#    self._client = MongoClient()

    # Todo: get connection info from env file / vars, together with docker-compose?
    client = MongoClient('mongodb://%s:%s@mongodb:27017/' % ("root", "example"))

    db = client['loxia']

    # Todo: move to methods?
    self._sessionsColl = db['sessions']
    self._filesColl = db['files']
    self._segmentsColl = db['segments']
    self._annotationsColl = db['annotations']


  def getDbMetaFields(self):
    data = {}
    data["recordLastModifiedUTC"] = datetime.datetime.utcnow()

    # This adds and element which is not overwritten on upsert, displaying human-readable date for debugging
    data[str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))] = "recordModifiedUTC"
    return data


  def saveSession(self, data):
    _id = { "_id": data.get("_id") }
    data.update(self.getDbMetaFields())

    recordId = self._sessionsColl.update_one(_id, { "$set": data }, True)#.inserted_id
    print(recordId)
    pprint.pprint(data)
    print("Inserted session")


  def saveFile(self, data):
    _id = { "_id": data.get("_id") }
    data.update(self.getDbMetaFields())

    recordId = self._filesColl.update_one(_id, { "$set": data }, True)#.inserted_id
    print(recordId)
    pprint.pprint(data)
    print("Inserted file")


  def saveSegment(self, data):
    _id = { "_id": data.get("_id") }
    data.update(self.getDbMetaFields())

    recordId = self._segmentsColl.update_one(_id, { "$set": data }, True)#.inserted_id
    print(recordId)
    pprint.pprint(data)
    print("Inserted segment")


  def saveAnnotation(self, data):
    _id = { "_id": data.get("segment") }
    data.update(self.getDbMetaFields())

    recordId = self._annotationsColl.update_one(_id, { "$set": data }, True)#.inserted_id
    return _id

# testPost = {"foo": "bar"}


# print(recordId)


