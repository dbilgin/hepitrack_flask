def get_news(db):
    return db.execute("SELECT * FROM news WHERE publish_date > date('now', '-1 days') LIMIT 10").fetchall()
