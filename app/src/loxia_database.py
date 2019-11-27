
# Connection to mongodb

# admin UI: http://localhost:8081/

# localhost:27017
# database: loxia
# collection: sessions

from pymongo import MongoClient
import datetime
import pprint
import uuid
import json

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


  def getDbMetaFields(self, includeUniqueEditedField = True):
    data = {}
    data["recordLastModifiedUTC"] = datetime.datetime.utcnow()

    # This adds and element which is not overwritten on upsert, displaying human-readable date for debugging
    if True == includeUniqueEditedField:
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


  # Todo: Move to main / helpers??
  def datetimeToJson(self, datetimeObject):
    if isinstance(datetimeObject, datetime.datetime):
      return datetimeObject.__str__()


  # Todo: handle if no records found, in both this and api endpoint
  def getSegment(self, file_id, segmentNumber):
    where = {"file_id": file_id, "segmentNumber": segmentNumber}
#    where = {"file_id": "ks/HLO10_20191102_022600.wav", "segmentNumber": 1}

    resultDict = self._segmentsColl.find_one(where)

    resultJson = json.dumps(resultDict, default = self.datetimeToJson)

    return resultJson


  # Todo: Later handle if no records found
  def getFiles(self):
    resultDict = {}
    cursor = self._filesColl.find({})

    for document in cursor:
      resultDict[document['_id']] = document

    return resultDict


  # Todo: Later handle if no records found
  # UNTESTED
  # def getSegmentCount(self, file_id):
  #   resultDict = {}
  #   filter = { "file_id": file_id }
  #   count = self._segmentsColl.count_documents(filter)

  #   return count


  def saveAnnotation(self, data):
    data.update(self.getDbMetaFields(False))

    # Flask does not like object id, so we'll create our own
    data["_id"] = str(uuid.uuid1())

    result = self._annotationsColl.insert_one(data)
    return result.inserted_id

    # Todo: how to return the id?
    # result.inserted_id is object


  def getAnnotationCount(self, file_id, segmentNumber):

    where = {"file_id": file_id, "segmentNumber": segmentNumber}

    count = self._annotationsColl.count_documents(where)

    return count


