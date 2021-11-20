from random import randrange
from typing import Optional

from fastapi import FastAPI, Query
from handle_data import get_articles, post_article, vote_article
from redis_client import redis_client

app = FastAPI()


@app.get('/')
def read_root():
    return {'Welcome to learn Redis'}


@app.get('/article')
def get_article(order: Optional[str] = Query('score', enum=['score', 'time'])):
    return get_articles(order)


@app.post('/random_post_article')
def random_post_article(number: Optional[int] = 10):
    """
    使用随机用户发表文章
    """

    for _ in range(number):
        user = randrange(number)
        post_article(user)
    return True


@app.post('/random_vote')
def random_vote(number: Optional[int] = 10):
    """
    使用随机用户对随机文章点赞
    """

    article_id_max = int(redis_client.get('article:'))

    for _ in range(number):
        user = randrange(number)
        article = f'article:{randrange(1, article_id_max+1)}'
        vote_article(user, article)
    return True


@app.post('/clear_data')
def clear_data():
    """
    清空数据
    """
    for key in redis_client.scan_iter('*'):
        redis_client.delete(key)
