def generate_roadmap (quiz_score, time_taken) :
    GNW_AVG_TIME = 90
    score_feedback = ""

    if time_taken > GNW_AVG_TIME * 1.2:
        roadmap_message = f"नमस्ते{score_feedback}"
        return roadmap_message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ARchieve.db'
app.config ['SQALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    was_correct = db.Column(db.Boolean, nullable = False)
    time_taken_seconds = db.Column(db.Float, nullable = False)
    date_taken = db.Column(db.DateTime, nullable = False)

class User(db.Model):
    id = db.Column (db. Integer, primary_key=True)
    username = db.Column (db. String (80), unique=True, nullable=False)
    email = db.Column (db.String(120), unique=True, nullable=False)
    city = db.Column (db. String(50)) 
    is_premium = db.Column (db. Boolean, default=False)

class Question(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    text = db.Column (db.String (500), nullable=False)
    topic = db.Column (db.String (50), nullable=False)
    topic_id = db.column(db.Integer,db.ForeignKey('topic.id'), nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db. Column(db.String(50), unique=True, nullable=False)
    subject = db.Column(db.String(50)) 

class UserTopicProgress(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    total_attempts = db.Column (db.Integer, default=0)
    correct_attempts = db.Column (db.Integer, default=0)
    avg_time = db.Column(db.Float, default=0)

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    time_taken = db.Column(db.Float)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.Integer, db.ForeignKey('quiz_session.id'))

class Roadmap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weak_topics = db.Column(db.String(300))
    suggested_plan = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

with app.app_context():
    db.create_all()
    print("Database Tables Created!")

def add_first_test_data():
    with app.app_context():
        test_user = User.query.filter_by("Aradhya_Test").first()
        if not test_user:
            test_user = User(username='Aradhya_Test', email='test@ARchieve.com',city="Greater Noida West")
            db.session.add(test_user)
            db.session.commit()
            print("Test User Created!")
        test_q = Question.query.filter_by("Polynomials").first()
        if not test_q:
            test_q = Question(text='What is x^2 - 4?', topic='Polynomials')
            db.session.add(test_q)
            db.session.commit()
            print("Test Questions Created!")
        new_result = QuizResult(
            user_id = test_user.id,
            question_id = test_q.id,
            was_correct = True,
            time_taken_seconds = 15.5,
            date_taken = datetime.utcnow()
        )
        db.session.add(new_result)
        db.session.commit()
        print("First Quiz Result Saved!")

if __name__ == '__main__':
    app.run(debug = True)