import logging
from flask import Flask, jsonify
from flask_cors import CORS
from app.routes.aws_routes import aws_bp
from loguru import logger

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)  # Create Flask app

    CORS(app)  # Enable CORS

    # Register the AWS routes blueprint
    app.register_blueprint(aws_bp, url_prefix='/api/v1/instance')

    # Global exception handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled Exception: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

    logger.info("Flask app created successfully.")
    return app
