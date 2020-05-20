# Similarity Check API



[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)]

Basic Similarity Check API based on SpaCy to calculate ratio between two texts.

  - User Token based to allow the usage of the API.
  - Calculates the ratio of how similar the two texts are.
  - Refills by the admin

### Tech

Similarity Check API uses a the following libraries:

* [SpaCy] - SpaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python.
* [flask_restful] - Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs. 
* [pymongo] - MongoDB is a document database with the scalability and flexibility that works with the querying and indexing.
* [bcrypt] - The bcrypt hashing function allows us to build a password security platform that can scale with computation power. 
* [Flask] - Flask is a web framework. It provides tools, libraries and technologies that allow to build a web application.
* [Docker] -A Docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application.



### Installation

Similarity Check requires Docker and Docker Compose to run.

Install the dependencies.
Docker and Docker Compose from [DOCKER](https://docs.docker.com/compose/install/)
For [MongoDB](https://docs.mongodb.com/)


### To run the API:

```sh
$ docker-compose build
$ docker-compose up
```



License
Freeware
----






