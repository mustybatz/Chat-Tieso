import os
from time import localtime, strftime

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from flask_socketio import SocketIO, send, emit, join_room, leave_room

from wtform_fields import *
from models import * 


#Configuración de la app
app = Flask(__name__)
app.secret_key = 'secret'

#Configuración de la base de datos.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://szdcmvcdkokcri:1d8f7e17c656bee1fe288624f1eede7ed85355f8322fa929ffb7f802a7ad33aa@ec2-23-21-249-0.compute-1.amazonaws.com:5432/d17fes5fclu14o'
db = SQLAlchemy(app)

#Inicializando Flask-socketio
socketio = SocketIO(app)
ROOMS = ["Principal", "Noticias", "Programación", "Videojuegos"]


#Configurando el login de flask
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    #Actualiza la base de datos si el registro se completa satisfactioriamente.
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        #Agregar usuario a la base de datos.
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registro completado exitosamente. Por favor incia sesión.', 'success')
        return redirect(url_for('login'))



    return render_template("index.html",form = reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    #Permitir acceso si la validación fue verdadera.
    if login_form.validate_on_submit():
        user_object=User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)       


@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    flash('Has cerrado sesión satisfactoriamente.', 'success')
    return redirect(url_for('login'))

""" Chat """

@socketio.on('message')
def message(data):
    socketio.send({'msg':data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%Mp', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " se ha unido a la sala de " + data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " ha abandonado la sala de " + data['room']}, room=data['room'])




if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=6969 , debug=True)