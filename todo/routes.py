from flask import render_template, flash, url_for, redirect, request
from todo import app, db, bcrypt
from todo.forms import *
from todo.model import User, List, ListItem
from flask_login import login_user, logout_user, current_user, login_required
from todo.helpers import sendEmail, getUserFromCode, save_picture


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template("index.html")


@app.route("/home")
@login_required
def home():
    lists = List.query.filter_by(user_id=current_user.id)
    return render_template("home.html", lists=lists,ListItem=ListItem)


@app.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.name}.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["get", "post"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_token=bcrypt.generate_password_hash(hashed_password).decode()
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, token=new_token)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login', 'success')
        login_user(user)
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route("/reset/code", methods=["get", "post"])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        code = form.code.data
        user = getUserFromCode(code)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated!', 'success')
        login_user(user)
        return redirect(url_for('home'))
    return render_template("reset.html", title="Reset", form=form)


@app.route("/reset/", methods=["get", "post"])
def resetRequest():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            sendEmail(user.email)
            flash(f'Password reset email was sent {user.name}.', 'success')
            return redirect(url_for('reset'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("requestReset.html", title="Reset", form=form)

@app.route("/home/list")
@login_required
def editlist():
    form = ListForm()
    if form.validate_on_submit():
        flash('Your list as been created!', 'success')
    return render_template('list.html', title=list, form=form)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)