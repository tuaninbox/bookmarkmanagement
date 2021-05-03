from flask import Flask, render_template, url_for, request, redirect
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)
client = MongoClient(os.getenv("MONGOURL"))
db = client.bookmarkmanagement   #Select the database
#db.authenticate(name=os.getenv("MONGO_USERNAME"),password="os.getenv("MONGO_PASSWORD")")
bookmarkcollection = db.bookmarkcollection #Select the collection (table)
foldercollection = db.foldercollection 
usercollection = db.usercollection 

@app.route('/',methods=['GET'])
def home():
    client_ip = request.access_route[0]
    output="<html>Your IP Address: {}</html>".format(client_ip.split(":")[0])
    return output, 200
    
@app.route('/bm',methods=['POST','GET'])
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


################################# FOLDERS ################################
@app.route('/folders',methods=['POST'])
def folders():
    if request.method == 'POST':
        folder_name = request.form['folder']
        new_folder = {"name":folder_name}
        try:
            foldercollection.insert_one(dict(new_folder))
            return redirect('/settings')
        except Exception as e:
            print(e)
            return "There was an issue adding your folder %r" % (e)
    else:
        return redirect(url_for("settings"))

@app.route('/folders/delete/<string:id>')
def deletefolder(id):
    try:
        foldercollection.remove({"_id":ObjectId(id)})
        return redirect('/settings')
    except Exception as e:
        print(e)
        return "There was an issue deleting your bookmark: %r" % (e)

@app.route('/folders/update/<string:id>',methods=['POST','GET'])
def updatefolder(id):
    folder=foldercollection.find_one({"_id":ObjectId(id)})
    if request.method == 'POST':
        name = request.form['folder']
        try:
            foldercollection.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name}})
            return redirect('/settings')
        except Exception as e:
            print(e)
            return "There was an issue updating your folder %r" % (e)
    else:
        folders = foldercollection.find()
        users = usercollection.find()
        return render_template('settings.html', folders=folders,folder=folder,users=users)

################################### USERS ####################################
@app.route('/users',methods=['POST'])
def users():
    if request.method == 'POST':
        user_name = request.form['user']
        new_user = {"name":user_name}
        try:
            usercollection.insert_one(dict(new_user))
            return redirect('/settings')
        except Exception as e:
            print(e)
            return "There was an issue adding your user %r" % (e)
    else:
        return redirect(url_for("settings"))

@app.route('/users/delete/<string:id>')
def deleteuser(id):
    try:
        usercollection.remove({"_id":ObjectId(id)})
        return redirect('/settings')
    except Exception as e:
        print(e)
        return "There was an issue deleting your bookmark: %r" % (e)

@app.route('/users/update/<string:id>',methods=['POST','GET'])
def updateuser(id):
    user=usercollection.find_one({"_id":ObjectId(id)})
    if request.method == 'POST':
        name = request.form['user']
        try:
            usercollection.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name}})
            return redirect(url_for('settings'))
        except Exception as e:
            print(e)
            return "There was an issue updating your folder %r" % (e)
    else:
        folders = foldercollection.find()
        users = usercollection.find()
        return render_template('settings.html', folders=folders,users=users,user=user)
########################### SETTINGS #######################
@app.route('/settings',methods=['GET'])
def settings():
    folders = foldercollection.find()
    users = usercollection.find()
    return render_template('settings.html', folders=folders, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=80)

