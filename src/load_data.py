import io
import logging
from typing import Dict

import boto3
import pandas as pd

logger = logging.getLogger(__name__)

def load_data(config: Dict[str, str]) -> pd.DataFrame:
    """
    Function to load a csv file from an AWS S3 bucket into a pandas dataframe.
    
    Args:
        config (Dict[str, str]): A dictionary with AWS configuration details. 
        It must include "bucket_name" and "file_key" keys.
        
    Returns:
        pd.DataFrame: A pandas dataframe loaded from the csv file specified in the config.
    """
    # Validate the keys in config
    if not all(key in config for key in ["bucket_name", "file_key"]):
        logger.error("The config dictionary must contain \"bucket_name\" and \"file_key\".")
        raise ValueError("The config dictionary must contain \"bucket_name\" and \"file_key\".")
    
    # Assuming the AWS SSO profile is correctly configured in the machine
    # The S3 client will automatically use the credentials provided by AWS SSO
    s3_client = boto3.client("s3")

    bucket_name = config["bucket_name"]
    file_key = config["file_key"]

    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = obj["Body"].read()  # read the csv file as bytes
        string_data = data.decode("utf-8")  # decode bytes to string
        df = pd.read_csv(io.StringIO(string_data))  # create pandas dataframe
        logger.info(f"Successfully loaded data from s3://{bucket_name}/{file_key}")
    except Exception as e:
        logger.error(f"Error occurred while loading data from s3://{bucket_name}/{file_key}. Error: {e}")
        raise e

    return df
