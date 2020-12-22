from blog.models import User, Post
from flask import render_template, url_for, redirect, flash
from blog.forms import LoginForm, RegisterForm
from blog import app

posts = [
    {
        'title': 'Post 1',
        'author': 'Vyankatesh Manwade',
        'postedOn': '20 Mar 2020',
        'content': 'This is post 1'
    },
    {
        'title': 'Post 2',
        'author': 'Parth Naik',
        'postedOn': '21 Mar 2020',
        'content': 'This is post 2'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(
            f'Account created successfully for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin@123':
            flash(
                f'You have been logged in successfully as {form.email.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash(
                'Login Unsuccessful! Please Check email and password and try again', 'danger')
    return render_template('login.html', title='Login', form=form)
