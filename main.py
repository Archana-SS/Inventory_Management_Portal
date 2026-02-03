from fastapi import FastAPI, Depends, HTTPException
from models import Product
from database import engine, Base, SessionLocal
from schemas import ProductSchema
from sqlalchemy.orm import Session
from seed_data import SAMPLE_PRODUCTS
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

# create SQLite database & tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def seed_database():
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            db.add_all([Product(**p) for p in SAMPLE_PRODUCTS])
            db.commit()
            print("Database initialized with sample products.")
    finally:
        db.close()


@app.get("/")
def greet():
    return "Welcome to your Inventory Track!!"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    """for product in products:
        if product.id == id:
            return product"""
    if not product:
        #raise HTTPException(status_code=404, detail="Product not found")
        return "Product not found"
    return product

@app.post("/products")
def add_product(product:ProductSchema, db: Session = Depends(get_db)):
    #products.append(product)
    """db.add(product)
    db.commit()
    db.refresh(product)
    return product"""
    data=product.model_dump(exclude={"id"})
    db_product = Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}")
def update_product(id:int,product:ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        #raise HTTPException(status_code=404, detail="Product not found")
        return "Product not found"
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        #raise HTTPException(status_code=404, detail="Product not found")
        return "Product not found"
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}