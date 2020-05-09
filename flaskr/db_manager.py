from flaskr.db import get_db

# News
def get_news():
    return get_db().execute(
        "SELECT * FROM news "
        + "WHERE publish_date > date('now', '-1 days') LIMIT 10"
    ).fetchall()

def insert_news_article(article):
    db = get_db()
    db.execute(
        "INSERT INTO news "
        + "(source, author, title, description, url, image, publish_date) "
        + "VALUES (?, ?, ?, ?, ?, ?, ?)",
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
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE email = ?',
        (email,)
    ).fetchone()

def get_user_by_token(access_token):
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE access_token = ?',
        (access_token,)
    ).fetchone()

def insert_user(email, password_hash, token):
    db = get_db()
    db.execute(
        'INSERT INTO user (email, password, access_token) VALUES (?, ?, ?)',
        (email, password_hash, token)
    )
    db.commit()

def update_user_token(token, id):
    db = get_db()
    db.execute(
        'UPDATE user Set access_token = ? WHERE id = ?',
        (token, id)
    )
    db.commit()
