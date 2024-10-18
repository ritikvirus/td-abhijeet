# run.py
from app.factory import create_app  # Import the factory function
from loguru_config import setup_logging, logger  # Import logging setup and logger

# Setup logging
setup_logging()

# Log the startup process
logger.info("Starting the application...")

# Create the Flask app using the factory function
app = create_app()

# Start the Flask application (use uWSGI for production)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Enable debug mode for local testing

