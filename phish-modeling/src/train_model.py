import logging
import pickle
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

def train_model(df: pd.DataFrame, config: Dict) -> Tuple[object, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataframe into train, validation, and test sets.
    Conducts grid search and cross-validation on RandomForest and XGBoost models.
    Selects and trains the best model based on CV accuracy.

    Args:
        df (pd.DataFrame): The input data frame to split and train on.
        config (dict): Configuration dictionary that includes parameters for data split, model, and grid search.
        
    Returns:
        best_model (object): The model that has the highest cross-validation accuracy.
        df_train (pd.DataFrame): The training set.
        df_validation (pd.DataFrame): The validation set.
        df_test (pd.DataFrame): The test set.
    """

    try:
        # Split the data into 80% train, 18% validation, and 2% test
        df_train, df_temp = train_test_split(df, test_size=config["split"]["test_size"], random_state=config["split"]["random_state"])
        df_validation, df_test = train_test_split(df_temp, test_size=config["split"]["test_size_validation"], random_state=config["split"]["random_state"])

        X_train = df_train.drop("status", axis=1)
        y_train = df_train["status"]
        
        models = [
            ("RandomForest", RandomForestClassifier(), config["grid_search"]["RandomForest"]),
            ("XGBoost", XGBClassifier(), config["grid_search"]["XGBoost"])
        ]
        
        highest_accuracy = 0
        best_model = None

        for name, model, params in models:
            grid_search = GridSearchCV(estimator=model, param_grid=params, cv=config["split"]["cv"], scoring="accuracy", n_jobs=-1)
            grid_search.fit(X_train, y_train)

            logger.info(f"Best parameters for {name}: {grid_search.best_params_}")
            logger.info(f"Best cross-validation accuracy for {name}: {round(grid_search.best_score_, 3)}")

            if grid_search.best_score_ > highest_accuracy:
                best_model = grid_search.best_estimator_
                highest_accuracy = grid_search.best_score_
        
        best_model.fit(X_train, y_train)
        logger.info(f"Best trained model: {type(best_model).__name__}")

        return best_model, df_train, df_validation, df_test

    except Exception as e:
        logger.error(f"Error occurred during model training: {str(e)}")
        raise e

def save_split(train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame, path: Path) -> None:
    """
    Function to save the train, validation, and test split dataframes to disk.
    
    Args:
        train (pd.DataFrame): The train dataframe.
        validation (pd.DataFrame): The validation dataframe.
        test (pd.DataFrame): The test dataframe.
        path (Path): The directory where the dataframes should be saved.
        
    Returns:
        None
    """
    try:
        train.to_csv(path / "train.csv", index=False)
        validation.to_csv(path / "validation.csv", index=False)
        test.to_csv(path / "test.csv", index=False)
        logger.info(f"Successfully saved train/validation/test split data to {path}.")
    except Exception as e:
        logger.error(f"Error occurred while saving train/validation/test split data. Error: {e}")
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
    