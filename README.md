# csRU
This will be a course manager for the BA/BS Computer Science Track at Rutgers University New-Brunswick. It will be a dedicated RestAPI that has all the available courses, professors, and sections of a class in the desired semester. In will also have a professor rating from the website: RateMyProfessor.com

# Getting started
First you would need to have docker desktop downloaded [here](https://www.docker.com/products/docker-desktop/)

## Docker Desktop
The API is containerized in these docker containers so that you will not need to worry about downloading dependencies.

You need to trust the third party application, and signing in is optional. You can continue without signing in.

### Common problems

1. `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

Ensure that Docker Desktop is *running first* prior to using any docker-compose (or any other related) commands

2. Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 -> 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use

Ensure that whichever applications are running on port 5432, cease to while the program runs. 

If you are on a Unix/Linux-like system, you can use:

```
netstat -tuln | grep <port_number>
```

For windows:

```
tasklist /FI "PID eq <PID>"
```


