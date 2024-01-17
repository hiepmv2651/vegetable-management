from sqlalchemy.orm import Session, joinedload

from app.model.models import Products


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
        products = (
            db.query(Products)
            .options(joinedload(Products.category))
            .filter(Products.name.ilike(f"%{search}%"))
            .order_by(
                getattr(Products, sort_value).asc()
                if sort_type
                else getattr(Products, sort_value).desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return products
