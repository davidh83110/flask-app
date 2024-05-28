from flask_restful import Resource
from flask import jsonify, Response
import time
from prometheus_client import generate_latest
from clients.redis_client import redis_client
from configs import config


class Root(Resource):
    def get(self):
        return jsonify({
            "version": config.APP_VERSION,
            "date": int(time.time()),
            "kubernetes": config.IS_KUBERNETES
        })


class Health(Resource):
    def get(self):
        try:
            """
            We need to make sure the Redis is up beofre we return healthy.
            """
            redis_client.ping()
            return {'status': 'healthy'}, 200
        except redis.ConnectionError:
            return {'status': 'unhealthy'}, 500


class Metrics(Resource):
    def get(self):
        return Response(generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'})
