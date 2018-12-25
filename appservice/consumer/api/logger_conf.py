import logging


logger = logging.basicConfig(filename='consumer_logs.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')