from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.get_database('sparta')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def write_review():
    form = request.form
    title = form['title']
    author = form['author'],
    review = form['review']

    document = {
        'title': title,
        'author': author,
        'review': review
    }

    db.bookreview.insert_one(document)

    return jsonify(
        {'result': 'success',
         'msg': '저장되었습니다.'}
    )

@app.route('/review', methods=['GET'])
def read_review():
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify(
        {'result': 'success',
         'reviews': reviews}
    )


if __name__ == '__main__':
    app.run(
        '0.0.0.0',
        5000,
        debug = True
    )