from redis.exceptions import LockError, WatchError
from redis_client import redis_client

PRODUCT_NUMBER_KEY = 'product:'
SUCCESS_USER_KEY = 'user:'


def handle_buy_product_1(user):
    """
    抢购商品
    """
    product_number = redis_client.get(PRODUCT_NUMBER_KEY)
    # 未设置商品数目时，秒杀尚未开始
    if product_number is None:
        print('秒杀尚未开始')
        return False
    # 如果用户已经秒杀成功了
    if redis_client.sismember(SUCCESS_USER_KEY, user):
        print('你已秒杀成功，不能重复购买')
        return False
    # 如果库存不足，秒杀失败
    if int(product_number) <= 0:
        print('没有库存了')
        return False
    # 商品数量减1
    redis_client.decr(PRODUCT_NUMBER_KEY)
    # 记录秒杀成功的用户
    redis_client.sadd(SUCCESS_USER_KEY, user)
    return True


def handle_buy_product_2(user):
    """
    抢购商品
    """
    pipe = redis_client.pipeline()
    try:
        # 增加监视
        pipe.watch(PRODUCT_NUMBER_KEY)
        # 获取库存
        product_number = pipe.get(PRODUCT_NUMBER_KEY)
        # 未设置商品数目时，秒杀尚未开始
        if product_number is None:
            print('秒杀尚未开始')
            return False
        # 如果用户已经秒杀成功了
        if redis_client.sismember(SUCCESS_USER_KEY, user):
            print('你已秒杀成功，不能重复购买')
            return False
        # 如果库存不足，秒杀失败
        if int(product_number) <= 0:
            print('没有库存了')
            return False
        # 事务
        pipe.multi()
        # 商品数量减1
        pipe.decr(PRODUCT_NUMBER_KEY)
        # 记录秒杀成功的用户
        pipe.sadd(SUCCESS_USER_KEY, user)
        # 执行
        pipe.execute()
    except WatchError:
        print('秒杀失败')
        return False
    finally:
        pipe.reset()
    return True


def handle_buy_product(user):
    """
    抢购商品
    """
    try:
        with redis_client.lock('my-lock-key', blocking_timeout=5):
            # 获取库存
            product_number = redis_client.get(PRODUCT_NUMBER_KEY)
            # 未设置商品数目时，秒杀尚未开始
            if product_number is None:
                print('秒杀尚未开始')
                return False
            # 如果用户已经秒杀成功了
            if redis_client.sismember(SUCCESS_USER_KEY, user):
                print('你已秒杀成功，不能重复购买')
                return False
            # 如果库存不足，秒杀失败
            if int(product_number) <= 0:
                print('没有库存了')
                return False
            # 商品数量减1
            redis_client.decr(PRODUCT_NUMBER_KEY)
            # 记录秒杀成功的用户
            redis_client.sadd(SUCCESS_USER_KEY, user)
            return True
    except LockError:
        print('秒杀失败')
        return False
