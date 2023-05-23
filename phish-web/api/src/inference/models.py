import pandas as pd
import numpy as np
import yaml
from src.preprocessing.feature_extractor import extract_features
from src.preprocessing.generate_features import generate_features
from src.preprocessing.load_model import load_model
from src.preprocessing.load_data import load_data


def url_inference(url: str, config: dict) -> list:
    """
    Perform inference on the given URL using the provided configuration.

    Args:
        url (str): The URL to perform inference on.
        config (dict): Configuration dictionary.

    Returns:
        int: Prediction result (0 if legitimate, 1 if phishing).
    """
    # Load model object
    # If need to call random forest, change file-key in config
    model_trained = load_model(config["aws_model"])

    # Load original data to check if the user provided URL is in our data already
    urls = load_data(config["aws_full_data"])["url"]
    # If so, we can skip the feature generation steps and just pull the features from S3
    if np.isin(url, urls):
        print("Found this url in dataset. Using existing features to fit model.")
        # Get the cleaned and processed data
        phish_ready_features = load_data(config["aws_features"])
        # Match by the index
        match_index = np.where(urls == url)[0]
        # Grab the features
        features = phish_ready_features.iloc[match_index].drop(columns=["status"])
    else:
        print("Didn't find this url in dataset. Generating features....")
        # Access variables
        headers = config['headers']
        row = extract_features(url)

        # Put headers on the data
        data = pd.DataFrame([row], columns=headers)

        # Generate new features and drop unwanted features
        features = generate_features(data, config["generate_features"]).drop(columns=["url", "status"])
        print("Features generated. Running best model trained....")

    return model_trained.predict(features)


def predict_and_save(url: str):
    with open('config/inference_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    input_url = url

    # Call the inference function
    pred = url_inference(input_url, config)

    return pred