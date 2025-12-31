import logging
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(base_dir, 'app.log')

logger = logging.getLogger('LibraryApp')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)