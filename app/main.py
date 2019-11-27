from flask import Flask, escape, request, render_template, send_from_directory
import random # debug/dev
import logging
import json
import datetime
import collections

import sys
sys.dont_write_bytecode = True # debug

#from SUBDIRECTORY import FILE - requires the subdir to have __init__.,py file. Delete .pyc files before trying this!
from src import loxia_database

app = Flask(__name__)


def datetimeToJson(datetimeObject):
  if isinstance(datetimeObject, datetime.datetime):
    return datetimeObject.__str__()


@app.route("/")
def index():
  name = request.args.get("name", "World")
  return f'Hello, {escape(name)}!'


@app.route("/sessions")
def sessions():
  cacheb = random.randint(0,10000) # debug/dev

  db = loxia_database.db()
  resultDict = db.getFiles()

  # Creating a sorted dictionary. 
  # Todo: Check sorting: which filed is sorted by?
  orderedDict = collections.OrderedDict(sorted(resultDict.items(), reverse=False))
#  resultDict.sort()
  debug = json.dumps(resultDict, default = datetimeToJson)

  return render_template("sessions.html", cacheb=cacheb, documents=orderedDict, debug=debug)


@app.route("/segment")
def segment():
  file_id = request.args.get("file_id")
  cacheb = random.randint(0,10000) # debug/dev
  return render_template("segment.html", file_id=file_id, cacheb=cacheb)


# http://localhost/api/segment?file_id=ks/HLO10_20191102_022600.wav&segmentNumber=150
@app.route("/api/segment", methods=['GET'])
def apiSegment():
  # Todo: input sanitization
  file_id = str(request.args.get("file_id")) # Todo: try removing str
  segmentNumber = int(request.args.get("segmentNumber")) # Todo: try removing int

#  res = "FOOBAR" + fileId + segmentNumber
#  res = "DEBUG: "

  db = loxia_database.db()
  resultJson = db.getSegment(file_id, segmentNumber)

  return resultJson, 200


# http://localhost/api/annotation/count?file_id=ks/HLO10_20191102_022600.wav&segmentNumber=150
@app.route("/api/annotation/count", methods=['GET'])
def apiAnnotationCount():
  # Todo: input sanitization
  file_id = str(request.args.get("file_id")) # Todo: try removing str
  segmentNumber = int(request.args.get("segmentNumber")) # Todo: try removing int

  db = loxia_database.db()
  count = db.getAnnotationCount(file_id, segmentNumber)

  countDict = {}
  countDict['count'] = count
  countJson = json.dumps(countDict)

  return countJson, 200


@app.route("/api/annotation", methods=['POST'])
def apiAnnotation():
  # Todo: move logic to a module. But how, to avoid import troubles?
  # Todo: remove logging here?
  logging.basicConfig(filename='api.log',level=logging.DEBUG)

  dataDict = request.get_json()
  logging.info(type(dataDict))

  db = loxia_database.db()

  result = {}
  result = db.saveAnnotation(dataDict)

  return {
        "debug": dataDict,
        "status": "ok",
        "result": result
  }, 200

@app.route("/api/agg", methods=['GET'])
def apiAgg():
  import pprint
  db = loxia_database.db()
  result = db.getSegmentsPerFile()

#  return "RESULT: " + str(result)
#  return str(type(result))
  return json.dumps(list(result))



if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=80)

