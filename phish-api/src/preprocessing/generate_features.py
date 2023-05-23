import logging
from typing import Dict

import pandas as pd

logger = logging.getLogger(__name__)

def generate_features(df: pd.DataFrame, config: Dict[str, str]) -> pd.DataFrame:
    """
    Function to generate new features in the dataframe as per the provided configuration.
    
    Args:
        df (pd.DataFrame): The input dataframe for feature generation.
        config (Dict[str, str]): A dictionary with feature generation details. 
        It must include 'standardize_prefix' and 'standardize_by' keys.
        
    Returns:
        pd.DataFrame: The dataframe with new features.
    """
    try:
        # Find all the columns that starts with specified prefix
        feature_cols = [item for item in df.columns if item.startswith(config["standardize_prefix"])]
        
        # Standardize all these columns by the specified column
        for col in feature_cols:
            df[col] = df[col]/df[config["standardize_by"]]
        
        logger.info("Successfully generated features.")
    except Exception as e:
        logger.error(f"Error occurred while generating features. Error: {e}")
        raise e

    return df
