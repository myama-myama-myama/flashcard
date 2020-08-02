from flask_script import Command 
from flask_blog import db 
#
from flask_blog.models.entries import *
#
from flask_blog.scripts import db_data

class InitDB(Command): 
    "create database" 

    def run(self): 
        db.create_all()
        #
        '''
        items =[
            Entry(question='Q1',answer='A1'),
            Entry(question='Q2',answer='A2')            
        ]
        db.session.add_all(items)
        db.session.commit()
        '''
        for item in db_data.question_list:
            item = Entry(question=item[1],answer=item[2])
            db.session.add(item)
            db.session.commit()

        items = db.session.query(Entry).all()
        print("===Entry===================")
        for item in items:
            print(item.question)
            print(item.answer)
        print("===Entry===================")

        #
        item = User(name='john',passwd='due123')
        db.session.add(item)
        db.session.commit()
        
        #
        items = db.session.query(User).all()

        print("===User===================")
        for item in items:
            print(item.id)
            print(item.name)
            
            item2 = Answer(correct=1, user_id = item.id, q_id=1)
            db.session.add(item2)

            item2 = Answer(correct=1, user_id = item.id, q_id=2)
            db.session.add(item2)

            db.session.commit()
            
        print("===User===================")
        
        #
        uid= item.id
        items = db.session.query(Answer).filter(Answer.user_id == uid).all()
        #items = db.session.query(Answer).all()
        
        print("===Answer===================")
        for item in items:
            print(item.q_id)
            print(item.correct)
        print("===Answer===================")
            
        

        
