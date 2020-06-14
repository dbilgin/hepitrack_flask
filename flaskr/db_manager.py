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
        'UPDATE user SET password=? WHERE verification_token=?',
        (password, token)
    )
    db.commit()

    return db_result