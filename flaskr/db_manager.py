def get_news(db):
    return db.execute("SELECT * FROM news WHERE publish_date > date('now', '-1 days') LIMIT 10").fetchall()

def mapped_news(db):
    news_list = get_news(db)
    mapped_list = []
    for article in news_list:
        mapped_list.append(
                {
                    "source": article['source'],
                    "author": article['author'],
                    "title": article['title'],
                    "description": article['description'],
                    "url": article['url'],
                    "image": article['image'],
                    "publish_date": article['publish_date']
                    }
                )
    return mapped_list
