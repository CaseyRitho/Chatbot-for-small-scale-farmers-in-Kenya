from flask import Flask,render_template,url_for,redirect,jsonify,request
from wtforms import StringField, SubmitField, PasswordField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,ValidationError,EqualTo
from flask import flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SECRET_KEY']  = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/farmers'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    return SmallFarmers.query.get(int(user_id))


class SmallFarmers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    

    # Create String

    def __repr__(self):
        return '<Name %r>' % self.username

   
data = []

class Chatbot(FlaskForm):
    message = StringField(render_kw = {"placeholder":"Type a message", "id":"user-message"})
    send = SubmitField('Send', render_kw={"class":"button", "id":"button"})

class Signup(FlaskForm):
    firstname = StringField(render_kw={"placeholder":"Enter firstname"}, validators=[InputRequired()])
    lastname = StringField(render_kw={"placeholder":"Enter lastname"}, validators=[InputRequired()])
    username = StringField(render_kw={"placeholder":"Enter username"}, validators=[InputRequired()])
    email = EmailField(render_kw={"placeholder":"Enter email-address"}, validators=[InputRequired()])
    password = PasswordField(render_kw={"placeholder":"Enter password"}, validators=[InputRequired()])
    # confirm_password = PasswordField(render_kw={"placeholder":"Confirm Password"}, validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):

        farmer = SmallFarmers.query.filter_by(username=username.data).first()
        if farmer:
            raise ValidationError('The username already exists. Please choose another username')

    def validate_email(self,email):

        farmer = SmallFarmers.query.filter_by(email=email.data).first()
        if farmer:
            raise ValidationError('The email is already registered')



class Login(FlaskForm):
    username = StringField(render_kw={"placeholder":"Enter username"}, validators=[InputRequired()])
    password = PasswordField(render_kw={"placeholder":"Enter password"}, validators=[InputRequired()])
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = EmailField(render_kw={"placeholder":"Enter email-address"}, validators=[InputRequired()])
    submit = SubmitField('Request Reset')

    def validate_email(self,email):

        farmer = SmallFarmers.query.filter_by(email=email.data).first()
        if farmer is None:
            raise ValidationError('This account does not exist please register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(render_kw={"placeholder":"Enter password"}, validators=[InputRequired()])
    confirm_password = PasswordField(render_kw={"placeholder":"Confirm Password"}, validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    form = Chatbot()
    
    return render_template('chatbot.html', form=form)
         
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form  = Login()

    if form.validate_on_submit():
        user = SmallFarmers.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login was Unsuccesful please check your username or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = Signup()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = SmallFarmers(
            username=form.username.data,
            email = form.email.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created for {form.username.data}')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


if  __name__ == '__main__':
    app.run(debug=True, port=8081)