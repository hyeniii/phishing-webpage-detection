import logging
from typing import Dict, Any

import boto3
import pickle

logger = logging.getLogger(__name__)

def load_model(config: Dict[str, str]) -> Any:
    """
    Function to load a pickled object from an AWS S3 bucket.
    
    Args:
        config (Dict[str, str]): A dictionary with AWS configuration details. 
        It must include "bucket_name" and "file_key" keys.
        
    Returns:
        Any: The unpickled object loaded from the specified file in the S3 bucket.
    """
    # Validate the keys in config
    if not all(key in config for key in ["bucket_name", "file_key"]):
        logger.error("The config dictionary must contain \"bucket_name\" and \"file_key\".")
        raise ValueError("The config dictionary must contain \"bucket_name\" and \"file_key\".")
    
    # Assuming the AWS SSO profile is correctly configured on the machine
    # The S3 client will automatically use the credentials provided by AWS SSO
    s3_client = boto3.client("s3")

    bucket_name = config["bucket_name"]
    file_key = config["file_key"]

    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = obj["Body"].read()  # Read the pickle file as bytes
        unpickled_object = pickle.loads(data)  # Unpickle the object
        logger.info(f"Successfully loaded object from s3://{bucket_name}/{file_key}")
    except Exception as e:
        logger.error(f"Error occurred while loading object from s3://{bucket_name}/{file_key}. Error: {e}")
        raise e

    return unpickled_object
