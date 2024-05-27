from flask_restful import Resource
from flask import request, jsonify
import socket
import time
from clients.redis_client import redis_client


class Lookup(Resource):
    def get(self):
        domain = request.args.get('domain', '')

        if not domain:
            return {'message': 'Missing required parameter: domain'}, 400

        try:
            """
            `gethostbyname_ex` will return multiple IPv4 addresses, but not suppport IPv6.
            """
            addresses = socket.gethostbyname_ex(domain)[2]
            ipv4_addresses = [addr for addr in addresses if ':' not in addr]

            result = {
                'addresses': ipv4_addresses,
                'client_ip': request.remote_addr,
                'created_at': int(time.time()),
                'domain': domain
            }

            """
            lpush will add new element to the beginning of the list.
            And set an expire TTL for each elements. 
            """
            redis_client.lpush('history_data', str(result))
            redis_client.expire('history_data', 604800)

            return jsonify(result)
        except socket.gaierror:
            return {'message': 'Domain not found'}, 404


