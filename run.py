# run.py
from app.factory import create_app  # Import the factory function
from loguru import logger
import sys
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure Loguru to log both to stderr and a file
logger.remove()
logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")
logger.add("logs/app.log", rotation="1 MB", level="INFO") 

# Log the startup process
logger.info("Starting the application...")

# Create the Flask app using the factory function
app = create_app()

# Start the Flask application (use uWSGI for production)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Enable debug mode for local testing