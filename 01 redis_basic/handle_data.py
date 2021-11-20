import time

from redis_client import redis_client


def post_article(user):
    """
    发表一篇文章
    """
    # 利用redis的计数器生成文章id
    article_id = str(redis_client.incr('article:'))
    # 文章title
    article_title = f'article_title_{article_id}'

    # 文章发布时间
    now = time.time()

    # 将作者加入到点赞这篇文章的用户列表中
    voted = f'voted:{article_id}'
    redis_client.sadd(voted, user)

    # 将文章信息存放到一个散列中
    article = f'article:{article_id}'
    redis_client.hmset(
        article,
        {
            'title': article_title,
            'poster': user,
            'time': now,
            'votes': 1,
        },
    )
    # 将文章发布到根据点赞数量排序的有序集合中
    redis_client.zadd('score:', {article: 1})
    # 将文章发布到根据发布时间排序的有序集合中
    redis_client.zadd('time:', {article: now})
    return article_id


def vote_article(user, article):
    """
    为文章点赞
    """
    article_id = article.split(':')[-1]
    if redis_client.sadd('voted:' + article_id, user):
        redis_client.zincrby('score:', 1, article)
        redis_client.hincrby(article, 'votes', 1)


def get_articles(order='score'):
    """
    获取 10 篇文章
    """
    ids = redis_client.zrevrange(order + ':', 0, 10)
    articles = []
    for id in ids:
        article_data = redis_client.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)
    return articles
