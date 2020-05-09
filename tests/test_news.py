import pytest
from flaskr.db import get_db


def test_list(client, app):
    response = client.get('/news/list')
    assert 401 == response.status_code

    response = client.get(
            '/news/list',
            headers={'Authorization': 'token ' + app.config['API_KEY']}
    )
    assert 200 == response.status_code
    assert b'author' in response.data
