from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, owner_id: int, data: ItemCreate) -> Item:
        item = Item(title=data.title, description=data.description, owner_id=owner_id)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def list(self, owner_id: int, limit: int, offset: int) -> list[Item]:
        res = await self.session.execute(
            select(Item)
            .where(Item.owner_id == owner_id)
            .order_by(Item.id)
            .limit(limit)
            .offset(offset)
        )
        return list(res.scalars())
