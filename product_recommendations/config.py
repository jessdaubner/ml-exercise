"""Configure logging and global path variables"""
import os
import sys
import logging

# Configure logging
logger = logging.getLogger('recommender')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt='%(levelname)s | %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)
logger.setLevel('INFO')

# Data file locations
APP_DIR = os.getenv('APP_DIR', '.')
logger.info('APP_DIR set to {}'.format(APP_DIR))

DATA_DIR = '{}/data'.format(APP_DIR)
RAW_DATA = '{}/recs.csv'.format(DATA_DIR)
RECS = '{}/recommendations.csv'.format(DATA_DIR)
