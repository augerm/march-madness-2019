import os
import logging

# Imports the Google Cloud client library
import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Connects the logger to the root logging handler; by default this captures
# all logs at INFO level and higher
client.setup_logging()

logging.info("@@@ Running startup script...")
logging.info("@@@ Fetching origin...")
os.system('git pull origin master...')

logging.info("@@@ Running main.py...")
os.system('python3 ../main.py')

# Turn off machine when finished in order to limit costs.
logging.info("@@@ Shutting down machine...")
os.system('sudo poweroff')
