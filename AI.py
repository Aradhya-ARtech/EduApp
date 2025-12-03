def generate_roadmap (quiz_score, time_taken) :
    GNW_AVG_TIME = 90
    score_feedback = ""

    if time_taken > GNW_AVG_TIME * 1.2:
        roadmap_message = f"नमस्ते{score_feedback}"
        return roadmap_message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///ARchieve.db'
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
    id = db. Column (db. Integer, primary_key=True)
    username = db. Column (db. String (80), unique=True, nullable=False)
    email = db. Column (db.String(120), unique=True, nullable=False)
    city = db. Column (db. String(50)) 
    is_premium = db. Column (db. Boolean, default=False)

class Question(db.Model):
    id = db. Column (db. Integer, primary_key=True)
    text = db. Column (db. String (500), nullable=False)
    topic = db. Column (db. String (50), nullable=False)

with app.app_context():
    db.create_all()
    print("Database Tables Created!")

if __name__ == '__main__':
    app.run(debug = True)