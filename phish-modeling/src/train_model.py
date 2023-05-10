import logging
import pickle
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

def train_model(df: pd.DataFrame, config: Dict[str, Dict], model_type: str) -> Tuple[object, pd.DataFrame, pd.DataFrame]:
    """
    Function to train a model based on the provided configuration.
    
    Args:
        df (pd.DataFrame): The input dataframe for training.
        config (Dict[str, Dict]): A dictionary with model training details.
        model_type (str): The type of model to train. Can be "RandomForest" or "XGBoost".
        
    Returns:
        Tuple[object, pd.DataFrame, pd.DataFrame]: Tuple containing the trained model object, train and test dataframe.
    """
    try:
        # Create train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            df.drop("status", axis = 1), df["status"], 
            test_size = config["split"]["test_size"], 
            random_state = config["split"]["random_state"]
        )

        # Create a model
        if model_type == "RandomForest":
            model = RandomForestClassifier(
                n_estimators=config["RandomForest"]["n_estimators"], 
                min_samples_split=config["RandomForest"]["min_samples_split"], 
                max_depth=config["RandomForest"]["max_depth"], 
                random_state=config["RandomForest"]["random_state"]
            )
        elif model_type == "XGBoost":
            model = XGBClassifier(
                n_estimators=config["XGBoost"]["n_estimators"], 
                learning_rate=config["XGBoost"]["learning_rate"], 
                max_depth=config["XGBoost"]["max_depth"]
            )

        # Train model on the training data
        model.fit(X_train, y_train)
        
        logger.info(f"Successfully trained the {model_type} model.")
        
        return model, X_train, X_test
    except Exception as e:
        logger.error(f"Error occurred while training the model. Error: {e}")
        raise e

def save_split(train: pd.DataFrame, test: pd.DataFrame, path: Path) -> None:
    """
    Function to save the train and test split dataframes to disk.
    
    Args:
        train (pd.DataFrame): The train dataframe.
        test (pd.DataFrame): The test dataframe.
        path (Path): The directory where the dataframes should be saved.
        
    Returns:
        None
    """
    try:
        train.to_csv(path / "train.csv", index=False)
        test.to_csv(path / "test.csv", index=False)
        logger.info(f"Successfully saved train/test split data to {path}.")
    except Exception as e:
        logger.error(f"Error occurred while saving train/test split data. Error: {e}")
        raise e

def save_model(model: object, filepath: Path) -> None:
    """
    Function to save the trained model to disk.
    
    Args:
        model (object): The trained model object.
        filepath (Path): The file path where the model should be saved.
        
    Returns:
        None
    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Successfully saved model to {filepath}.")
    except Exception as e:
        logger.error(f"Error occurred while saving model. Error: {e}")
        raise e
    