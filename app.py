from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmark.db'
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __retr__(self):
        return '<Bookmark %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        bookmark_name = request.form['name']
        url = request.form['url']
        new_bookmark = Bookmark(name=bookmark_name,url=url)

        try:
            db.session.add(new_bookmark)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your bookmark"
    else:
        bookmarks = Bookmark.query.order_by(Bookmark.date_created).all()
        return render_template('index.html', bookmarks=bookmarks)

@app.route('/delete/<int:id>')
def delete(id):
    bookmark_to_delete = Bookmark.query.get_or_404(id)

    try:
        db.session.delete(bookmark_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting your bookmark"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    bookmark = Bookmark.query.get_or_404(id)

    if request.method == 'POST':
        bookmark.name = request.form['name']
        bookmark.url = request.form['url']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your bookmark"
    else:
        return render_template('update.html', bookmark=bookmark)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=80)

