# POC Strawberry GraphQL and FastAPI
Foobar is a Python library for dealing with word pluralization.

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

Federation of the two microservices will be available on port 7000

Access: http://localhost:7000

## Generating the Schema

In the microservice folder run:
```bash
strawberry export-schema schema.schema > schema/schema.graphql
```

