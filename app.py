from flask import Flask
import signal, os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from datetime import datetime

now = datetime.now()

app = Flask(__name__)
logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')

@app.route('/', methods=['GET'])
def home():
    logger.info('Request arrived to Home')
    return "Hello from Flask"

def exit_handler(signum, frame):
    current_time = now.strftime("%H:%M:%S")
    logger.warning("Exiting because of signal number" + str(signum) + "| Time: " + str(current_time))
    print("Exiting because of signal number" + str(signum) + "| Time: " + str(current_time))
    exit(0)

def signal_handler(signum, frame):
    current_time = now.strftime("%H:%M:%S")
    logger.warning("Signal number: " + str(signum) + "| Time: " + str(current_time))
    print("Signal number: " + str(signum) + "| Time: " + str(current_time))
    return

if __name__ != '__main__':
    logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=e68b4afd-0d26-44ce-a1ae-b0707eb83c64'))
    logger.setLevel(logging.INFO)
    logger.addHandler(gunicorn_logger.handlers[0])
    logger.setLevel(gunicorn_logger.level)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=e68b4afd-0d26-44ce-a1ae-b0707eb83c64'))
    logger.setLevel(logging.INFO)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    app.run(host='0.0.0.0', debug=True, port=8082)