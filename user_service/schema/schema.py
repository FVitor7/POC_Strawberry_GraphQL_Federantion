from typing import List, Optional

import strawberry
from models import models
from .types import User
from sqlalchemy import select
from strawberry.fastapi import GraphQLRouter
from database.database import get_session


@strawberry.type
class UserExists:
    message: str = "User with this CPF already exist"

AddUserResponse = strawberry.union("AddUserResponse", (User, UserExists))

@strawberry.type
class Query:
    @strawberry.field
    def users_service(self) -> str:
        return "users_service"

    @strawberry.field
    async def users(
        self,
        id: Optional[int] = None,
        name: Optional[str]= None,
        cpf: Optional[str] = None,
        email: Optional[str] = None
        ) -> List[User]:

        async with get_session() as s:
            sql = select(models.User).order_by(models.User.id)
            if id:
                sql = select(models.User).filter(models.User.id == id)
            if name:
                name = "%{}%".format(name)
                sql = select(models.User).filter(models.User.name.like(name))
            if cpf:
                sql = select(models.User).filter(models.User.cpf == cpf)
            if email:
                sql = select(models.User).filter(models.User.email == email)
                
            db_users = (await s.execute(sql)).scalars().unique().all()
        return [User.marshal(loc) for loc in db_users]



@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str, cpf: str) -> AddUserResponse:
        async with get_session() as s:
            existing_db_user = None
            sql = select(models.User).where(models.User.cpf == cpf)
            existing_db_user = (await s.execute(sql)).first()
            
            if existing_db_user is not None:
                return UserExists()
                
            db_user = models.User(name=name, email=email, cpf=cpf)
            s.add(db_user)
            await s.commit()
        return User.marshal(db_user)


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[User]
    )
graphql_app = GraphQLRouter(schema)