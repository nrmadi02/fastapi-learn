from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.security.password import verify_password
from app.repositories.user_repository import user_repo
from app.schemas.user import UserCreate
from app.security.jwt import create_access_token


class AuthService:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        return await user_repo.get_by_email(db=db, email=email)

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        return await user_repo.create_user(db=db, user_in=user_in)

    def check_password(self, password: str, hashed_password: str) -> bool:
        return verify_password(password, hashed_password)

    def access_token(self, email: str) -> str:
        return create_access_token(email)


auth_service = AuthService()
