import requests

import json
from flask import Blueprint, g, current_app, jsonify
from flaskr.auth import login_required
from flaskr.db_manager import get_news, insert_news_article

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/list', methods=['GET'])
@login_required
def list():
    todays_news = get_news()

    try:
        if not todays_news:
            print('fetching news')
            fetched_news = requests.get(
                "http://newsapi.org/v2/top-headlines"
                + "?category=health&country=gb&pageSize=10&apiKey="
                + current_app.config['NEWS_API_KEY']
            ).json()

            if not fetched_news:
                todays_news = []
            else:
                for article in fetched_news['articles']:
                    if (
                            article['title'] is not None
                            and article['url'] is not None
                            and article['publishedAt'] is not None
                        ):
                        insert_news_article(article)
                todays_news = get_news()

    except:
        todays_news = []

    return jsonify(todays_news)
