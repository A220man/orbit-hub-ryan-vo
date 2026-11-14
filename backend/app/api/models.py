import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.model import Model
from app.schemas.model import ModelCreate, ModelListResponse, ModelResponse, ModelUpdate
from app.auth.manager import get_current_user
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


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
) -> ModelListResponse:
    stmt = select(Model)
    result = await db.execute(stmt)
    models = result.scalars().all()
    return ModelListResponse(
        items=[ModelResponse.model_validate(m) for m in models],
        total=len(models),
        page=1,
        page_size=len(models),
    )


@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ModelResponse:
    model = await db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return ModelResponse.model_validate(model)


@router.patch("/models/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: uuid.UUID,
    model_in: ModelUpdate,
    db: AsyncSession = Depends(get_db),
) -> ModelResponse:
    model = await db.get(Model, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for field, value in model_in.model_dump(exclude_unset=True).items():
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
        raise HTTPException(status_code=404, detail="Model not found")
    await db.delete(model)
    await db.commit()
