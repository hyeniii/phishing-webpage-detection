import argparse
import datetime
import logging.config
from pathlib import Path

import yaml

import src.aws_utils as aws
import src.generate_features as gf
import src.load_data as ld
import src.process_data as prd
import src.save_data as sd
import src.train_model as tm

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("pipeline")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Acquire, clean, and create features from phishing data"
    )
    parser.add_argument(
        "--config", default="config/modeling_config.yaml", help="Path to configuration file"
    )
    args = parser.parse_args()

    #Load configuration file for parameters and run config
    with open(args.config, "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.error.YAMLError as e:
            logger.error("Error while loading configuration from %s", args.config)
        else:
            logger.info("Configuration file loaded from %s", args.config)

    run_config = config.get("run_config", {})

    # Set up output directory for saving artifacts
    now = int(datetime.datetime.now().timestamp())
    artifacts = Path(run_config.get("output", "runs")) / str(now)
    artifacts.mkdir(parents=True)

    # Save config file to artifacts directory for traceability
    with (artifacts / "config.yaml").open("w") as f:
        yaml.dump(config, f)

    # Acquire data from S3 bucket
    df = ld.load_data(config["aws"])

    # Process data
    df = prd.process_data(df, config["process_data"])
  
    # Generate features; save to disk
    df = gf.generate_features(df, config["generate_features"])
    sd.save_data(df, artifacts / "phish_ready.csv")
    
    # Split data into train/test set and train models based on config; save each to disk
    rf, train, test = tm.train_model(df, config["train_model"], "RandomForest")
    xgb = (tm.train_model(df, config["train_model"], "XGBoost"))[0]
    tm.save_split(train, test, artifacts)
    tm.save_model(rf, artifacts / "rf_trained.pkl")
    tm.save_model(xgb, artifacts / "xgb_trained.pkl")

    # Upload all artifacts to S3
    aws_config = config.get("aws")
    if aws_config.get("upload", False):
        aws.upload_artifacts(artifacts, aws_config)
    else:
        logger.info("Not uploading any files to S3. To upload, change upload in aws config")
