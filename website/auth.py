import os
from flask import Blueprint, app,  render_template,render_template_string, request, flash, redirect, url_for
from .models import User, Candidate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import qrcode


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            elif email == 'Teacher@gmail.com' and password == 'Teachers123456789':
                login_user(user, remember=True)
                return redirect(url_for('views.Teacher_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

# Home Page (Voting Interface)

@auth.route('/Candidates')

def index():

    candidates = Candidate.query.all()

    return render_template('home.html', candidates=candidates)


# Cast Vote

@auth.route('/vote/<int:id>', methods=['POST'])

def vote(id):

    candidate = Candidate.query.get_or_404(id)

    candidate.votes += 1

    db.session.commit()

    return redirect(url_for('index'))


# Teacher's Panel (Add Candidates)

@auth.route('/teacher', methods=['GET', 'POST'])

def teacher():

    if request.method == 'POST':

        name = request.form['name']

        description = request.form['description']

        image = request.files['image']

        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        

        new_candidate = Candidate(

            name=name,

            description=description,

            image=filename

        )

        db.session.add(new_candidate)

        db.session.commit()

        return redirect(url_for('teacher'))

    

    candidates = Candidate.query.all()

    return render_template('teacher.html', candidates=candidates)


## This is for the authentication
@auth.route('/Authenticate', methods=['GET', 'POST'] )
@login_required
def Authenticate_user():
    if qrcode.QRCode.verify(input):
        return redirect(url_for('views.home'))
    else:
        flash('Wrong Code', category='error')
    return render_template("Authenticator.html", user=current_user)



## This is for the Image upload and showing
@auth.route('/add_candidate', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if 'image' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            flash('Candidate successfully added', category='success')
            return render_template('display_candidate.html', name=name, description=description, image_filename=filename)
    return render_template('Voting_System_Teachers.html')