from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        return await self.create(db=db, obj_in=user_in)

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        res = await db.execute(select(self.model).where(self.model.email == email))
        return res.scalar_one_or_none()


user_repo = UserRepository(User)
