import boto3
from dotenv import load_dotenv
import os
from loguru import logger  

 
load_dotenv()

# Retrieve AWS region from environment or use a default
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')  
logger.info(f"Using AWS region: {AWS_REGION}")

# Create AWS clients with error handling
try:
    efs_client = boto3.client('efs', region_name=AWS_REGION)
    logger.info("EFS client created successfully.")
except Exception as e:
    logger.error(f"Failed to create EFS client: {e}")

try:
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    logger.info("EC2 client created successfully.")
except Exception as e:
    logger.error(f"Failed to create EC2 client: {e}")

# Retrieve security group ID from environment or use default
security_group_id = os.getenv('SECURITY_GROUP_ID', 'sg-022d05b4b6bd78b78')
logger.info(f"Using security group ID: {security_group_id}")

 
def get_clients():
    """Return AWS clients for EFS and EC2."""
    return efs_client, ec2_client

def get_security_group_id():
    """Return the security group ID."""
    return security_group_id

