'''
mongoDB 활용, 데이터 입출력
실행 후 localhost:5000 에서 확인 가능
'''

from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.

    mystars = list(db.mystar.find({},{'_id':False}).sort('like',-1))

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'mystars': mystars})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    current_like = db.mystar.find_one({'name': name_receive})['like']
    new_like = current_like+1
    print(new_like)
    db.mystar.update_one({'name':name_receive},{'$set':{'like':new_like}})
    return jsonify({'result': 'success', 'msg': '좋아요 완료!'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']

    db.mystar.delete_one({'name':name_receive})
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '삭제완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)