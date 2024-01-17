from fastapi import HTTPException, UploadFile, status

from app.helper.json_response_default import JSONResponseDefault


VALID_IMAGE_TYPES = ["jpg", "jpeg", "png"]
MAX_IMAGE_SIZE = 1024 * 1024 * 2  # 2MB


def validate_image(image: UploadFile):
    if image.filename.split(".")[-1] not in VALID_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(
                status=False, message="Image must be jpg, jpeg, or png", data=None
            ).model_dump(),
        )
    if image.size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(
                status=False, message="Image size must be less than 2MB", data=None
            ).model_dump(),
        )
