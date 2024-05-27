import os

APP_VERSION = os.getenv('APP_VERSION', '0.0.1')
IS_KUBERNETES = os.getenv('IS_KUBERNETES', 'False').lower() == 'true'   # Default is False
LOG_FILE = os.getenv('LOG_FILE', 'flask-app.log')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
GRACEFUL_SHUTDOWN_PERIOD = os.getenv('GRACEFUL_SHUTDOWN_PERIOD', 1)
