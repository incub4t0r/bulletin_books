from flask import Flask, render_template, request, redirect
import requests
import json
from datetime import datetime
import secrets

app = Flask(__name__)

def random():
    rand = secrets.token_urlsafe(6)
    return rand

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/textbooks/listbook", methods=["GET", "POST"])
def listbook():
    return render_template("listbook.html")


@app.route("/textbooks/newbook", methods=["POST"])
def newbook():
    # each database insertion should have a hash associated with book title
    # database insertion should happen here.
    deleteCode = random()
    print(deleteCode)
    # email = request.form["userEmail"]
    return render_template("listbook.html")


# @app.route("/textbooks/submit", methods=["POST"])
# def submit():
#     try: 
#         form = request.form
#         print(form)
#         # print(request.form["bookTitle"])
#         return ("new book submitted")
#     except:
#         return ("error")

@app.route("/textbooks/isbnsearch", methods=["POST", "GET"])
def isbnsearch():
    if request.method == "GET":
        return render_template("newbook.html")
    elif request.method == "POST":
        try:
            isbn = request.form["bookISBN"].strip("-").rstrip()
            reqRaw = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")
            reqLoad = json.loads(reqRaw.text)
            # print(reqLoad)
            authorList = []
            authorStr = ""
            authors = reqLoad["authors"]
            for authorKey in authors:
                authorLink = authorKey["key"]
                authRaw = requests.get(f"https://openlibrary.org{authorLink}.json")
                authLoad = json.loads(authRaw.text)
                name = authLoad["name"]
                authorList.append(name)
            authorStr = (', '.join(authorList))
            publisher = reqLoad["publishers"][0]
            return render_template("newbook.html", results=reqLoad, authors=authorStr, publisher=publisher)

            # return render_template("isbnsearch.html", results=reqLoad, authors=authorStr, publisher=publisher)
        except:
            return render_template("newbook.html", error="Error, cannot find ISBN.")
    else:
        return render_template("error.html")

@app.route("/about", methods=["GET"])
def about():
    if request.method == "GET":
        return render_template("about.html")
    else:
        return render_template("error.html")


@app.route("/textbooks/delete", methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        return render_template("delete.html")
    elif request.method == "POST":
        try:
            deletionCode = request.form["deletionCode"]
            return render_template("delete.html", success=f"Successfully deleted {deletionCode}")
        # write logic to search table and delete
        except:
            return render_template("delete.html", error="Something went wrong")
    else:
        return render_template("error.html")

app.run(host="0.0.0.0", debug=True)

