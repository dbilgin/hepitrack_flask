import json

def test_user_data(client, auth, app):
    register_result = json.loads(auth.register().data)

    with app.app_context():
        change_response = client.get(
            '/user/data',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + register_result['access_token']
            }
        )
        assert change_response.status_code == 200
        assert b'email' in change_response.data
        assert b'verified' in change_response.data
        assert b'color' in change_response.data