import strawberry
from models import models


@strawberry.federation.type(keys=["id"])
class User:
    id: strawberry.ID
    name: str
    email: str
    cpf: str

    @classmethod
    def marshal(cls, model: models.User) -> "User":
        return cls(
            id=strawberry.ID(str(model.id)),
            name=model.name,
            email=model.email,
            cpf=model.cpf,
        )



