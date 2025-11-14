import logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('System check started.')
logging.warning('Low disk space.')
logging.error('Service connection failed.')