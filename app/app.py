# coding: utf-8
from flask import Flask, request, jsonify, make_response
from logging import getLogger
from functools import wraps
import config
import logging.config
import os
import sys
import time
import yaml

LOG_CONFIG_FILE = '\..\config\log_config.yaml'
CONFIG_OBJECT = 'config.AppConfig'

logger = None
app = Flask(__name__,
            static_url_path='',
            static_folder='',
            template_folder='')


def api(route, methods=['POST'], content_type='application/json'):
    """
    APIを定義する関数
    - content-typeのvalidationをする
    - ライブラリの処理速度を計測してログに出力する
    """
    def decorate(func):
        @app.route(route, methods=methods)
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get("Content-Type") == content_type:
                error_message = {
                    'error': 'not supported Content-Type'
                }
                return make_response(jsonify(error_message), 400)
            logger.info('{0} : start'.format(func.__name__))
            start = time.perf_counter()
            data = request.get_json(silent=True)
            if data:
                result = func(data)
            else:
                result = func(*args, **kwargs)
            t = get_elapsed_time_in_ms(start)
            logger.info('{0} : finish. [{1}ms]'.format(func.__name__, t))
            return jsonify(result)
        return wrapper
    return decorate


def get_elapsed_time_in_ms(start_time):
    """
    時間を計測する関数。結果の単位はミリ秒
    """
    SEC_IN_MSEC = 1000
    elapsed_time = round((time.perf_counter() - start_time) * SEC_IN_MSEC, 2)
    return elapsed_time


@api(route='/hello', methods=['GET'], content_type=None)
def hello():
    return 'Hello, world!'


if __name__ == '__main__':
    log_file = os.path.dirname(os.path.abspath(__file__)) + LOG_CONFIG_FILE
    logging.config.dictConfig(
        yaml.load(open(log_file).read()))
    logger = getLogger(__name__)
    logger.info('app start')
    app.config.from_object(CONFIG_OBJECT)
    # werkzeugのログ無効化(run前にやる必要がある)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.disabled = True
    # app.run()
    # 外部公開用
    app.run(host=config.AppConfig.HOST, port=config.AppConfig.PORT)
    # Flaskのログ無効化(run後にやる必要がある)
    app.logger.disabled = True
