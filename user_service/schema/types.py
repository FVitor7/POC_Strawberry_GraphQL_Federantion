import strawberry
from models import models
from sqlalchemy import select
from typing import List, Optional


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    name: str
    email: str
    cpf: str

    @classmethod
    def marshal(cls, model: models.User) -> "User":
        return cls(id=strawberry.ID(str(model.id)), name=model.name, email=model.email, cpf=model.cpf)


@strawberry.federation.type(keys=["id"], extend=True)
class Task:
    id: strawberry.ID = strawberry.federation.field(external=True)
    task_name: str = strawberry.federation.field(external=True)

    @strawberry.federation.field(requires=["task_name"])
    def code(self) -> str:
        return f"TaskService: {self.task_name}"

    @strawberry.field
    async def tasks(self) -> List["Task"]:
        if self.id:
            async with models.get_session() as s:
                sql = select(models.User).where(models.User.tasks == self.id)
                db_tasks = (await s.execute(sql)).scalars().unique().all()
            return [Task.marshal(tasks) for tasks in db_tasks]
        else:
            return []


    @classmethod
    async def resolve_reference(cls, id: strawberry.ID, task_name: Optional[str] = None):
        return cls(id=id, task_name=task_name)