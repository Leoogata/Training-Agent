from flask import Blueprint, request, jsonify
from app import db
from app.models import ExerciseLog, WorkoutLog, Exercise

exerciseslogs_bp = Blueprint('exerciseslogs_bp', __name__)

@exerciseslogs_bp.route('/exerciseslogs', methods=['GET'])
def get_all_exercise_logs():
    exercise_logs = ExerciseLog.query.all()

    output = []
    for log in exercise_logs:
        log_data = {
            'id': log.id,
            'workout_log_id': log.workout_log_id,
            'exercise_id': log.exercise_id,
            'weight': log.weight,
            'reps_done': log.reps_done,
            'notes': log.notes
        }
        output.append(log_data)

    return jsonify(output)

@exerciseslogs_bp.route('/exerciseslogs/<int:id>', methods=['GET'])
def get_exercise_log(id):
    exercise_log = ExerciseLog.query.get_or_404(id)

    return jsonify({
        'id': exercise_log.id,
        'workout_log_id': exercise_log.workout_log_id,
        'exercise_id': exercise_log.exercise_id,
        'weight': exercise_log.weight,
        'reps_done': exercise_log.reps_done,
        'notes': exercise_log.notes
    })

@exerciseslogs_bp.route('/exerciseslogs', methods=['POST'])
def add_exercise_log():
    data = request.get_json()

    # Verify workout_log and exercise exist
    WorkoutLog.query.get_or_404(data['workout_log_id'])
    Exercise.query.get_or_404(data['exercise_id'])

    new_log = ExerciseLog(
        workout_log_id=data['workout_log_id'],
        exercise_id=data['exercise_id'],
        weight=data.get('weight'),
        reps_done=data.get('reps_done'),
        notes=data.get('notes')
    )

    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Log de exercício criado com sucesso', 'id': new_log.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@exerciseslogs_bp.route('/exerciseslogs/<int:id>', methods=['DELETE'])
def delete_exercise_log(id):
    exercise_log = ExerciseLog.query.get_or_404(id)

    try:
        db.session.delete(exercise_log)
        db.session.commit()
        return jsonify({'message': 'Log de exercício foi excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
