from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.schemas.user_schema import (
    UserSignup,
    UserResponse,
    UserLogin,
    TokenResponse
)

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.services.auth_service import AuthService

from app.core.logger import logger

logger.info(
    "Employee list requested"
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/signup",
    response_model=UserResponse
)
async def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    try:

        return AuthService.signup(
            db,
            user
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    
@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    try:

        return AuthService.login(
            db,
            user
        )

    except Exception as error:

        raise HTTPException(
            status_code=401,
            detail=str(error)
        )    