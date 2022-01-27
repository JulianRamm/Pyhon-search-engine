from dataclasses import dataclass

@dataclass
class Product:
    productId: int
    product: str
    category: str
    brand: str
    price: float
    quantity: int
    freeShipping: bool
    prestige: int