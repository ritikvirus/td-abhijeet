import os
import logging
from datadog_api_client.v2 import ApiClient, ApiException, Configuration
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import HTTPLog, HTTPLogItem

class DatadogHandler(logging.StreamHandler):
    """Custom logging handler to send logs to Datadog."""
    def __init__(self):
        super().__init__()
        configuration = Configuration()
        self.api_client = ApiClient(configuration)
        self.api_instance = logs_api.LogsApi(self.api_client)
        self.service_name = "my-flask-app"  # Change to your app name
        self.ddsource = "python"  # Identify the log source
        self.env = os.getenv("ENV", "DEV")  # Environment (DEV, PROD)

    def emit(self, record):
        msg = self.format(record)
        log_item = HTTPLogItem(
            ddsource=self.ddsource,
            ddtags=f"env:{self.env}",
            message=msg,
            service=self.service_name,
        )
        body = HTTPLog([log_item])

        try:
            self.api_instance.submit_log(body)  # Send logs to Datadog
        except ApiException as e:
            print(f"Failed to send log to Datadog: {e}")

def setup_logger():
    """Sets up the logger with Datadog and file handlers."""
    logger = logging.getLogger("my-flask-app")
    logger.setLevel(logging.INFO)

    # Datadog handler
    datadog_handler = DatadogHandler()
    datadog_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(datadog_handler)

    # Local file handler
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
    logger.addHandler(file_handler)

    return logger

