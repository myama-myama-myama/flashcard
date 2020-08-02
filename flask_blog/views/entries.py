from flask import request,redirect, url_for, render_template, flash, session
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
# for class User
from flask_blog.models.entries import *
# for USERNAME
from flask_blog import app
# for request
from flask import request

@app.route('/')
@login_required
def show_entries():
    username = app.config['USERNAME']
    user = db.session.query(User).filter(User.name == username).one()
    items = db.session.query(Answer).filter(Answer.user_id == user.id).all()
    app.config['USER_ID']=user.id
    #
    entries = Entry.query.order_by(Entry.id.desc()).all()
    app.config['QUESTION_NUMBER'] = len(entries)
    #print(entries)
    #
    # count the number of correction
    #
    num_correct=0
    entries = []
    for item in items:
        if item.correct == 1:
            num_correct+=1
        entries.append([item.q_id, item.correct])
    #
    # [q_id, correct] ... [[1,1][2,1]]
    #
    correct_ratio = [num_correct,app.config['QUESTION_NUMBER']]
    #print(correct_ratio)
    #
    return render_template('entries/index.html',
                           username=username,
                           correct_ratio=correct_ratio)


@app.route('/user/new', methods =['GET']) 
def new_user(): 
    return render_template('entries/new_user.html')
@app.route('/user', methods =['POST'])
def add_user(): 
    user = User(
        name = request.form['user'],
        passwd = request.form['pass']
        )
    db.session.add(user)
    db.session.commit()
    flash(request.form['user'])
    flash('新規ユーザが追加されました') 
    return redirect( url_for('show_entries'))


@app.route('/user_delete', methods =['GET'])
@login_required
def delete_user():
    username = app.config['USERNAME']
    user = db.session.query(User).filter(User.name == username).one()
    db.session.delete(user)
    db.session.commit()
    flash(username) 
    flash('ユーザが削除されました')
    session.pop('logged_in',None)
    flash('ログアウトしました')
    return redirect( url_for('show_entries'))

@app.route('/entries/<int:id>', methods =['GET'])
@login_required
def start_asking(id):
    entry = Entry.query.get(id)
    return render_template( 'entries/show.html',id=id,entry=entry)

@app.route('/entries/<int:id>/answer', methods =['POST'])
@login_required
def show_answer(id): 
    entry = Entry.query.get(id)
    if request.form['action'] == 'answer':
        return render_template('entries/show_answer.html', id=id, entry = entry)
    else:
        # abort
        return redirect(url_for('show_result'))

@app.route('/entries/<int:id>/next_question', methods =['POST'])
@login_required
def next_question(id):
    # register result of answer
    user_id = app.config['USER_ID']
    q_id=id
    print("*********")
    print("user_id={} q_id={}".format(user_id,q_id))
    answer = Answer.query.filter_by(user_id = user_id,q_id = q_id).first()
    print("answer.query")
    print(answer)
    #
    if request.form['action'] == 'correct':
        correct =1
    else:
        correct =0
    #
    if answer == None:
        answer = Answer(
            correct = correct,
            user_id =user_id,
            q_id=q_id
        )
        db.session.add(answer)
        db.session.commit()
        print("*********create")
        print(answer)
    else:
        answer.correct = correct
        db.session.merge(answer)
        db.session.commit()
        print("*********update")
        print(answer)        
        
    id+=1
    #
    question_num = app.config['QUESTION_NUMBER']
    #
    if id == question_num+1:
        print("***next_question***")
        print(request.form['action'])        
        return redirect(url_for('show_result'))
    print("***next_question***")
    print(request.form['action'])
    return redirect( url_for('start_asking',id=id))


@app.route('/entries/result', methods =['GET']) 
@login_required
def show_result():
    username = app.config['USERNAME']
    user = db.session.query(User).filter(User.name == username).one()
    question_num = app.config['QUESTION_NUMBER']    
    #
    answers = Answer.query.filter_by(user_id = user.id).all()
    correct_num =0
    wrong_num=0
    for answer in answers:
        if answer.correct == 1:
            correct_num +=1
        else:
            wrong_num +=1
    #
    # [correct, wrong, total]
    #correct_num =  10
    #wrong_num = 3
    result = [correct_num,wrong_num, question_num]
    return render_template( 'entries/result.html',
                            username=username,
                            result=result)


