 # helpers/aws_helpers.py
from config import efs_client, ec2_client
from loguru import logger

def create_efs():
    """Create an EFS using AWS SDK."""
    try:
        logger.info("Creating EFS with CreationToken 'mytoken'")
        response = efs_client.create_file_system(CreationToken='mytoken')
        logger.info(f"EFS created successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Error creating EFS: {e}")
        return {"error": str(e)}

def describe_ec2_instances():
    """Describe EC2 instances."""
    try:
        logger.info("Describing EC2 instances...")
        response = ec2_client.describe_instances()
        return response['Reservations']
    except Exception as e:
        logger.error(f"Error retrieving EC2 instances: {e}")
        return {"error": str(e)}
    
######################################################################
def create_ec2_instance(instance_type, image_id, min_count=1, max_count=1):
    """Create an EC2 instance using AWS SDK."""
    try:
        logger.info(f"Creating EC2 instance: Type={instance_type}, ImageId={image_id}, MinCount={min_count}, MaxCount={max_count}")
        response = ec2_client.run_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MinCount=min_count,
            MaxCount=max_count
        )
        return response['Instances']
    except Exception as e:
        logger.error(f"Error creating EC2 instance: {e}")
        return {"error": str(e)}

