from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.workout_routes import workout_bp
    from app.routes.exercise_routes import exercise_bp
    from app.routes.workoutslogs_routes import workoutslogs_bp
    from app.routes.exerciseslogs_routes import exerciseslogs_bp

    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(workoutslogs_bp)
    app.register_blueprint(exerciseslogs_bp)

    with app.app_context():
        db.create_all() 

    return app