from typing import Optional

import strawberry
from models import models
from sqlalchemy import String, select
from strawberry.fastapi import GraphQLRouter
from .types import Category, Task, User
from database.database import get_session


@strawberry.type
class TaskExists:
    message: str = "Task with this name already exist"

AddTaskResponse = strawberry.union("AddTaskResponse", (Task, TaskExists))


@strawberry.type
class CategoryExists:
    message: str = "Category with this name already exist"

AddCategoryResponse = strawberry.union("AddCategoryResponse", (Category, CategoryExists))


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_task(self, task_name: str, user_id: Optional[int], category_name: Optional[str]) -> AddTaskResponse:
        async with get_session() as s:
            db_category, db_task = None, None
            
            if category_name:
                sql_category = select(models.Category).where(models.Category.category_name == category_name)
                db_category = (await s.execute(sql_category)).scalars().first()
            
            sql_task = select(models.Task).where(models.Task.task_name == task_name)
            db_task = (await s.execute(sql_task)).scalars().first()

            if db_task is not None:
                return TaskExists()

            if user_id:
                db_task = models.Task(task_name=task_name, user_id=user_id, category=db_category)
            else:
                db_task = models.Task(task_name=task_name, category=db_category)

            s.add(db_task)
            await s.commit()
        return Task.marshal(db_task)

    
    @strawberry.mutation
    async def add_category(self, category_name: str) -> AddCategoryResponse:
        async with get_session() as s:
            sql = select(models.Category).where(models.Category.category_name == category_name)
            existing_db_category = (await s.execute(sql)).first()
            if existing_db_category is not None:
                return CategoryExists()
            db_category = models.Category(category_name=category_name)
            s.add(db_category)
            await s.commit()
        return Category.marshal(db_category)



@strawberry.type
class Query:
    @strawberry.field
    def tasks_service(self) -> str:
        return "tasks"

    @strawberry.field
    async def tasks(
        self,
        id: Optional[int] = None,
        task_name: Optional[str]= None,
        user_id: Optional[int] = None
        ) -> list[Task]:

        async with get_session() as s:
            sql = select(models.Task).order_by(models.Task.id)
            if id:
                sql = select(models.Task).filter(models.Task.id == id)
            if task_name:
                task_name = "%{}%".format(task_name)
                sql = select(models.Task).filter(models.Task.task_name.like(task_name))
            if user_id:
                sql = select(models.Task).filter(models.Task.user_id == user_id)
                
            db_tasks = (await s.execute(sql)).scalars().unique().all()
        return [Task.marshal(tasks) for tasks in db_tasks]


    @strawberry.field
    async def categories(
        self,
        id: Optional[int] = None,
        category_name: Optional[str]= None,
        ) -> list[Category]:

        async with get_session() as s:
            sql = select(models.Category).order_by(models.Category.id)
            if id:
                sql = select(models.Category).filter(models.Category.id == id)
            if category_name:
                category_name = "%{}%".format(category_name)
                sql = select(models.Category).filter(models.Category.category_name.like(category_name))

            db_category = (await s.execute(sql)).scalars().unique().all()
        return [Category.marshal(loc) for loc in db_category]



schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[User, Task, Category]
    )
    
graphql_app = GraphQLRouter(schema)