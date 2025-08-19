from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserCreate
from app.security.jwt import create_access_token
from app.security.password import get_password_hash, verify_password
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=Token, summary="Register new user")
async def register(
    payload: RegisterRequest, session: AsyncSession = Depends(get_session)
):
    exists = await auth_service.get_by_email(db=session, email=payload.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await auth_service.create(
        db=session,
        user_in=UserCreate(
            email=payload.email,
            password=get_password_hash(payload.password),
        ),
    )
    token = auth_service.access_token(user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token, summary="Login and get JWT")
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await auth_service.get_by_email(db=session, email=payload.email)
    valid_password = auth_service.check_password(payload.password, user.password)
    if not user or not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(user.email)
    return Token(access_token=token)
