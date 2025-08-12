from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import ItemService
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.post("/", response_model=ItemRead, summary="Create new item")
async def create_item(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = ItemService(session)
    item = await svc.create(owner_id=current_user.id, data=payload)
    return ItemRead.model_validate(item)


@router.get("/", response_model=list[ItemRead], summary="List my items")
async def list_items(
    page: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = ItemService(session)
    items = await svc.list(
        owner_id=current_user.id, limit=page.limit, offset=page.offset
    )
    return [ItemRead.model_validate(it) for it in items]
