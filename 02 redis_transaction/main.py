from random import randrange
from typing import Optional

from fastapi import FastAPI
from handle_data import PRODUCT_NUMBER_KEY, handle_buy_product
from redis_client import redis_client

app = FastAPI()


@app.get('/')
def read_root():
    return {'Welcome to learn Redis'}


@app.get('/product_number')
def get_product_number():
    """
    查询商品库存
    """
    return redis_client.get(PRODUCT_NUMBER_KEY)


@app.post('/buy')
def buy_product():
    """
    抢购商品
    """
    # 随机一个用户
    user = randrange(10000)
    # 抢购商品
    return handle_buy_product(user)


@app.post('/clear_data')
def clear_data():
    """
    清空数据
    """
    for key in redis_client.scan_iter('*'):
        redis_client.delete(key)
    return True


@app.post('/init_data')
def init_data(number: Optional[int] = 10):
    """
    初始化商品数目
    """
    redis_client.set(PRODUCT_NUMBER_KEY, number)
    return True
