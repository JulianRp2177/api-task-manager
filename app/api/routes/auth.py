from fastapi import APIRouter
from app.domain.schemas.user import UserCreate, UserOut
from app.services.auth_service import auth_service
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user: UserCreate) -> UserOut:
    """
    Register a new user.

    **Args**:
        - user (UserCreate): The user data including email and password.

    **Returns**:
        - UserOut: The registered user's public data.

    **Raises**:
        - HTTPException: 400 if the email is already registered.
    """
    return await auth_service.register_user(user)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authenticate a user and return a JWT token.

    **Args**:
        user (UserLogin): The user's email and password.

    **Returns**:
        dict: A dictionary containing the access token and token type.

    **Raises**:
        HTTPException: 401 if credentials are invalid.
    """
    return await auth_service.login_user(form_data)
