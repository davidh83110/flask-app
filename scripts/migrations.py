import redis
import json
import os

redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'),
                           port=os.getenv('REDIS_PORT', 6379),
                           db=os.getenv('REDIS_DB', 0),
                           password=os.getenv('REDIS_PASSWORD', None),
                           decode_responses=True
                           )

current_path = os.getcwd()
redis_key = 'history_data'

if not redis_client.lrange(redis_key, 0, 1):
    print(f'Empty {redis_key}, starting initial data migration...')
    if os.path.exists(f'/data/history_data.json'):
        with open(f'/data/history_data.json', 'r') as f:
            history_data = json.load(f)
            for item in history_data:
                redis_client.lpush(redis_key, item)
            print('Redis data migrated.')
    else:
        print('Path not found')
else:
    print(f'{redis_key} data existed, migration will not start.')

