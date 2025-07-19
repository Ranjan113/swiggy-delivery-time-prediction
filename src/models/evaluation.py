import pandas as pd
import logging
import joblib
from pathlib import Path
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import json



# Constants
TARGET = "time_taken"

# Setup logger
logger = logging.getLogger("model_evaluation")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_data(data_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Data loaded from {data_path}")
        return df
    except FileNotFoundError:
        logger.error(f"The file {data_path} does not exist.")
        raise


def make_X_and_y(data: pd.DataFrame, target_column: str):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y


def load_model(model_path: Path):
    try:
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        raise


def save_metrics_json(path: Path, metrics: dict):
    with open(path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics saved to {path}")


if __name__ == "__main__":
    # Define paths
    root_path = Path(__file__).parent.parent.parent
    train_data_path = root_path / "data" / "processed" / "train_trans.csv"
    test_data_path = root_path / "data" / "processed" / "test_trans.csv"
    model_path = root_path / "models" / "model.pkl"  
    metrics_path = root_path / "metrics.json"

    # Load data
    train_data = load_data(train_data_path)
    test_data = load_data(test_data_path)

    # Split into features and target
    X_train, y_train = make_X_and_y(train_data, TARGET)
    X_test, y_test = make_X_and_y(test_data, TARGET)
    logger.info("Data split into X and y")

    # Load model
    model = load_model(model_path)

    # Predict
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Metrics
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1)
    mean_cv_score = -cv_scores.mean()

    logger.info(f"Train MAE: {train_mae}")
    logger.info(f"Test MAE: {test_mae}")
    logger.info(f"Train R2: {train_r2}")
    logger.info(f"Test R2: {test_r2}")
    logger.info(f"Cross-Validation Scores: {[-s for s in cv_scores]}")
    logger.info(f"Mean CV Score: {mean_cv_score}")

    # Save all metrics to JSON
    metrics = {
        "train_mae": train_mae,
        "test_mae": test_mae,
        "train_r2": train_r2,
        "test_r2": test_r2,
        "mean_cv_score": mean_cv_score,
        "cv_scores": [-s for s in cv_scores.tolist()]  
    }
    save_metrics_json(metrics_path, metrics)

