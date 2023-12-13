from http import HTTPStatus

from flask import Flask, render_template, request

from flask_restful import reqparse, abort, Api, Resource

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Integer, String
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, mapped_column
)


app = Flask(__name__, )
api = Api(app)



class Base(DeclarativeBase): pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment.db"

# initialize the DB App
db.init_app(app)


# ================================== Data Base Modal ==================================
class BookDB(db.Model):
    __tablename__ = "Books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)




# ================================== Flask Routes ==================================
@app.route("/", methods=('GET',))
def main():
    if request.method == "GET":
        return render_template("index.html")
    else:       # POST and other methods
        return "This method is not supported", HTTPStatus.METHOD_NOT_ALLOWED  # 405 Not Allowed




#  ================================== Flask Restful API ==================================
def abort_if_book_doesnt_exist(book_id):
    book = db.get_or_404(BookDB, book_id)
    
    # if book_id not in TODOS:
    if not book:
        abort(404, message="Book {} doesn't exist".format(book_id))
    return book


def get_data_json(data):
    return {"id": data.id, "name": data.name}


parser = reqparse.RequestParser()
parser.add_argument('book_name')

#  ================================== API routes ==================================
class Books(Resource):
    def get(self, book_id):
        book = abort_if_book_doesnt_exist(book_id)
        return get_data_json(book)

    def delete(self, book_id):
        book = abort_if_book_doesnt_exist(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

    def put(self, book_id):
        data = request.json
        print(data)
        book = abort_if_book_doesnt_exist(book_id)
        book.name = data['book_name']
        db.session.commit()
        db.session.refresh(book)
        return get_data_json(book)

class BooksList(Resource):
    def get(self):
        books = BookDB.query.all()
        books_list = [get_data_json(book) for book in books]
        return books_list

    def post(self):
        args = request.json
        new_book = BookDB(name=args['book_name'])
        db.session.add(new_book)
        db.session.commit()
        db.session.refresh(new_book)
        return get_data_json(new_book), 201


api.add_resource(BooksList, '/books')
api.add_resource(Books, '/books/<book_id>')

