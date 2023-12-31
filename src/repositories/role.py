from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from src.database.connection import get_db
from src.models.model import Role


class RoleRepository:
    def __init__(self, session=Depends(get_db)):
        self.session = session

    async def get_role_list(
        self,
        performance_id: UUID,
        limit: int,
        cursor: str | None = None,
    ) -> list[Role]:
        query = select(Role).where(Role.performance_id == performance_id)

        if cursor is not None:
            query = query.where(Role.created_at < cursor)

        query = query.order_by(Role.created_at.desc()).limit(limit)

        return list((await self.session.execute(query)).scalars().all())

    async def save_role(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)

        return role
