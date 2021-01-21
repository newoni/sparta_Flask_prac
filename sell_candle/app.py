from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost',27017)

db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    tmp_name = request.form['order_name']
    tmp_count = request.form['order_count']
    tmp_addr = request.form['order_address']
    tmp_phone = request.form['order_phone']

    doc = {'name': tmp_name, 'count': tmp_count, 'addr': tmp_addr, 'phone': tmp_phone}

    db.tmp_homework.insert_one(doc)
    return jsonify({'result': 'success', 'msg':'저장 완료'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    data= list(db.tmp_homework.find({},{'_id': False}))
    return jsonify({'result': 'success', 'data':data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)