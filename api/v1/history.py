from flask_restful import Resource
from flask import jsonify
from clients.redis_client import redis_client


class History(Resource):
    def get(self):
        try:
            history_data = redis_client.lrange('history_data', 0, 19)
            if history_data:
                return jsonify([item for item in history_data])
            else:
                return jsonify({"message": "No history data available, please try lookup first."}), 404
        except redis.exceptions.RedisError as e:
            return jsonify({"error": str(e)}), 500
