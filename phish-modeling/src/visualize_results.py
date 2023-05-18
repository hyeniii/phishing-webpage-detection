import logging
from pathlib import Path
from typing import Dict, Union

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from xgboost import XGBClassifier

logger = logging.getLogger(__name__)

def visualize_results(model: Union[RandomForestClassifier, XGBClassifier], validation: pd.DataFrame, artifacts: Path, config: Dict) -> None:
    """
    Function to generate model performance metric visualizations on validation.

    Args:
        model (Union[RandomForestClassifier, XGBClassifier]): Trained model.
        validation (pd.DataFrame): The validation dataset.
        artifacts (Path): The directory where the plots should be saved.
        config (Dict): Configuration dictionary.
    
    Returns:
        None
    """
    try:
        logger.info("Generating predictions on validation data...")
        # Extract features and target
        X = validation.drop("status", axis=1)
        y_true = validation["status"]
        y_pred = model.predict(X)
        y_score = model.predict_proba(X)[:, 1]  # scores for the positive class

        # Confusion matrix
        logger.info("Generating confusion matrix...")
        conf_matrix = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(conf_matrix, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues, cbar=False)
        ax.set(xlabel="Predicted", ylabel="True", title="Confusion Matrix")
        plt.savefig(str(artifacts / config["confusion_matrix_filename"]))
        plt.close()

        # Classification report
        logger.info("Generating classification report...")
        report = classification_report(y_true, y_pred, output_dict=True)
        df_report = pd.DataFrame(report).transpose()
        df_report = df_report.loc[["0", "1"], ["precision", "recall", "f1-score"]]
        df_report = df_report.round(3)
        fig, ax = plt.subplots()
        ax.axis("tight")
        ax.axis("off")
        ax.table(cellText=df_report.values, colLabels=df_report.columns, rowLabels=df_report.index, cellLoc = "center", loc="center")
        ax.set_title("Classification Report")
        fig.tight_layout()
        fig.savefig(str(artifacts / config["classification_report_filename"]))
        plt.close()

        # ROC curve 
        logger.info("Generating ROC curve...")
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        plt.figure()
        plt.plot(fpr, tpr, color="salmon", lw=2, label='ROC curve (AUC: %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color="steelblue", lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.savefig(str(artifacts / config["roc_curve_filename"]))
        plt.close()

        logger.info("Successfully generated and saved all model performance visualizations.")
    
    except Exception as e:
        logger.error("Error occurred while generating model performance visualizations. Error: %s", str(e))
        raise e
