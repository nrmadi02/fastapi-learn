from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.item import Item
from app.repositories.base_repository import BaseRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):

    async def get_by_owner(
        self, db: AsyncSession, *, owner_id: int, offset: int = 0, limit: int = 100
    ) -> list[Item]:
        res = await db.execute(
            select(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
        )
        return list(res.scalars().all())

    async def create_for_user(
        self, db: AsyncSession, *, item_in: ItemCreate, owner_id: int
    ) -> Item:
        item_data = item_in.model_dump()
        db_obj = self.model(**item_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


item_repo = ItemRepository(Item)
