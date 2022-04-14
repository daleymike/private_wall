from crypt import methods
import bcrypt
from flask_app import app
from flask import get_flashed_messages, render_template, redirect, request, session, flash 
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')

    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }

    user_id = User.save(data)
    session['user_id'] = user_id

    return redirect('/dashboard')



@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {'id': session['user_id']}
    results = User.get_all(data)
    user = results[0]
    
    get_all_users = User.get_all_users()

    message_data = {'receiver_id': session['user_id']}
    get_messages = Message.get_messages(message_data)

    return render_template("dashboard.html", user = user, get_all_users = get_all_users, get_messages = get_messages)
