from flask import Blueprint, request, jsonify
from app import db
from app.models import Workout


workout_bp = Blueprint('workout_bp', __name__)

@workout_bp.route('/workouts', methods=['GET'])
def get_all_workouts():
    workouts = Workout.query.all()

    output = []
    for workout in workouts:
        workout_data = {
            'id': workout.id,
            'name': workout.name
        }
        output.append(workout_data)

    return jsonify(output)

@workout_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)

    return jsonify({"id": workout.id, "name": workout.name})

@workout_bp.route('/workouts/<int:workout_id>/exercise', methods=['GET'])
def get_workout_exercises(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    lista_exercicios = []
    for ex in workout.exercises:
        lista_exercicios.append({
            "id": ex.id,
            "name": ex.name,
            "sets": ex.sets,
            "reps": ex.reps,
            "technique": ex.technique
        })
        
    return jsonify({
        "workout_name": workout.name,
        "exercises": lista_exercicios
    }), 200
 
@workout_bp.route('/register', methods=['POST'])
def add_workout():
    data = request.get_json()

    new_workout = Workout(
        name = data['name']
    )

    try:
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({'message': 'Treino criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@workout_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    try:
        db.session.delete(workout)
        db.session.commit()
        return jsonify ({f'message': 'Treino {workout.name} foi excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400