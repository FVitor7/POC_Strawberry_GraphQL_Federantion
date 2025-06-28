# POC Strawberry GraphQL and FastAPI
This project demonstrates a federated GraphQL setup composed of two
FastAPI microservices and an Apollo Gateway. Each service can be run
individually or all together using Docker.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

Go to one of the microservice folders and run:

```bash
pip install -r requirements.txt
```

## Usage

### Users Microservice

Open the user_service folder in your terminal and run:
```bash
uvicorn app:app --port 8000 --reload
```

### Tasks Microservice

Open the task_service folder in your terminal and run:
```bash
uvicorn app:app --port 8800 --reload
```
### Gateway

Open the gateway folder in your terminal and isntall npm dependencies:
```bash
npm install
```

```bash
npm run-script dev
```

Federation of the two microservices will be available on port 8080

Access: http://localhost:8080

### Running with Docker Compose

To start all services at once use `docker-compose`:

```bash
docker-compose build
docker-compose up
```

The gateway will be available on http://localhost:8080

## Generating the Schema

In the microservice folder run:
```bash
strawberry export-schema schema.schema > schema/schema.graphql
```

## Mutations
#### createUser
```bash
mutation {
  createUser(
    cpf: "12345678900"
    email: "fabio@example.com"
    name: "Fábio Vitor"
  ) {
    id
    name
    email
    cpf
  }
}
```
#### addCategory
```bash
mutation {
  addCategory(categoryName: "Tecnologia") {
    __typename
    ... on Category {
      id
      categoryName
    }
    ... on CategoryExists {
      message
    }
  }
}
```
#### addCategory
```bash
mutation {
  addTask(
    categoryName: "Tecnologia"
    taskName: "Estudar Federation"
    userId: 1
  ) {
    __typename
    ... on Task {
      id
      taskName
      userId
      category {
        id
        categoryName
      }
    }
    ... on TaskExists {
      message
    }
  }
}
```
## Queries
#### federation Example
```bash
query {
  users(cpf: "12345678900") {
    id
    name
    email
    tasks {
      id
      taskName
      category {
        id
        categoryName
      }
    }
  }
}
```
