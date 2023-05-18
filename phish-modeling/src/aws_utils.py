import logging
import os
from pathlib import Path
from typing import List

import boto3
from botocore.exceptions import NoCredentialsError

logger = logging.getLogger(__name__)

def upload_artifacts(artifacts: Path, config: dict) -> List[str]:
    """Upload all the artifacts in the specified directory to S3.

    Args:
        artifacts: Directory containing all the artifacts from a given experiment
        config: Config required to upload artifacts to S3; see example config file for structure

    Returns:
        List of S3 url's for each file that was uploaded
    """
    try:
        session = boto3.Session()
        s3_session = session.client("s3")
        logger.info("Boto3 S3 client started")
    except NoCredentialsError as e:
        logger.error("AWS credentials not found: %s", e)
        raise
    except Exception as e:
        logger.error("Error occurred while creating AWS session: %s", e)
        raise

    bucket = config["bucket_name"]
    s3_urls = []

    for root, _, files in os.walk(artifacts):
        for file in files:
            local_path = os.path.join(root, file)
            
            if file.endswith(".csv"):
                prefix = config["data_prefix"]
            elif file.endswith(".yaml"):
                prefix = config["config_prefix"]
            elif file.endswith(".pkl"):
                prefix = config["model_prefix"]
            elif file.endswith(".png"):
                prefix = config["visuals_prefix"]
            else:
                prefix = config["prefix"]

            s3_key = os.path.join(prefix, os.path.relpath(local_path, artifacts))

            try:
                s3_session.upload_file(str(local_path), bucket, s3_key)
                logger.debug("Uploaded %s to %s:%s", local_path, bucket, s3_key)
                url = f"https://{bucket}.s3.amazonaws.com/{s3_key}"
                s3_urls.append(url)
            except FileNotFoundError as e:
                logger.error("Could not find file: %s", local_path)
                raise e
            except TypeError as e:
                logger.error("Invalid file type: %s", local_path)
                raise e
            except Exception as e:
                logger.error("Error occurred while uploading %s to S3: %s", local_path, e)
                raise e
    logger.info("All artifacts uploaded to S3 bucket.")
    return s3_urls
