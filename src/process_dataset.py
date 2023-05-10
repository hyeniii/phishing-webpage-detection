import logging
from typing import Dict

import pandas as pd

logger = logging.getLogger(__name__)

def process_data(df: pd.DataFrame, config: Dict[str, list]) -> pd.DataFrame:
    """
    Function to process a dataframe as per the provided configuration.
    
    Args:
        df (pd.DataFrame): The input dataframe to be processed.
        config (Dict[str, list]): A dictionary with processing details. 
        It must include 'drop_columns', 'drop_duplicates', 'drop_na', 
        'drop_columns_correlated' and 'drop_external_features' keys.
        
    Returns:
        pd.DataFrame: The processed dataframe.
    """
    try:
        # Drop specified columns
        df = df.drop(columns=config["drop_columns"])
        
        # Remove columns with strong/perfect correlation
        df = df.drop(columns=config["correlated_columns"])
        
        # Check and remove duplicates if specified
        if config["drop_duplicates"]:
            df = df.drop_duplicates()
        
        # Drop NA if specified
        if config["drop_na"]:
            df = df.dropna()
        
        # Drop external features
        df = df.drop(columns=config["external_features"])
        logging.info("Successfully processed data.")
    except Exception as e:
        logging.error(f"Error occurred while processing data. Error: {e}")
        raise e

    return df
