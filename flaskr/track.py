from flask import Blueprint, g, request, abort, jsonify

from flaskr.auth import login_required
from flaskr.db_manager import (
    insert_track, get_all_tracks, get_all_food_tracks, get_all_symptom_tracks
)

import json

bp=Blueprint('track', __name__, url_prefix='/track')

@bp.route('/save', methods=['POST'])
@login_required
def save():
    content=request.get_json()
    if not content:
        abort(400)
    try:
        symptoms=content['symptoms']
        food_tracks=content['food_tracks']
        water_count=content['water_count']
        date_time=content['date_time']

        insert_track(water_count, symptoms, food_tracks, date_time)
    except:
        abort(400)

    return ('', 204)

@bp.route('/all', methods=['GET'])
@login_required
def all():
    try:
        tracks=get_all_tracks()

        data=[
            {
                'id':track['id'],
                'water_count':track['water_count'],
                'date':track['date'],
                'food_tracks':get_all_food_tracks(track['id']),
                'symptom_tracks':get_all_symptom_tracks(track['id'])
            }
            for track in tracks
        ]
    except:
        abort(400)

    return jsonify(data)
