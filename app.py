from flask import Flask, render_template

app = Flask(__name__)

def random():
    pass

@app.route("/")
def index():
    return render_template("index.html")

app.run(host="0.0.0.0", debug=True)

