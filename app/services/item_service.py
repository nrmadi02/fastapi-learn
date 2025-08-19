from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate

from app.repositories.item_repository import item_repo


class ItemService:
    async def create_item_for_user(
        self, db: AsyncSession, *, item_in: ItemCreate, owner_id: int
    ) -> Item:
        """
        Create a new item for a specific user.
        """
        # We can't use the generic create method from the repo directly
        # because we need to inject the owner_id.
        res = await item_repo.create_for_user(db=db, item_in=item_in, owner_id=owner_id)
        return res

    async def list(
        self, db: AsyncSession, owner_id: int, page: int, size: int
    ) -> Page[Item]:
        res = await item_repo.get_by_owner(
            db=db, owner_id=owner_id, page=page, size=size
        )
        return res


item_service = ItemService()
