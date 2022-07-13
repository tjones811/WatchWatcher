from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.show_model import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    new_user_id = User.create_user(data)

    session['user_id'] = new_user_id


        
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():

    if not User.validate_login(request.form):
        return redirect('/')

    data = {
        'email': request.form['email']
    }

    logged_in_user = User.get_by_email(data)

    session['user_id'] = logged_in_user.id

    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login or register')
        return redirect('/')
    #user_id = session['user_id']
    #return render_template('dashboard.html',logged_user_id = user_id)

    data= {
        'user_id' : session['user_id']
    }
    user = User.get_by_id(data)

    shows = Show.get_all()

    return render_template('dashboard.html',user = user,shows = shows)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
