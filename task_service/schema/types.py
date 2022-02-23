from typing import List, Optional

import strawberry
from models import models
from sqlalchemy import select
from database.database import get_session


@strawberry.type
class Category:
    id: strawberry.ID
    category_name: str

    @strawberry.field
    async def tasks(self) -> List["Task"]:
        if self.id:
            async with get_session() as s:
                sql = select(models.Task).where(models.Task.category_id == self.id)
                db_tasks = (await s.execute(sql)).scalars().unique().all()
            return [Task.marshal(tasks) for tasks in db_tasks]
        else:
            return []

    @classmethod
    def marshal(cls, model: models.Category) -> "Category":
        return cls(id=strawberry.ID(str(model.id)), category_name=model.category_name)


@strawberry.type
class Task:
    id: strawberry.ID
    task_name: str
    user_id: int
    category: Optional[Category] = None


    @classmethod
    def marshal(cls, model: models.Task) -> "Task":
        return cls(
            id=strawberry.ID(str(model.id)),
            task_name=model.task_name,
            user_id=model.user_id,
            category=Category.marshal(model.category) if model.category else None,
        )
    

@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    name: str = strawberry.federation.field(external=True)

    @strawberry.federation.field(requires=["name"])
    def code(self) -> str:
        return f"TaskService: {self.task_name}"

    @strawberry.field
    async def tasks(self) -> List[Task]:
        if self.id:
            async with get_session() as s:
                sql = select(models.Task).where(models.Task.user_id == self.id)
                db_tasks = (await s.execute(sql)).scalars().unique().all()
            return [Task.marshal(tasks) for tasks in db_tasks]
        else:
            return []

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID, name: Optional[str] = None):
        return cls(id=id, name=name)
