from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import os   
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('Home.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    User.save(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if "user_id" in session:
        return redirect("/")
    data = {
        "email": request.form["email"]
    }
    user = User.get_by_email(data)
    if not user:
        flash("User doesn't exist", "userlogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Password is incorrect", "passlogin")
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/wheel')
def wheel():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('wheel.html' , user = user)

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('about.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('profile.html', user = user)

@app.route('/new/profil/pic', methods=['POST'])
def new_profil_pic():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], current_time + filename))
            data["image"] = current_time + filename
            User.update_profile_pic(data)
    return redirect('/profile')


@app.route('/wheelPoint', methods=['POST'])
def wheelPoint():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
        "points": request.form['point']
    }
    User.update_wheel_points(data)
    return redirect('/wheel')