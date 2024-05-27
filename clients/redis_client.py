import redis
import os
from configs import config


class RedisClient:
    _instance = None

    """
    This is for make sure there's one 1 instance of Redis Client created at once.
    __new__ will be called before _init_redis to actal create the Redis Client.
    
    TODO: Implement retry for Redis Client in case Redis Server has occured unexpected interruption.  
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # if the instance hasn't been created, then create one and assign to _instance.
            cls._instance = super(RedisClient, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_redis()
        return cls._instance

    def _init_redis(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            password=config.REDIS_PASSWORD,
            decode_responses=True
        )

    def get_client(self):
        return self.client

    def lpush(self, key, value):
        return self.client.lpush(key, value)

    def lrange(self, key, start, end):
        return self.client.lrange(key, start, end)


# Initialize Redis Client
redis_client = RedisClient().get_client()
