from flask import Flask, escape, request
app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
#    return "Hello World from Flask"







if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)

