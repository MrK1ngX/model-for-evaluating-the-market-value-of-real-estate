from __future__ import annotations

from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "novosibirsk_real_estate_data.csv"
MODEL_PATH = BASE_DIR / "models" / "price_model.joblib"
METRICS_PATH = BASE_DIR / "models" / "training_metrics.json"
TARGET_COLUMN = "Value"

NUMERIC_FEATURES = [
    "RoomsCount",
    "TotalArea",
    "BuildingAge",
    "BanksCount",
    "BarsCount",
    "KindergartensCount",
    "FillingStationsCount",
    "CafesCount",
    "CinemasCount",
    "SubwayStationcCount",
    "ClothingStoresCount",
    "PublicTransportStopsCount",
    "CulturalParksCount",
    "PizzeriasCount",
    "ChildsClinicsCount",
    "PostOfficesCount",
    "DentalClinicsCount",
    "GroceryStoresCount",
    "ShoppingMallsCount",
    "UniversitiesCount",
    "SchoolsCount",
]

CATEGORICAL_FEATURES = [
    "FloorType",
    "WallType",
    "RepairType",
    "BalconyBlockPresence",
    "ElevatorPresence",
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, sep=";")
    df["TotalArea"] = (
        df["TotalArea"].astype(str).str.replace(",", ".", regex=False).astype(float)
    )

    missing_columns = [column for column in ALL_FEATURES + [TARGET_COLUMN] if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {missing_columns}")

    return df[ALL_FEATURES + [TARGET_COLUMN]].copy()


def build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=300,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    return model


def main() -> None:
    df = load_dataset(DATA_PATH)

    x = df[ALL_FEATURES]
    y = df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = build_pipeline()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        "dataset_path": str(DATA_PATH),
        "model_path": str(MODEL_PATH),
        "rows": int(len(df)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "features": ALL_FEATURES,
        "target": TARGET_COLUMN,
    }
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Model trained successfully.")
    print(f"Saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")
    print(f"Rows: {len(df)}")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.4f}")


if __name__ == "__main__":
    main()
