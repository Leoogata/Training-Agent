from app import db
from datetime import datetime

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    exercises = db.relationship('Exercise', backref='workout', lazy = True)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable = False)
    reps = db.Column(db.Integer, nullable = False)
    technique= db.Column(db.String(100), nullable = True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    
    exercise_logs = db.relationship('ExerciseLog', backref='workout_log', lazy=True)

class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'
    id = db.Column(db.Integer, primary_key=True)
    workout_log_id = db.Column(db.Integer, db.ForeignKey('workout_logs.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    weight = db.Column(db.Float) 
    reps_done = db.Column(db.Integer) 
    notes = db.Column(db.String(255)) 
    
    