import requests

import json

from flask import Blueprint, g, current_app, jsonify

from flaskr.auth import login_required

from flaskr.db import get_db

from flaskr.db_manager import mapped_news

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/list', methods=['GET'])
@login_required
def list():
    db = get_db()
    todays_news = mapped_news(db)

    try:
        if not todays_news:
            print('fetching news')
            fetched_news = requests.get(
                    'http://newsapi.org/v2/top-headlines?category=health&country=gb&pageSize=10&apiKey=' +
                    current_app.config['NEWS_API_KEY']
                    ).json()
                    
        
            if not fetched_news:
                todays_news = []
            else:
                for article in fetched_news['articles']:
                    if article['title'] is not None and article['url'] is not None and article['publishedAt'] is not None:
                        db.execute(
                                'INSERT INTO news (source, author, title, description, url, image, publish_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                (article['source']['name'], article['author'], article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt'])
                                )
                        db.commit()
                    
                todays_news = mapped_news(db)

    except:
        todays_news = []

    return jsonify(todays_news)
