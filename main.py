import json

import requests as requests
import base64
from flask import Flask, jsonify, request, Blueprint, render_template, redirect
from flask_login import login_user, login_required, logout_user
from db_data import db_session
from db_data.users import User
from db_data.cases import Case
from db_data.skins import Skin
from random import randint
from flask_login import LoginManager

from forms.loginform import LoginForm
from forms.registerform import RegisterForm

app = Flask(__name__)
api = Blueprint('api', __name__)
app.config['SECRET_KEY'] = 'invoker_case_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    cases = get_cases()
    return render_template('index.html', title="InvokerCase_beta", cases=cases)


def open_case_by_id(id):
    db_sess = db_session.create_session()
    case = db_sess.query(Case).filter(Case.id == id).first()
    skins_id = case.skins_ids.split(', ')
    skins_line = []
    for skins in range(387):
        skin = db_sess.query(Skin).filter(Skin.id == skins_id[randint(0, len(skins_id) - 1)]).first()
        res = {
            'id': skin.id,
            'name': skin.name,
            'rarity': skin.rarity,
            'price': skin.price,
            'image_bytes': base64.b64encode(skin.image_bytes).decode("utf-8")
        }
        skins_line.append(res)
    return skins_line


@app.route('/case/<int:id>')
def open_case(id):
    items = open_case_by_id(id)
    duration = randint(10000, 15000)
    print(duration)
    return render_template('open_case.html', title="InvokerCase_beta", duration=duration,
                           items=items, win_elem=int((duration / 300) + (387 / 2)))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        params = {
            "name": form.email.data,
            "hashed_pass": form.password.data
        }
        user_data = requests.post('http://127.0.0.1:5000/api/login', json=params).text
        user = db_sess.query(User).filter(User.name == params["name"]).first()
        if user and user.check_password(params["hashed_pass"]):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@api.route('/login', methods=['POST'])
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


@api.route('/balance', methods=['POST'])
def balance():
    db_sess = db_session.create_session()
    return jsonify(db_sess.query(User).filter(User.email == request.get_json()['email']).first().balance)


@api.route('/balance_case', methods=['POST'])
def balance_case():
    # url, email,

    data = request.get_json()
    case_id = int(data['url'].split('case')[1].split('/')[1])

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == data['email']).first()
    print(user.balance)
    case = db_sess.query(Case).filter(Case.id == case_id).first()
    if user.balance >= case.price:
        user.balance -= case.price
        db_sess.commit()
        return jsonify('success')
    else:
        return jsonify('insufficient balance')



@api.route('/sell', methods=['POST'])
def sell():
    # text
    data = request.get_json()
    price = round(float(data['text'].split()[2].replace(',', '.')))
    print(price)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == data['email']).first()
    user.balance += price
    db_sess.commit()
    print(user.balance)
    return ''


def get_cases():
    # id
    # data = request.get_json()
    db_sess = db_session.create_session()
    cases = db_sess.query(Case)
    answer = []
    for case in cases:
        res = {
            'id': case.id,
            'name': case.name,
            'price': case.price,
            'image_bytes': base64.b64encode(case.image_bytes).decode("utf-8"),
            'skins_ids': case.skins_ids
        }
        answer.append(res)
    return answer


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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.register_blueprint(api, url_prefix='/api')
    app.run(port=5000, host='127.0.0.1', debug=True)