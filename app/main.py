from flask import Flask, escape, request, render_template, send_from_directory
import random
import logging

#from SUBDIRECTORY import FILE - requires the subdir to have __init__.,py file. Delete .pyc files before trying this!
from src import loxia_database

app = Flask(__name__)


@app.route("/")
def index():
  name = request.args.get("name", "World")
  return f'Hello, {escape(name)}!'


@app.route("/segment")
def segment():
  segment = request.args.get("segment", "0")
  cacheb = random.randint(0,10000)
  return render_template("segment.html", segment=segment, cacheb=cacheb)


@app.route("/api/annotation", methods=['POST', 'GET'])
def api():
  # Todo: move logic to a module. But how, to avoid import troubles?
  logging.basicConfig(filename='api.log',level=logging.DEBUG)

  json = request.json
  logging.info("allTags: ")
  logging.info(json)

  db = loxia_database.db()
  recordId = db.saveAnnotation("FOO")

  return {
        "status": "ok",
        "insertedRecordId": recordId
  }, 200



if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=80)

