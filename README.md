# Welcome!
My name is William and this is my project that I've been working on for a little while. I've had frustrations with the Degree planner that Rutgers (New Brunswick) has, so I wanted to create my own. Funnily enough, this project was also inspired by one of my assignments in my cs classes, who knew? Its my most ambitious project yet, and one that I hope to transform into a full fledged deployed application. The goal is to make it much more convenient for students to track, plan, and manage their courses depending on the meeting times, professor ratings from RateMyProfessor.com.

The API itself is a dedicated RestAPI with CRUD operations, and has all the available courses, professors, and sections of a class in the desired semester. The passwords to their online account are encrpyted and each user session has been tokenized with JWT tokens.

# Getting started
First you would need to have docker desktop downloaded [here](https://www.docker.com/products/docker-desktop/)

## Docker Desktop
The API is containerized in these docker containers so that you will not need to worry about downloading dependencies.

You need to trust the third party application, and signing in is optional.

# Docker Commands
- ```Docker-compose up -d``` will build all the containers necessary for the application
- ```sudo docker-compose up --build -d --no-deps api``` will build the API without the dependencies.
- ```docker-compose down``` will stop the containers
- ``` docker-compose down -v``` stops containers and removes the volume
- ```docker ps``` lists all the docker containers


# Limitations
There are a few limitations on my project:
- This is only designed with BA/BS degree track in mind. Tackling the all the courses for all the majors/degree paths would be a very daunting task to start off with. I will scale my application, only after creating a minimal viable product. 
- If there is no dependencies, the current program has to first start the API so that it will not prematurely try to connect to the postgres database without first creating it. 
**Note**: this will usually only happen once (at the start of the container creation with docker), or whenever the local volume is deleted.
- This is still in production, so there is still much to do!

# Common problems

1. `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

Ensure that Docker Desktop is *running first* prior to using any docker-compose (or any other related) commands

2. `Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 -> 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use`

Ensure that whichever applications are running on port 5432, cease to while the program runs. 

If you are on a Unix/Linux-like system, you can use:

```
netstat -tuln | grep <port_number>
```

For windows:

```
tasklist /FI "PID eq <PID>"
```

to figure out what is running on that port and terminate that process.



