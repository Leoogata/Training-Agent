from flask import Blueprint, request, jsonify
from app import db
from app.models import WorkoutLog, Workout

workoutslogs_bp = Blueprint('workoutslogs_bp', __name__)

@workoutslogs_bp.route('/workoutslogs', methods=['GET'])
def get_all_workout_logs():
    workout_logs = WorkoutLog.query.all()

    output = []
    for log in workout_logs:
        log_data = {
            'id': log.id,
            'date': log.date,
            'workout_id': log.workout_id
        }
        output.append(log_data)

    return jsonify(output)

@workoutslogs_bp.route('/workoutslogs/<int:id>', methods=['GET'])
def get_workout_log(id):
    workout_log = WorkoutLog.query.get_or_404(id)

    return jsonify({
        'id': workout_log.id,
        'date': workout_log.date,
        'workout_id': workout_log.workout_id
    })

@workoutslogs_bp.route('/workoutslogs', methods=['POST'])
def add_workout_log():
    data = request.get_json()

    # Verify workout exists
    workout = Workout.query.get_or_404(data['workout_id'])

    new_log = WorkoutLog(
        workout_id=data['workout_id']
    )

    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Log de treino criado com sucesso', 'id': new_log.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@workoutslogs_bp.route('/workoutslogs/<int:id>', methods=['DELETE'])
def delete_workout_log(id):
    workout_log = WorkoutLog.query.get_or_404(id)

    try:
        db.session.delete(workout_log)
        db.session.commit()
        return jsonify({'message': 'Log de treino foi excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
