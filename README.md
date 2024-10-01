# Blog Application

This is a blog application built with FastAPI, using MongoDB as the database, Docker for containerization, and Pytest for testing.

## Features

- **User Authentication**: JWT-based authentication for users (register/login).
- **CRUD Blog Operations**: Users can create, read, update, and delete blog posts.
- **MongoDB Integration**: MongoDB is used to store user, blog and comments data.
- **Docker Support**: The application is containerized with Docker for easy deployment.
- **Unit Testing**: Pytest is used for unit and integration testing.

## Getting Started

Ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Python 3.8+](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community)



#### Run Project

First create docker network 

```
sudo docker network create --driver bridge <your-network-name-here>
```

Create mongodb container following these commands

```
sudo docker run -d -it --name mongodb-container -e MONGO_INITDB_ROOT_USERNAME=<your-username-here> -e MONGO_INITDB_ROOT_PASSWORD=<your-password-here> -p 27017:27017 --network <your-network-name-here> mongo
```

Create image of the project folloing these commands

```
sudo docker build -t <your-docker-image-name-here> <projects-path-here>
```

Finally run the backend container using these commands

```
docker run -d -p 8000:8000 -it --name <container-name> <image-name>
```

#### Run Tests

```
python3 test_runner.py
```

## Todo

##### New Endpoints
- [ ] Like and dislike comments, blogs
- [ ] Add profile picture for profile and cover picture for blogs
- [ ] Notifications

---------------------------

##### System
- [ ] Logging on exception events
- [ ] Slowapi implementation for request control 
- [ ] AWS image storage connection
- [ ] Docker compose

---------------------------

##### Enviorements
- [ ] Test enviorement
- [ ] Product enviorement

---------------------------

##### Tests
- [ ] Router blog tests
- [ ] Router user tests
- [ ] Router comments tests