import pandas as pd
import yaml
from src.feature_extractor import extract_features
from src.generate_features import generate_features
from src.load_model import load_model

# Global variables for config and model
CONFIG = None
MODEL_TRAINED = None

def lambda_handler(event, context):
    """AWS Lambda function handler.
    Args:
        event (dict): The event dictionary passed by AWS Lambda. This should contain the URL to perform inference on.
        context (object): The context in which the function is called.
    Returns:
        int: Prediction result (0 if legitimate, 1 if phishing).
    """
    global CONFIG, MODEL_TRAINED

    # Load config file from S3 if not already loaded
    if CONFIG is None:
        with open('config/config.yaml', 'r') as f:
            CONFIG = yaml.safe_load(f)

    # Load model object if not already loaded
    if MODEL_TRAINED is None:
        MODEL_TRAINED = load_model(CONFIG["aws"])

    # Get the URL from the event
    url = event['url']

    # Perform the inference
    return inference(url, CONFIG)

def inference(url: str, config: dict) -> list:
    """
    Perform inference on the given URL using the provided configuration.

    Args:
        url (str): The URL to perform inference on.
        config (dict): Configuration dictionary.

    Returns:
        int: Prediction result (0 if legitimate, 1 if phishing).
    """
    # Access variables
    headers = config['headers']
    row = extract_features(url)

    # Put headers on the data
    data = pd.DataFrame([row], columns=headers)

    # Generate new features and drop unwanted features
    features = generate_features(data, config["generate_features"]).drop(columns=["url", "status"])

    # Use the global model object
    return MODEL_TRAINED.predict(features)
