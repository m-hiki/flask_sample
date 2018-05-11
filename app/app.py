# coding: utf-8
from flask import Flask
from logging import getLogger
import logging.config
import yaml

logger = None
app = Flask(__name__,
            static_url_path='',
            static_folder='',
            template_folder='')


def run_submarine(port, log_config_file):
    global logger
    logging.config.dictConfig(
        yaml.load(open(log_config_file).read()))
    logger = getLogger(__name__)
    app.run(debug=False, host='127.0.0.1', port=port)
    logger.info('Submarine started')


@app.route('/hello', methods=['GET'])
def hello():
    app.logger.info('start')
    message = 'Hello, world!'
    app.logger.info('finish')
    return message
