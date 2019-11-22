from flask import Flask, escape, request, render_template, send_from_directory

import random
import logging

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

@app.route("/api", methods=['POST', 'GET'])
def api():
  # Todo: move logic to a module
  logging.basicConfig(filename='api.log',level=logging.DEBUG)
#  keywords = request.form.get('keywords') # POST
#  tags = request.form.get('tags')
#  keywords = request.args.get('keywords') # GET
#  logging.info("logged:" + keywords + tags)


#  tags = request.form['allTags']
#  allTags = request.args.get('allTags') # GET
#  allTags = request.form.get('allTags') # POST
  json = request.json
  logging.info("allTags: ")
  logging.info(json)

  """
  request.get_data()
#  data = request.form()
  dataDict = request.form;
  logging.info(str(dataDict))
  test = ""
  for key, value in dataDict.items():
    logging.info("here1")
    logging.info("here: " + str(value))
    test = test + "|" + value

  logging.info("logged: " + test)
#  logging.info("logged:" + str(request.form))
  """

  return "ok"



if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=80)

