from flask import Flask, escape, request, render_template, send_from_directory

import random

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




if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=80)

