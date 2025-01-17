from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix='/api/operations',
    tags=['Operation'],
)


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return {
        'status': '200',
        'data': result.mappings().all(),
        'details': None
    }


@router.post('/')
async def create_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stm = insert(operation).values(**new_operation.dict())
    await session.execute(stm)
    await session.commit()
    return {
        'status': '201'
    }
