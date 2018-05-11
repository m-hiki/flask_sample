
import app
import argparse
import sys
import os

LOG_CONFIG_FILE = '\..\config\log_config.yaml'

if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', help='',
                        type=str, choices=['dev', 'stg', 'prd'],
                        default='dev')
    """

    name = os.path.dirname(os.path.abspath(__file__))
    log_file = name + LOG_CONFIG_FILE

    app.run_submarine(5001, log_file)
