from flask import Flask, escape, request, render_template, send_from_directory
app = Flask(__name__)

@app.route("/")
def index():
  name = request.args.get("name", "World")
  return f'Hello, {escape(name)}!'

@app.route("/segment")
def segment():
  segment = request.args.get("segment", "0")
  return render_template("segment.html", segment=segment)

@app.route("/spectrogram")
def spectrogram():
  path = "../_exports/noordwijk/5DB0D594.WAV.00000.png"
  file = return send_from_directory('js', path)




if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=80)

