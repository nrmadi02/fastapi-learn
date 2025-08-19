from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.item import Item, ItemCreate
from app.services.item_service import item_service
from app.utils.pagination import PaginationParams
from fastapi_pagination import Page, Params

router = APIRouter()


@router.post("", response_model=Item, summary="Create new item")
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = await item_service.create_item_for_user(
        db=session, item_in=payload, owner_id=current_user.id
    )
    return item


@router.get("", response_model=Page[Item], summary="List my items")
async def list_items(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = await item_service.list(
        db=session, owner_id=current_user.id, page=params.page, size=params.size
    )
    return items
