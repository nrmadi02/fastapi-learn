from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.security.jwt import create_access_token
from app.security.password import get_password_hash, verify_password

router = APIRouter()


@router.post("/register", response_model=Token, summary="Register new user")
async def register(
    payload: RegisterRequest, session: AsyncSession = Depends(get_session)
):
    exists = await session.execute(select(User).where(User.email == payload.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, password=get_password_hash(payload.password))
    session.add(user)
    await session.commit()
    token = create_access_token(user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token, summary="Login and get JWT")
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).where(User.email == payload.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(user.email)
    return Token(access_token=token)
