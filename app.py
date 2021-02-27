from flask import Flask, render_template, url_for, request, redirect
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)
client = MongoClient(os.getenv("MONGOURL"))
db = client.bookmarkmanagement   #Select the database
#db.authenticate(name=os.getenv("MONGO_USERNAME"),password="os.getenv("MONGO_PASSWORD")")
bookmarkcollection = db.bookmarkcollection #Select the collection


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        bookmark_name = request.form['name']
        url = request.form['url']
        new_bookmark = {"name":bookmark_name, "url": url, "date_created": datetime.utcnow()}
        try:
            bookmarkcollection.insert_one(dict(new_bookmark))
            return redirect('/')
        except Exception as e:
            print(e)
            return "There was an issue adding your bookmark %r" % (e)
    else:
        bookmarks = bookmarkcollection.find()
        return render_template('index.html', bookmarks=bookmarks)

@app.route('/delete/<string:id>')
def delete(id):
    try:
        bookmarkcollection.remove({"_id":ObjectId(id)})
        return redirect('/')
    except Exception as e:
        print(e)
        return "There was an issue deleting your bookmark: %r" % (e)

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    bookmark=bookmarkcollection.find_one({"_id":ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        date_created = datetime.utcnow()
        try:
            bookmarkcollection.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "url":url, "date_created":date_created}})
            return redirect('/')
        except Exception as e:
            print(e)
            return "There was an issue updating your bookmark %r" % (e)
    else:
        return render_template('update.html', bookmark=bookmark)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=80)

