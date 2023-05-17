import pandas as pd
import yaml
from src.feature_extractor import extract_features
from src.generate_features import generate_features
from src.load_model import load_model

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

    # Load model object
    # If need to call random forest, change file-key in config
    model_trained = load_model(config["aws"])

    return model_trained.predict(features)

def main():
    """
    Main entry point of the script.
    """
    # Load config file
    with open('./phish-inference/src/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    input_url = config["url"]

    # Call the inference function
    result = inference(input_url, config)

    # Print the result
    print(result)

if __name__ == '__main__':
    main()
