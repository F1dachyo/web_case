import json
from flask import Flask, jsonify, request, Blueprint, render_template
from db_data import db_session
from db_data.users import User
from db_data.cases import Case
from db_data.skins import Skin
from random import randint

app = Flask(__name__)
api = Blueprint('api', __name__)


@app.route('/')
def index():
    return render_template('index.html', title="InvokerCase_beta")

  
@app.route('/login', methods=['POST'])
def login():
    # args: name, hashed_pass(md5)
    data = request.get_json()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == data['name'], User.hashed_password == data['hashed_pass']).first()
    if user:
        res = {'id': user.id, 'name': user.name, 'hashed_pass': user.hashed_password, 'balance': user.balance}
    else:
        res = {'error': "Login or password are incorrect"}
    return jsonify(res)


@api.route('/register', methods=['POST'])
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


@api.route('/get_case_image', methods=['POST'])
def get_case_image():
    # id
    data = request.get_json()
    db_sess = db_session.create_session()
    case = db_sess.query(Case).filter(Case.id == data['id'])
    res = {'image_bytes': case.image_bytes}
    return jsonify(res)


@api.route('/get_skin_image', methods=['POST'])
def get_skin_image():
    # id
    data = request.get_json()
    db_sess = db_session.create_session()
    skin = db_sess.query(Skin).filter(Skin.id == data['id'])
    res = {'image_bytes': skin.image_bytes}
    return jsonify(res)


@api.route('/get_case', methods=['POST'])
def get_case():
    # id
    data = request.get_json()
    db_sess = db_session.create_session()
    case = db_sess.query(Case).filter(Case.id == data['id'])
    res = {
        'id': case.id,
        'name': case.name,
        'price': case.price,
        'image_bytes': case.image_bytes,
        'skins_ids': case.skins_ids
    }
    return jsonify(res)


@api.route('/get_skin', methods=['POST'])
def get_skin():
    # id
    data = request.get_json()
    db_sess = db_session.create_session()
    skin = db_sess.query(Skin).filter(Skin.id == data['id'])
    res = {
        'id': skin.id,
        'name': skin.name,
        'rarity': skin.rarity,
        'price': skin.price,
        'image_bytes': skin.image_bytes
    }
    return jsonify(res)


@api.route('/open_case', methods=['POST'])
def open_case():
    # case_id
    # TEMPORARY
    data = request.get_json()
    db_sess = db_session.create_session()
    case = db_sess.query(Case).filter(Case.id == data['id'])
    skins_ids = case.skins_ids.split(',')
    skin = db_sess.query(Skin).filter(Skin.id == skins_ids[randint(0, len(skins_ids) - 1)])
    res = {
        'id': skin.id,
        'name': skin.name,
        'rarity': skin.rarity,
        'price': skin.price,
        'image_bytes': skin.image_bytes
    }
    return jsonify(res)

if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.register_blueprint(api, url_prefix='/api')
    app.run(port=5000, host='127.0.0.1', debug=True)
