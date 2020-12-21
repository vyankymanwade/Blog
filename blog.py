from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7e87257cf101da56aba72037aa3efa4e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    profileImage = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.profileImage}')"

 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    postedOn = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

    def __repr__(self):
        return f"Post('{self.id}','{self.title}','{self.postedOn}')"


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


if __name__ == "__main__":
    app.run(debug=True)
