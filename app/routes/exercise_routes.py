from flask import Blueprint, request, jsonify
from app.models import Workout, Exercise
from app import db


exercise_bp = Blueprint('exercise_bp', __name__)

@exercise_bp.route('/exercise', methods=['GET'])
def get_all_exercise():
    exercises = Exercise.query.all()

    output = []
    for exercise in exercises:
        exercise_data = {
            'name': exercise.name,
            'sets': exercise.sets, 
            'reps': exercise.reps, 
            'technique': exercise.technique 
        }
        output.append(exercise_data)

    return jsonify({output})
    
@exercise_bp.route('/exercise/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    return jsonify(exercise)


@exercise_bp.route('/register', methods=['POST'])
def add_exercise():
    data = request.get_json()

    new_exercise = Exercise( 
        name = data['name'], 
        sets = data['sets'],
        reps = data['reps'],
        technique = data['technique'],
        workout_id = data['workout_id']
    )

    try:
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify({'message': 'O exercício {new_exercise.name} foi adicionado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    
@exercise_bp.route('/remove/<int:id>', methods=['DELETE'])
def remover_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    try:
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({'message': 'Exercicio {exercise.name} foi deletado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400