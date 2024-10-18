from flask import Blueprint, jsonify, request
from loguru import logger
from helpers.aws_helpers import describe_ec2_instances, create_ec2_instance  # Import the new helper function
import os

# Load the API key from the environment variable
API_KEY = os.getenv('API_KEY')

# Create the blueprint
aws_bp = Blueprint('aws', __name__)

# Authentication decorator
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    
    # Set a unique endpoint name to avoid conflicts
    decorated_function.__name__ = f"decorated_{f.__name__}"
    return decorated_function

@aws_bp.route('/list', methods=['GET'])
@require_api_key  # Protect this route with the API key
def list_ec2_instances():
    """API endpoint to list EC2 instances."""
    logger.info("Received request to list EC2 instances.")
    try:
        instances = describe_ec2_instances()  # Call the helper function to get EC2 instances
        logger.info(f"Successfully retrieved instances: {instances}")
        return jsonify(instances)  # Return the list of instances as JSON
    except Exception as e:
        logger.error(f"Error retrieving EC2 instances: {e}")  # Log any error that occurs
        return jsonify({"error": "Failed to retrieve EC2 instances."}), 500

@aws_bp.route('/create', methods=['POST'])  # New route for creating an instance
@require_api_key  # Protect this route with the API key
def create_instance():
    """API endpoint to create an EC2 instance."""
    logger.info("Received request to create an EC2 instance.")
    data = request.get_json()  # Get the JSON data from the request

    # Extract the parameters from the JSON payload
    instance_type = data.get("InstanceType")
    image_id = data.get("ImageId")
    min_count = data.get("MinCount", 1)  # Default to 1 if not provided
    max_count = data.get("MaxCount", 1)  # Default to 1 if not provided

    # Create the EC2 instance
    try:
        instance = create_ec2_instance(instance_type, image_id, min_count, max_count)
        logger.info(f"Successfully created instance: {instance}")
        return jsonify(instance), 201  # Return the created instance with a 201 status
    except Exception as e:
        logger.error(f"Error creating EC2 instance: {e}")
        return jsonify({"error": "Failed to create EC2 instance."}), 500