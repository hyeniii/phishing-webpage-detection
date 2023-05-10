import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

def save_data(df: pd.DataFrame, filepath: Path) -> None:
    """
    Function to save a dataframe to a specified file path.
    
    Args:
        df (pd.DataFrame): The input dataframe to be saved.
        filepath (Path): The file path where the dataframe should be saved.
        
    Returns:
        None
    """
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully saved data to {filepath}.")
    except Exception as e:
        logger.error(f"Error occurred while saving data. Error: {e}")
        raise e
