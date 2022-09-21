import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app =  Flask(__name__)
################Database Configuration######################
basedir = os.path.abspath(os.path.dirname(__file__))
#basedir = "C:\Users\DELL\OneDrive\Desktop\Batch_156_160\database\"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

##############################################################

class BookModel(db.Model):
    _tablename_ = "books"
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String())
    book_description = db.Column(db.String())
    country = db.Column(db.String())
    book_writer = db.Column(db.String())



    def __init__(self,book_name,book_description,country,book_writer):
        self.book_name = book_name
        self.book_description = book_description
        self.country = country
        self.book_writer = book_writer



        def __repr__(self):
                return f"{self.book_name}:{self.book_description}"


#@app.before_first_request
#def create_table():
#    db.create_all()
########################################################################################

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'GET':
      return render_template("add.html")


    if request.method == 'POST':
        book_name = request.form['book_name']
        book_description = request.form['book_description']
        country = request.form['country']
        book_writer = request.form['book_writer']


        books = BookModel(
        book_name = book_name,
        book_description = book_description,
        country = country,
        book_writer = book_writer,
        )

        db.session.add(books)
        db.session.commit()
        return redirect('/')





@app.route("/view",methods=['GET'])
def RetriveList():
    books = BookModel.query.all()
    return render_template('index.html',books = books)


@app.route('/<int:id>/update', methods=['GET','POST'])

def update(id):
    books = BookModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        # db.session.delete(books)
        # db.session.commit()

        # if books:
            book_name = request.form['book_name']
            book_description = request.form['book_description']
            country = request.form['country']
            book_writer = request.form['book_writer']


            books.book_name = book_name
            books.book_description = book_description
            books.country = country
            books.book_writer = book_writer




            # books = BookModel(
            #     book_name = book_name,
            #     book_description = book_description,
            #     country = country,
            #     book_writer = book_writer,
            # )

            db.session.add(books)
            db.session.commit()
            return redirect('/')
        #return f"Book with id = {id} Does not exist"
        #books = BookModel.query.filter_by(id=id).first()
    return render_template('update.html',books = books)






@app.route('/<int:id>/delete', methods=['GET','POST'])

def delete(id):
    books = BookModel.query.filter_by(id=id).first()
    if request.method == 'POST':
          if books:
              db.session.delete(books)
              db.session.commit()
              return redirect('/')
          abort(404)
    return render_template('delete.html')

@app.route("/")
def home():
      return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
