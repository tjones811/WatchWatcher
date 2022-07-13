from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.show_model import Show


@app.route('/show/new')
def new():

    data= {
        'user_id' : session['user_id']
    }
    user = User.get_by_id(data)

    return render_template('new_show.html',user = user)

@app.route('/show/create', methods=['POST'])
def create():
    if not Show.validate_show(request.form):
        return redirect('/show/new')

    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'release_date' : request.form['release_date'],
        'description' : request.form['description'],
        'user_id' : int(request.form['user_id']),
    }

    new_show = Show.add_new(data)


    return redirect('/dashboard')


@app.route('/show/show/<int:id>')
def show_show(id):
    
    data = {
        'id': id}

    show = Show.get_one(data)

    return render_template('one_show.html',show = show)

@app.route('/show/edit/<int:id>')
def edit_show(id):

    data = {
        'id':id
        }

    show = Show.get_one(data)

    return render_template('one_edit.html',show = show)

@app.route('/show/update', methods=['POST'])
def show_update():
    x = request.form['show_id']
    if not Show.validate_show(request.form):
        return redirect(f'/show/edit/{x}')
    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'release_date' : request.form['release_date'],
        'description' : request.form['description'],
        'show_id' : int(request.form['show_id']),
    }

    show = Show.update(data)

    return redirect('/dashboard')

@app.route('/show/delete/<int:id>')
def delete(id):
    data = {'id': id}

    delete = Show.delete(data)

    return redirect('/dashboard')
