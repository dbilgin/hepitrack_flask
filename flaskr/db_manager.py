from flaskr.db import get_db
from flask import g

# News
def get_news():
    return get_db().execute(
        "SELECT * FROM news "
        + "WHERE publish_date > date('now', '-1 days') LIMIT 10"
    ).fetchall()

def insert_news_article(article):
    db=get_db()
    db.execute(
        'INSERT INTO news '
        + '(source, author, title, description, url, image, publish_date) '
        + 'VALUES (?, ?, ?, ?, ?, ?, ?)',
        (
            article['source']['name'],
            article['author'],
            article['title'],
            article['description'],
            article['url'],
            article['urlToImage'],
            article['publishedAt']
        )
    )
    db.commit()

# User
def get_user_by_email(email):
    db=get_db()
    return db.execute(
        'SELECT * FROM user WHERE email=?',
        (email,)
    ).fetchone()

def get_user_by_token(access_token):
    db=get_db()
    return db.execute(
        'SELECT * FROM user WHERE access_token=?',
        (access_token,)
    ).fetchone()

def insert_user(email, password_hash, token, verification_token):
    db=get_db()
    db.execute(
        'INSERT INTO user (email, password, access_token, verification_token)'
        + 'VALUES (?, ?, ?, ?)',
        (email, password_hash, token, verification_token)
    )
    db.commit()

def update_user_token(token, id):
    db=get_db()
    db.execute(
        'UPDATE user SET access_token=? WHERE id=?',
        (token, id)
    )
    db.commit()

def update_verification_token(verification_token):
    db=get_db()
    result=db.execute(
        'UPDATE user SET verification_token=? WHERE id=? AND verified=0',
        (verification_token, g.user['id'])
    )
    db.commit()

    return result

def update_verification_token_by_email(verification_token, email):
    db=get_db()
    result=db.execute(
        'UPDATE user SET verification_token=? WHERE email=?',
        (verification_token, email)
    )
    db.commit()

    return result

def check_user_count_by_email(email):
    db=get_db()
    result=db.execute(
        'SELECT COUNT(*) as count FROM user WHERE email=?',
        (email,)
    ).fetchone()['count']

    return result

def update_user_token_and_pass(token, password):
    db=get_db()
    db.execute(
        'UPDATE user SET access_token=?, password=? WHERE id=?',
        (token, password, g.user['id'])
    )
    db.commit()

def update_email(new_email, token, verification_token):
    db=get_db()
    db.execute(
        '''UPDATE user SET
        email=?,
        access_token=?,
        verification_token=?,
        verified=0
        WHERE id=?''',

        (new_email, token, verification_token, g.user['id'])
    )
    db.commit()

def verify_user(verification_token):
    db=get_db()
    update_result=db.execute(
      'UPDATE user set verified=1 '
      + 'WHERE verification_token=?',
      (verification_token,)
    )
    db.commit()

    if update_result.rowcount > 0:
      update_result=db.execute(
        'UPDATE user set verification_token=NULL '
        + 'WHERE verification_token=?',
        (verification_token,)
      )
      db.commit()

      return update_result.rowcount
    else:
      return 0

def user_data(user_id):
    db=get_db()
    return db.execute(
        'SELECT email, color, verified FROM user WHERE id=?',
        (user_id,)
    ).fetchone()

def update_color(color):
    db=get_db()
    db.execute(
        '''UPDATE user SET
        color=?
        WHERE id=?''',

        (color, g.user['id'])
    )
    db.commit()

def delete_user():
    db=get_db()
    db.execute(
        '''UPDATE user set email='deleted', verification_token=NULL
        WHERE id=?''',

        (g.user['id'],)
    )
    db.commit()

def log_out_user():
    db=get_db()
    db.execute(
        '''UPDATE user set verification_token=NULL
        WHERE id=?''',

        (g.user['id'],)
    )
    db.commit()

def update_user_pass_by_verify_token(password, token):
    db=get_db()
    db_result=db.execute(
        'UPDATE user SET password=?, verification_token=NULL WHERE verification_token=?',
        (password, token)
    )
    db.commit()

    return db_result

def get_email_from_verification(token):
    db=get_db()
    email=db.execute(
        'SELECT email FROM user WHERE verification_token=?',
        (token,)
    ).fetchone()

    return email

def get_all_tracks():
    db=get_db()
    tracks=db.execute(
        'SELECT id, water_count, date FROM track WHERE user_id=?',
        (g.user['id'],)
    ).fetchall()

    return tracks

def get_all_food_tracks(track_id):
    db=get_db()
    food_tracks=db.execute(
        'SELECT id, name, description FROM food_track WHERE track_id=?',
        (track_id,)
    ).fetchall()

    return food_tracks

def get_all_symptom_tracks(track_id):
    db=get_db()
    symptom_tracks=db.execute(
        'SELECT id, symptom, body_parts, intensity FROM symptom_track WHERE track_id=?',
        (track_id,)
    ).fetchall()

    return symptom_tracks

def insert_symptoms(symptoms, track_id):
    db=get_db()
    for symptom in symptoms:
        db.execute(
            'INSERT INTO symptom_track'
            + ' (track_id, symptom, body_parts, intensity)'
            + 'VALUES (?, ?, ?, ?)',
            (
                track_id,
                symptom['symptom'],
                symptom['body_parts'],
                symptom['intensity']
            )
        )
        db.commit()

def insert_food(food_tracks, track_id):
    db=get_db()
    for food in food_tracks:
        db.execute(
            'INSERT INTO food_track'
            + ' (track_id, name, description)'
            + 'VALUES (?, ?, ?)',
            (
                track_id,
                food['name'],
                food['description']
            )
        )
        db.commit()


def insert_track(water_count, symptoms, food_tracks, date_time):
    db=get_db()
    track=db.execute(
        'INSERT INTO track (user_id, water_count, date)'
        + 'VALUES (?, ?, ?)',
        (g.user['id'], water_count, date_time)
    )
    db.commit()
    track_id = track.lastrowid

    insert_symptoms(symptoms, track_id)
    insert_food(food_tracks, track_id)