from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '52e45de5548bd1f09fba589e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inner-air.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=3, max=30)],
                             render_kw={"placeholder": "First Name"})
    email = StringField(validators=[Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign up")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError(f'e-mail already exist.')


# Login form
class LoginForm(FlaskForm):
    email = StringField(validators=[Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data, 10)

        new_user = User(
            first_name=form.first_name.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect('login')

    return render_template('register.html', form=form)


# dash board
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    print(current_user.first_name)
    return render_template('dashboard.html', name=current_user.first_name)


# log out
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Checks if the main.py file has executed directly and not imported.
if __name__ == "__main__":
    app.run(debug=True)
