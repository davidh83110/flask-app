from flask_restful import Resource
from flask import request
import socket


class Validate(Resource):
    def post(self):
        data = request.get_json()
        ip = data.get('ip', '')
        if self._is_valid_ipv4(ip):
            return {'status': True}
        else:
            return {'message': 'Invalid IPv4 Address'}, 400

    @staticmethod
    def _is_valid_ipv4(ip):
        try:
            """
            `inet_pton` can validate both IPv4 and IPv6, 
            but here we specify `AF_INET` for only validating IPv4.
            """
            socket.inet_pton(socket.AF_INET, ip)
        except socket.error:
            return False
        return True
