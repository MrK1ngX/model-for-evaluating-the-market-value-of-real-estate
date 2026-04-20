# Novosibirsk real estate model

Адаптированная версия проекта под базу `Novosibirsk real estate data.csv`.

## Что изменено
- обучение теперь идёт на файле `src/data/novosibirsk_real_estate_data.csv`
- CSV читается с разделителем `;`
- поле `TotalArea` автоматически переводится из формата `66,6` в `66.6`
- целевая колонка: `Value`
- модель заменена на `RandomForestRegressor`, потому что на этой базе она даёт лучшее качество, чем обычная линейная регрессия

## Запуск обучения
```bash
cd src
python3 train.py
```

## Запуск предсказания
```bash
cd src
python3 predict.py
```

## Использование в коде
```python
from predict import predict_price

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
```
