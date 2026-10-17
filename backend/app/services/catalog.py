from app.models.category import CatalogItem, CatalogPreset, CatalogResponse

CATALOG = (
    CatalogItem(id="groceries", name="Groceries", icon="shopping_cart"),
    CatalogItem(id="dining_out", name="Dining Out", icon="restaurant"),
    CatalogItem(id="transport", name="Transport", icon="directions_car"),
    CatalogItem(id="housing", name="Housing", icon="home"),
    CatalogItem(id="bills", name="Bills", icon="receipt_long"),
    CatalogItem(id="health", name="Health", icon="medical_services"),
    CatalogItem(id="entertainment", name="Entertainment", icon="movie"),
    CatalogItem(id="shopping", name="Shopping", icon="shopping_bag"),
    CatalogItem(id="travel", name="Travel", icon="flight"),
    CatalogItem(id="education", name="Education", icon="school"),
    CatalogItem(id="subscriptions", name="Subscriptions", icon="subscriptions"),
)

PRESETS = (
    CatalogPreset(
        id="essential_4",
        name="Essential",
        catalog_ids=["groceries", "transport", "housing", "entertainment"],
    ),
    CatalogPreset(
        id="complete_6",
        name="Complete",
        catalog_ids=[
            "groceries",
            "transport",
            "housing",
            "entertainment",
            "dining_out",
            "health",
        ],
    ),
)

CATALOG_BY_ID = {item.id: item for item in CATALOG}


def get_catalog() -> CatalogResponse:
    return CatalogResponse(items=list(CATALOG), presets=list(PRESETS))
