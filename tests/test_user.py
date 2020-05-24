import pytest
import json

def test_user_data(client, auth, app):
    register_result=json.loads(auth.register().data)

    with app.app_context():
        change_response=client.get(
            '/user/data',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert change_response.status_code==200
        assert b'email' in change_response.data
        assert b'verified' in change_response.data
        assert b'color' in change_response.data

@pytest.mark.parametrize(('color', 'code'), (
    ('#FFFFFF', 204),
    ('#FFFFF', 400),
    (None, 400),
    ('#FFF', 204),
))
def test_color_patch(client, auth, app, color, code):
    register_result=json.loads(auth.register().data)

    with app.app_context():
        color_response=client.patch(
            '/user/color',
            data=json.dumps(
                dict(color=color)
            ),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert color_response.status_code==code