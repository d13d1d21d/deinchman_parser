from enum import Enum
from dataclasses import dataclass, asdict


class Selectors(Enum):
    BRAND_LINK = "a[class*='category-link']"
    PRODUCT_IMAGE = "div[class*='product-preview-item']"
    SIZE_LIST = "ul[class*='sizes']"
    COLOR = "span[class*='color']"
    MATERIAL = "*[type='material']"

@dataclass
class ProductData:
    url: str
    sku: str
    spu: str
    name: str
    brand: str
    category: str
    price: int
    in_stock: int
    color: str
    color_origin: str
    size: str
    images: list[str]
    description: str
    materials: dict[str, any]

COLORS = {
    "Weiss": "белый",
    "Blau": "голубой",
    "Grau": "серый",
    "Schwarz": "черный",
    "Braun": "коричневый",
    "Rot": "красный",
    "Silber": "серебряный",
    "Marine": "морской",
    "Bunt": "разноцветный",
    "Beige": "бежевый",
    "Kaki": "хаки",
    "Orange": "оранжевый",
    "Rosa": "розовый",
    "Bordeaux": "бордовый",
    "Violett": "фиолетовый",
    "Grün": "зелёный",
    "Gold": "золотой",
    "Creme": "кремовый",
    "Gelb": "желтый",
    "Cognac": "коричневый",
    "Maulwurf": "коричневый",
    "Multicolor": "разноцветный",
    "Other": "другой",
    "Silbern": "серебряный",
    "Leopard": "разноцветный",
    "Camel": "темно-бежевый",
    "Bronze": "бронза",
    "Multifarben": "разноцветный",
    "Malvenfarben": "лиловый",
    "Fuchsienrot": "розовый",
    "Pfirsisch": "светло-желтый",
    "Champagne": "оранжевый",
    "Goldfarben": "золотой",
    "Navy": "темно-синий",
    "Lila": "лиловый",
    "Glitterfarbe": "глиттер",
    "Olive": "оливковый",
    "Flamme": "светло-оранжевый",
    "Mustard": "оранжевый",
    "Senf": "оранжевый",
    "Schattengrau": "серый",
    "Capretto": "бежевый",
    "Elfenbein": "кремовый",
    "Platin": "светло-серый",
    "Pink": "розовый",
    "Turquoise": "бирюза",
    "Gruen": "зеленый",
    "White": "белый",
    "Standard Farbe": "не определено",
    "Weiß": "белый"
}

MATERIALS = {
    "Obermaterial": "upper_material",
    "Obermaterial - Detailangabe": "upper_material_details",
    "Innenmaterial": "inner_material",
    "Innenmaterial - Detailangabe": "inner_material_details",
    "Innensohle": "insole",
    "Innensohle - Detailangabe": "insole_details",
    "Laufsohle": "outsole",
    "Laufsohle - Detailangabe": "outsole_details"
}

class StockData(Enum):
    LAST_ITEM = "fast ausverkauft"
    OUT_OF_STOCK = "Leider ausverkauft"

