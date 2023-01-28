
# DevOps Experts Course - Docker HW

Multiservice application using docker-compose with MySQL and Python

## Installations:
```
create docker-compose.yml locally on your machine using context below:
Please choose require $BUILD_NUMBER from docker-hub
```
    version: "3.8"
    services:
      database:
        image: amirhazan/devops_experts_docker_hw_one:db_app_ver_$BUILD_NUMBER
      python:
        image: amirhazan/devops_experts_docker_hw_one:py_app_ver_$BUILD_NUMBER
        links:
          - database
        depends_on:
          - database 

## Start docker-compose:
    docker-compose --env-file proj_vars/proj_vars.env --file docker-compose.yml up

## Authors:

- [@amir-hazan](https://www.github.com/amir-hazan)
