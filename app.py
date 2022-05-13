from flask import Flask, render_template

app = Flask(__name__)

def random():
    pass

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/textbooks/listbook")
def listbook():
    return render_template("listbook.html")


@app.route("/textbooks/newbook")
def newbook():
    return render_template("newbook.html")



app.run(host="0.0.0.0", debug=True)

