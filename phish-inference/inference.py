import pandas as pd
import yaml
from src.feature_extractor import extract_features
from src.generate_features import generate_features
from src.load_model import load_model

# Load config file
with open('./src/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

input_url = config["url"]

def inference(url):

    # Access variables
    headers = config['headers']
    row = extract_features(url)

    # Put headers on the data
    data = pd.DataFrame([row], columns=headers)

    # Generate new features and drop unwanted features
    features = generate_features(data, config["generate_features"]).drop(columns=["url", "status"])

    #Load model object
    xgb_trained = load_model(config["aws"])

    return xgb_trained.predict(features)

# returns 0 if legitimate, 1 if phishing
print(inference(input_url))
