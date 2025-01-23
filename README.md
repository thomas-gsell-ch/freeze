# Freeze - Freezer-Management App

## Run the app in docker containers

_Make sure you have docker installed on your local machine._

- Go to project directory and run `docker-compose up` (with `-d` you can run it in detached mode)
  This creates docker images and starts up the following containers:
- frontend_prod
- productproviderservice
- bestreachedpnsservice
- mongo_products
- mongo_prodperlocs
- mongo_warndates
- rabbitmq
- rabbitmq_initializer

### Open the app UI

- Go to http://localhost:8080 to view the production UI

### Testprotokoll

Here you can find the [Testprotokoll](Testprotokoll.md) where the main functionality and how to test it, is described.

## Local development environment

### Run the app in docker containers

- Go to project directory and run `docker-compose -f docker-compose.dev.yml up` (with `-d` you can run it in detached mode)
  This creates docker images and starts up the following containers:
- frontend_prod
- frontend_dev
- productproviderservice
- bestreachedpnsservice
- mongo_products
- mongo_prodperlocs
- mongo_warndates
- mongo-express
- rabbitmq
- rabbitmq_initializer

### Endpoints

- Open http://localhost:8080 to view the production UI
- Open http://localhost:3000 to view the development UI
- Open http://localhost:5000 to view flask productproviderservice
- Open http://localhost:5001 to view flask bestreachedpnsservice
- Open http://localhost:8081 to view mongo express
- Open http://localhost:15672 to view the rabbitmq management

### How to run frontend locally

1. Install npm and node.js
2. Go to project directory and run `npm install`
3. Go to project directory and run `npm run`
4. Debug configuration: Launch Chrome

### How to run flask productproviderservice locally in a devcontainer

1. Install Dev Containers extension in VS Code
2. Run VS Code in Dev Container
3. Debug configuration: Python Debugger: Flask

### MongoDB connection string

mongodb://root:example@localhost:27017/

MongoDB connection string from within DevContainer:
mongodb://root:example@host.docker.internal:27017
