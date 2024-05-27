from flask import Flask, send_from_directory, request
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
import os
from utils.error_handlers import register_error_handlers
from utils.prometheus import PrometheusMetrics
from utils.logger import logger
import json

# Initialize Flask application and create a restful API
app = Flask(__name__)
api = Api(app)

# Initialize Prometheus Metrics
PrometheusMetrics(app, api)

# Initialize Error Handlers
register_error_handlers(app)


# Setup access log
# @app.after_request
# def after_request(response):
#     log_details = {
#         'remote_addr': request.remote_addr,
#         'method': request.method,
#         'scheme': request.scheme,
#         'path': request.full_path,
#         'status_code': response.status_code
#     }
#     access_logger.info(json.dumps({
#         'remote_addr': '%s',
#         'method': '%s',
#         'scheme': '%s',
#         'path': '%s',
#         'status_code': '%s'
#     }),
#         log_details['remote_addr'],
#         log_details['method'],
#         log_details['scheme'],
#         log_details['path'],
#         log_details['status_code'])
#     return response
@app.after_request
def after_request(response):
    log_details = {
        'remote_addr': request.remote_addr,
        'method': request.method,
        'scheme': request.scheme,
        'path': request.full_path,
        'status_code': response.status_code,
        'user_agent': request.headers.get('User-Agent')
    }
    logger.info('Request details', extra=log_details)
    return response


# Import apis
from api.v1.history import History
from api.v1.lookup import Lookup
from api.v1.validate import Validate
from api.root import Root, Health, Metrics

# Add resources to API
api.add_resource(History, '/v1/history', strict_slashes=False)
api.add_resource(Lookup, '/v1/tools/lookup', strict_slashes=False)
api.add_resource(Validate, '/v1/tools/validate', strict_slashes=False)
api.add_resource(Root, '/', strict_slashes=False)
api.add_resource(Health, '/health', strict_slashes=False)
api.add_resource(Metrics, '/metrics', strict_slashes=False)


# Setup Swagger and Blueprint
@app.route('/swagger.yaml', strict_slashes=False)
def swagger_yaml():
    swagger_file = os.path.join(app.root_path, 'swagger.yaml')
    return send_from_directory(os.path.dirname(swagger_file), os.path.basename(swagger_file))


SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "DNS Helper"
    }
)

# Register Swagger-UI
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL, strict_slashes=False)
