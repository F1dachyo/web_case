import json
from flask import Flask, jsonify, request
from db_data import db_session
from db_data.users import User

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    # args: name, hashed_pass(md5)
    data = request.get_json()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == data['name'], User.hashed_password == data['hashed_pass']).first()
    res = {'id': user.id, 'name': user.name, 'hashed_pass': user.hashed_password, 'balance': user.balance}
    return jsonify(res)


@app.route('/register', methods=['POST'])
def register():
    # args: name, hashed_pass(md5)
    data = request.get_json()
    db_sess = db_session.create_session()
    user = User()
    user.name = data['name']
    user.hashed_password = data['hashed_pass']
    user.balance = 0
    db_sess.add(user)
    db_sess.commit()
    return '', 200


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=5000, host='127.0.0.1', debug=True)