from random import randint
import recommender
from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommend.sqlite3'
app.config['SECRET_KEY'] = "random string"

db2 = SQLAlchemy(app)


class book(db2.Model):
      id = db2.Column('id',db2.Integer,primary_key = True)
      title = db2.Column(db2.String(100))
      author = db2.Column(db2.String(100))
      rating = db2.Column(db2.String(20))
      description = db2.Column(db2.String(2000))
      def __init__(self,  title, author, rating, description):
                   self.title = title
                   self.author = author
                   self.rating = rating
                   self.description = description

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/book',methods=['GET','POST'])
def book_search():
    if(request.method=='POST'):
        book_title=request.form['book_title']
        if(book_title==""):
            return redirect('/book')
        else:
            return redirect(url_for('book_output',id=book_title))
    else:
        boo=[]
        i=randint(1,96)
        for x in range(i,i+5):
            books=book.query.filter_by(id = x).first()
            boo.append(books)
        return render_template('book.html',books=boo)

@app.route('/book/<id>',methods=['GET'])
def book_output(id):
    book_recommendation=[]
    ani=recommender.recommend(id)
    if ani!=0:
        for books in ani:
            anim=book.query.filter_by(title = books).first()
            book_recommendation.append(anim)
        return render_template("book_output.html",book=book.query.filter_by(title = id).first(),book_recommendation=book_recommendation)
    else:
        demo=[]
        i=randint(1,95)
        for x in range(i,i+5):
            anim=book.query.filter_by(id = x).first()
            demo.append(anim)
        return render_template('book_output.html',book=book.query.filter_by(title = id).first(),book_recommendation=0,books=demo)

if __name__=="__main__":
    db2.create_all()
    app.run(debug=True)