from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.helper.json_response_default import JSONResponseDefault
from app.schema import category_schema
from app.service.category_service import CategoryService


router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
    default_response_class=ORJSONResponse,
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
async def get_categories(db: Session = Depends(get_db)):
    categories = CategoryService.get_all_categories(db)
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=JSONResponseDefault(
                status=False, message="No categories found"
            ).model_dump(),
        )
    response = [
        category_schema.CategoryGet.model_validate(category) for category in categories
    ]

    return {
        "status": True,
        "message": "Success",
        "data": response,
    }


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
async def get_category_by_id(db: Session = Depends(get_db), id: int = Path(..., ge=1)):
    category = CategoryService.get_category_by_id(db, id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=JSONResponseDefault(
                status=False, message="No category found"
            ).model_dump(),
        )
    response = category_schema.CategoryGet.model_validate(category).model_dump()

    return {
        "status": True,
        "message": "Success",
        "data": response,
    }


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=JSONResponseDefault
)
async def create_category(
    category: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
):
    result = CategoryService.create_category(db, category)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(status=False, message=result).model_dump(),
        )

    return {
        "status": True,
        "message": "Category created successfully",
    }


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
async def update_category(
    category: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
    id: int = Path(..., ge=1),
):
    result = CategoryService.update_category(db, category, id)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(status=False, message=result).model_dump(),
        )

    return {
        "status": True,
        "message": "Category updated successfully",
    }


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault
)
async def delete_category(
    db: Session = Depends(get_db),
    id: int = Path(..., ge=1),
):
    result = CategoryService.delete_category(db, id)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(status=False, message=result).model_dump(),
        )

    return {
        "status": True,
        "message": "Category deleted successfully",
    }
