import pytest
import json

@pytest.mark.parametrize((
    'water_count',
    'symptoms',
    'food_tracks',
    'date_time',
    'code'
), (
    (1, [], [], '2020-09-27T14:33:57.138814', 204),
    (
        1,
        [{'symptom': 3,'body_parts': '4,5', 'intensity':4}],
        [{'name': 'test', 'description': 'test'}],
        '2020-09-27T14:33:57.138814',
        204
    ),
    (
        1,
        "[{'symptom': 3,'body_parts': '4,5', 'intensity':4}]",
        "[{'name': 'test', 'description': 'test'}]",
        '2020-09-27T14:33:57.138814',
        400
    ),
))
def test_save_track(
    client,
    auth,
    app,
    water_count,
    symptoms,
    food_tracks,
    date_time,
    code
):
    register_result=json.loads(auth.register().data)

    with app.app_context():
        track_response=client.post(
            '/track/save',
            data=json.dumps(
                dict(
                    water_count=water_count,
                    symptoms=symptoms,
                    food_tracks=food_tracks,
                    date_time=date_time
                )
            ),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert track_response.status_code==code

def test_get_tracks(
    client,
    auth,
    app
):
    register_result=json.loads(auth.register().data)

    with app.app_context():
        track_response=client.get(
            '/track/all',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )

        assert track_response.status_code==200