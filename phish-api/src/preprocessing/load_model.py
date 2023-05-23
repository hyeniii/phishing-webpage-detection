import logging
from typing import Dict, Any

import boto3
import pickle
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache()
def load_model(config: tuple[str, str]) -> Any:
    """
    Function to load a pickled object from an AWS S3 bucket.
    
    Args:
        config (Dict[str, str]): A dictionary with AWS configuration details. 
        It must include "bucket_name" and "file_key" keys.
        
    Returns:
        Any: The unpickled object loaded from the specified file in the S3 bucket.
    """
    # Validate the keys in config
    if not all(key == "bucket_name" or key == "file_key" for key, _ in config):
        logger.error("The config tuple must contain (\"bucket_name\", \"file_key\").")
        raise ValueError("The config tuple must contain (\"bucket_name\", \"file_key\").")
    
    bucket_name = next(value for key, value in config if key == "bucket_name")
    file_key = next(value for key, value in config if key == "file_key")
    # Assuming the AWS SSO profile is correctly configured on the machine
    # The S3 client will automatically use the credentials provided by AWS SSO
    s3_client = boto3.client("s3")

    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = obj["Body"].read()  # Read the pickle file as bytes
        unpickled_object = pickle.loads(data)  # Unpickle the object
        logger.info(f"Successfully loaded object from s3://{bucket_name}/{file_key}")
    except Exception as e:
        logger.error(f"Error occurred while loading object from s3://{bucket_name}/{file_key}. Error: {e}")
        raise e

    return unpickled_object
