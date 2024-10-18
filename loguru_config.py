# loguru_config.py
from loguru import logger
import sys
import os
import json
from elasticsearch import Elasticsearch

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# File path for local logs
log_file_path = "logs/app.log"

# Global variable for Elasticsearch connection
es = None

# Connect to Elasticsearch
def connect_elasticsearch():
    global es  # Declare `es` as a global variable
    try:
        es = Elasticsearch(
            "http://3.232.154.215:9200",
            basic_auth=("elastic", "OPxsR6Z6*NNm*QyHvzXj")  # Provide username and password
        )
        if es.ping():
            logger.info("Connected to Elasticsearch successfully!")
        else:
            logger.error("Failed to connect to Elasticsearch.")
    except Exception as e:
        logger.warning(f"Error connecting to Elasticsearch: {e}")

# Custom function to send logs to Elasticsearch
def send_log_to_elasticsearch(message):
    if es:  # Check if `es` is defined
        log_record = json.loads(message)
        es.index(index="deployer_dev", body=log_record)
    else:
        logger.warning("Elasticsearch instance is not available.")

# Initialize logging configuration
def setup_logging():
    logger.remove()  # Remove any default handlers
    logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")
    logger.add(log_file_path, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="1 MB", level="INFO")

    connect_elasticsearch()  # Connect to Elasticsearch
    if es:  # Add to logger if connected
        logger.add(
            send_log_to_elasticsearch,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            serialize=True,
            level="INFO"
        )

# Define custom logging level if needed
events_level = logger.level("EVENT", no=38, color="<yellow>", icon="🔔")

