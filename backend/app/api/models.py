
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.model import Model
from app.schemas.model import ModelCreate, ModelListResponse, ModelResponse, ModelUpdate

router = APIRouter(tags=["models"])


@router.post("/models", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_in: ModelCreate,
    db: AsyncSession = Depends(get_db),
) -> ModelResponse:
    model = Model(**model_in.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return ModelResponse.model_validate(model)


@router.get("/models", response_model=ModelListResponse)
async def list_models(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    framework: Optional[str] = Query(None, description="Filter by framework"),
) -> ModelListResponse:
    stmt = select(Model)
    count_stmt = select(func.count(Model.id))

    if name:
        stmt = stmt.where(Model.name.ilike(f"%{name}%"))
        count_stmt = count_stmt.where(Model.name.ilike(f"%{name}%"))
    if framework:
        stmt = stmt.where(Model.framework == framework)
        count_stmt = count_stmt.where(Model.framework == framework)

    total = (await db.execute(count_stmt)).scalar_one()
    stmt = stmt.offset((page - 1) * page_size).limit(page_size).order_by(Model.created_at.desc())
    result = await db.execute(stmt)
    models = result.scalars().all()

    return ModelListResponse(
        items=[ModelResponse.model_validate(m) for m in models],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ModelResponse:
    model = await db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return ModelResponse.model_validate(model)


@router.patch("/models/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: uuid.UUID,
    model_in: ModelUpdate,
    db: AsyncSession = Depends(get_db),
) -> ModelResponse:
    model = await db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    update_data = model_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(model, field, value)

    await db.commit()
    await db.refresh(model)
    return ModelResponse.model_validate(model)


@router.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    model = await db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    await db.delete(model)
    await db.commit()
