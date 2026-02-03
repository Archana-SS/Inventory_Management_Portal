'''

class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int

    """
    This constructor is not needed when we use pydantic BaseModel

     def __init__(self,id:int,name:str,description:str,price:float,quantity:int):
        self.id=id
        self.name=name
        self.description=description
        self.price=price
        self.quantity=quantity 
    """

'''

from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True  # IMPORTANT for SQLAlchemy
