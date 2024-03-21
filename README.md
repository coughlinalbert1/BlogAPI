# BlogAPI
FastAPI, Docker, PostgreSQL


### Dockerfile
This file tells Docker how to create the Docker image.

### Docker Compose
This file basically tells Docker how the Docker container will run. This allows us to just run the file in the terminal and then it will execute the commands in the docker-compose.yml file. The commands here will set up environment variables, define services, port management, and define volumes. Normally, we wouldn't include this in the github repo, because it contains information we want to keep private, like database login info and API secrets, but this is just an example project so there is not anything serious here.

