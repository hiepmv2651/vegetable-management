from fastapi import File, UploadFile
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.model.models import Products
from app.schema.product_schema import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def get_all_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: str = "",
        sort_value: str = "id",
        sort_type: bool = True,
    ):
        query = db.query(Products)

        if search:
            query = query.filter(Products.name.ilike(f"%{search}%"))

        sort_func = asc if sort_type else desc
        query = query.order_by(sort_func(getattr(Products, sort_value)))

        products = query.offset(skip).limit(limit).all()

        return products

    @staticmethod
    def get_product_by_id(db: Session, id: int):
        product = db.query(Products).filter(Products.id == id).one_or_none()

        return product

    @staticmethod
    def create_product(
        db: Session, product: ProductCreate, image: UploadFile = File(...)
    ):
        try:
            existing_product = (
                db.query(Products).filter(Products.name == product.name).one_or_none()
            )
            if existing_product:
                return "A product with this name already exists."
            if image:
                image_url = f"app/static/images/{image.filename}"
                with open(image_url, "wb") as buffer:
                    content = image.file.read()
                    buffer.write(content)
            else:
                image_url = None

            new_product = Products(**product.model_dump(), image_url=image_url)
            db.add(new_product)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)

    @staticmethod
    def update_product(
        db: Session, product: ProductUpdate, id: int, image: UploadFile = File(...)
    ):
        try:
            existing_product = (
                db.query(Products).filter(Products.id == id).one_or_none()
            )
            if not existing_product:
                return "Product not found."
            if image:
                image_url = f"app/static/images/{image.filename}"
                with open(image_url, "wb") as buffer:
                    content = image.file.read()
                    buffer.write(content)
            else:
                image_url = existing_product.image_url

            existing_product.image_url = image_url
            db.query(Products).filter(Products.id == id).update(
                product.model_dump(), synchronize_session=False
            )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)

    @staticmethod
    def delete_product(db: Session, id: int):
        try:
            existing_product = (
                db.query(Products).filter(Products.id == id).one_or_none()
            )
            if not existing_product:
                return "Product not found."
            db.delete(existing_product)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)
