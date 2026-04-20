from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "price_model.joblib"

FEATURE_COLUMNS = [
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
    "FloorType",
    "WallType",
    "RepairType",
    "BalconyBlockPresence",
    "ElevatorPresence",
]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}\n"
            "Сначала запусти train.py"
        )
    return joblib.load(MODEL_PATH)


def _normalize_features(features: dict) -> dict:
    normalized = dict(features)

    if "TotalArea" in normalized:
        normalized["TotalArea"] = float(str(normalized["TotalArea"]).replace(",", "."))

    return normalized


def predict_price(**features) -> float:
    model = load_model()

    missing_columns = [column for column in FEATURE_COLUMNS if column not in features]
    if missing_columns:
        raise ValueError(f"Missing input fields: {missing_columns}")

    input_df = pd.DataFrame([_normalize_features(features)], columns=FEATURE_COLUMNS)
    predicted_price = model.predict(input_df)[0]
    return float(predicted_price)


if __name__ == "__main__":
    price = predict_price(
        RoomsCount=2,
        TotalArea=54.3,
        BuildingAge=12,
        BanksCount=4,
        BarsCount=3,
        KindergartensCount=8,
        FillingStationsCount=1,
        CafesCount=2,
        CinemasCount=0,
        SubwayStationcCount=0,
        ClothingStoresCount=3,
        PublicTransportStopsCount=9,
        CulturalParksCount=1,
        PizzeriasCount=2,
        ChildsClinicsCount=1,
        PostOfficesCount=2,
        DentalClinicsCount=2,
        GroceryStoresCount=10,
        ShoppingMallsCount=1,
        UniversitiesCount=0,
        SchoolsCount=6,
        FloorType="Не первый и не последний",
        WallType="Кирпичные",
        RepairType="Косметический ремонт",
        BalconyBlockPresence="Да",
        ElevatorPresence="Да",
    )

    print(f"Predicted price: {price:,.2f}")
