from sqlalchemy.orm import Session

from app.model.models import Categories
from app.schema.category_schema import CategoryCreate

class CategoryService:
    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Categories).all()
    
    @staticmethod
    def get_category_by_id(db: Session, id: int):
        return db.query(Categories).filter(Categories.id == id).one_or_none()
    
    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        try:
            existing_category = (
                db.query(Categories).filter(Categories.name == category.name).one_or_none()
            )
            if existing_category:
                return "A category with this name already exists."
            new_category = Categories(**category.model_dump())
            db.add(new_category)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)
        
    @staticmethod
    def update_category(db: Session, category: CategoryCreate, id: int):
        try:
            existing_category = (
                db.query(Categories).filter(Categories.id == id).one_or_none()
            )
            if not existing_category:
                return "Category not found."
            db.query(Categories).filter(Categories.id == id).update(
                category.model_dump(), synchronize_session=False
            )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)
        
    @staticmethod
    def delete_category(db: Session, id: int):
        try:
            existing_category = (
                db.query(Categories).filter(Categories.id == id).one_or_none()
            )
            if not existing_category:
                return "Category not found."
            db.delete(existing_category)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return str(e)