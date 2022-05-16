from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import secrets
import string
import yagmail
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import xmltodict

# from flask_talisman import Talisman


load_dotenv()

APP_PASSWORD = os.getenv('APP_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')


app = Flask(__name__)
# Talisman(app)

# db configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    edition = db.Column(db.String(100))
    condition = db.Column(db.String(50))
    price = db.Column(db.Numeric(10))
    deleteCode = db.Column(db.String(10))


db.create_all()


# Functions
def createNewBook(bookTitle, userEmail, bookEdition, bookCond, bookPrice, bookDeleteCode):
    try:
        newBook = Book(title=bookTitle, email=userEmail, edition=bookEdition,
                       condition=bookCond, price=bookPrice, deleteCode=bookDeleteCode)
        db.session.add(newBook)
        db.session.commit()
        return True
    except:
        return False


def deleteBook(deleteCode):
    try:
        bookToDelete = db.session.query(Book).filter(
            Book.deleteCode == deleteCode).first()
        db.session.delete(bookToDelete)
        db.session.commit()
        return True
    except:
        return False


def listBooks():
    try:
        allBooks = db.session.query(Book).all()
        return allBooks
    except:
        return None


def searchBook():
    return


def emailUserCode(userEmail, bookTitle, deleteCode):
    sender = EMAIL_SENDER
    appPassword = APP_PASSWORD
    to = userEmail

    subject = f'Your deletion code for {bookTitle} on Bulletin Books'
    mailContent = ["Hi there!", f"You recently posted {bookTitle} on Bulletin Books.",
                   " ", f"The deletion code associated with the book is {deleteCode}."]

    with yagmail.SMTP(sender, appPassword) as yag:
        try:
            yag.send(to, subject, mailContent)
            return True
        except:
            return False


def worldcat(isbn):
    reqRaw = requests.get(
        f"http://classify.oclc.org/classify2/Classify?isbn={isbn}&summary=true")
    reqLoad = json.loads(json.dumps(xmltodict.parse(reqRaw.text)))

    # print(json.dumps(xmltodict.parse(reqRaw.text)))
    try:
        bookTitle = (reqLoad["classify"]["work"]["@title"])
    except:
        print("test")
        bookTitle = (reqLoad["classify"]["works"]["work"][1]["@title"])
        print(bookTitle)
            # publisher = (reqLoad["classify"]["authors"]["author"][0]["#text"].strip("[Publisher]"))
    try:
        tempAuthor = reqLoad["classify"]["authors"]["author"]
        if type(tempAuthor) is list:
            author = (reqLoad["classify"]["authors"]["author"][1]["#text"])
        elif type(tempAuthor) is dict:
            author = (reqLoad["classify"]["authors"]["author"]["#text"])
    except:
        tempAuthor = reqLoad["classify"]["works"]["work"][1]["@author"]
        author = tempAuthor
    # author = (reqLoad["classify"]["authors"]["author"][1]["#text"].strip(""))
    # edition = (reqLoad["classify"]["work"]["@editions"])
    # return (bookTitle, author, edition)
    return (bookTitle, author)


# def openlibrary(isbn):
#     isbn = request.form["bookISBN"].strip("-").rstrip()
#     reqRaw = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")
#     reqLoad = json.loads(reqRaw.text)
#     authorList = []
#     authorStr = ""
#     authors = reqLoad["authors"]
#     for authorKey in authors:
#         authorLink = authorKey["key"]
#         authRaw = requests.get(
#             f"https://openlibrary.org{authorLink}.json")
#         authLoad = json.loads(authRaw.text)
#         name = authLoad["name"]
#         authorList.append(name)
#     authorStr = (', '.join(authorList))
#     publisher = reqLoad["publishers"][0]
#     return render_template("newbook.html", results=reqLoad, authors=authorStr, publisher=publisher)

# Flask paths


def random():
    alphabet = string.ascii_letters + string.digits
    rand = ''.join(secrets.choice(alphabet) for i in range(6))
    return rand


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/textbooks/listbook", methods=["GET", "POST"])
def listbook():
    books = listBooks()
    if books != None:
        return render_template("listbook.html", books=books)
    else:
        return render_template("listbook.html", error="oh no!")


@app.route("/textbooks/newbook", methods=["POST"])
def newbook():
    if request.method == "POST":
        deleteCode = random()
        userEmail = request.form["userEmail"]
        bookTitle = request.form["bookTitle"]
        bookCond = request.form["bookCond"]
        bookPrice = request.form["bookPrice"]
        bookEdition = request.form["bookEdition"]
        bookCreation = createNewBook(
            bookTitle, userEmail, bookEdition, bookCond, bookPrice, deleteCode)
        if bookCreation:
            codeEmail = emailUserCode(userEmail, bookTitle, deleteCode)
            if codeEmail:
                return redirect(url_for('listbook'), code="302")
            else:
                deleteBook(deleteCode)
                return render_template(url_for('newbook'), error="Something went wrong")
        else:
            return render_template(url_for('newbook'), error="Something went wrong")

    else:
        return redirect(url_for('listbook'), code="302")

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
            bookTitle, author = worldcat(isbn)
            return render_template("newbook.html", bookTitle=bookTitle, authors=author)
            # return render_template("newbook.html", bookTitle=bookTitle, authors=author, bookEdition=edition)
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
            print(deletionCode)
            query = deleteBook(deletionCode)
            if query:
                return render_template("delete.html", success=f"Successfully deleted {deletionCode}")
            return render_template("delete.html", error="Something went wrong, maybe you had the wrong code?")
        except:
            return render_template("delete.html", error="Something went wrong")
    else:
        return render_template("error.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
