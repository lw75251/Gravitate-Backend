# Gravitate Backend

[![Build Status](https://travis-ci.com/billyrrr/gravitate-backend.svg?token=V7MxKCogppX3CT7QjvhV&branch=master)](https://travis-ci.com/billyrrr/gravitate-backend)
[![Coverage Status](https://coveralls.io/repos/github/billyrrr/gravitate-backend/badge.svg?branch=master&t=QGfp9V)](https://coveralls.io/github/billyrrr/gravitate-backend?branch=master)

## Summary
From looking through hundreds of posts in Facebook carpooling groups to spending an unreasonable amount of money on rideshare applications such as Uber and Lyft, finding reliable and affordable transportation to Los Angeles International Airport (LAX) from San Diego can be a nightmare for students looking to return home during school breaks. International students attending UCSD often choose to fly home from LAX instead of San Diego International Airport (SAN) due to the vast difference in airfare, and must decide between largely inefficient modes of transportation such as taking the train or finding rideshare drivers who are willing to make the long trip to the airport. In addition, current rideshare services such as Uber and Lyft do not offer options to carpool with others who are also traveling long distances. To accommodate for these issues our Android application “Gravitate” will provide a platform for users to group up with each other, coordinate long-distance trips to the airport, and split the cost efficiently among the group.

## Gravitate Timeline 

### Winter 2019
- Joined Divergent Engineering 
- Member list

    - Amy Li

    - David Nong

    - Leon Wu

    - Michael Askndafi

    - Zixuan Rao

### Fall 2018

- Developed as CSE110 course project 

- Member list

    - David Alexander - Project Manager

    - Lauren Chang - Business Analyst

    - Jason Chau - Senior System Analyst

    - Kenneth Hua - User Experience and Interface Specialist

    - Sam Huang - Quality Assurance Lead

    - Andrew Kim - Database Specialist

    - David Nong - Algorithm Specialist
    
    - Billy Rao - Lead Software Architect
    
    - Tyler Song - Algorithm Specialist

    - Leon Wu - Lead Software Developer


## Run the server 
The back end should be deployed in Google App Engine Flexible Environment Python. Make sure 
that App Engine and Firebase are in the same project before proceeding to step 1. 
### Step 1: Firebase Service Account Json
Retrieve Firebase Service Account JSON from Firebase, and set the JSON path and App name
correctly in config.py 
### Step 2: Run Main Scripts
Run main_scripts.py in command lines to generate LAX location and events in the connected 
Firebase Firestore. 
### Step 3: Deploy to Google App Engine
1. Set local project-id to the correct Firebase project with 
```gcloud config set project gravitate-dev ``` (exchange gravitate-dev to desired project-id). 

2. Navigate to directory with app.yaml, run 
```gcloud beta app deploy``` (beta keyword is optional here, we want to add it for better 
debug support in the google cloud console)


## Develop Locally

Since the backend project is hosted by Google App Engine Flexible Environment Python, it will take a long set up process to test app locally. Therefore, you may work with submodules that can be tested without exposing to server, and skip all setup process other than "Setup Repository"  and https://cloud.google.com/python/setup. Wheareas, if you want to develop the layers that communicates with client via REST API. You should set up the environment for such testing. 

### Setup Local Environment

Follow the document provided by Google (we are working with Python 3.7/3.6)

Login 

	Username: cse110vibe@gmail.com
	
	Password: miwsag-syWsej-8jydpy

https://cloud.google.com/appengine/docs/flexible/python/quickstart

Make sure that you have deployed and run Hello World on your local machine before moving on to the next steps. DO NOT DEPLOY Hello World to cse110-vibe project, or create a new project to deploy to. 

# Organizing Modules
[Useful Guide](https://stackoverflow.com/questions/12578908/separation-of-business-logic-and-data-access-in-django/12579490#12579490)

## Generate Docs

(TODO: change Makefile)
``` 
sphinx-apidoc -o source/ ../gravitate
python3 -msphinx -b html docs/source docs/build
```

## Reference

<https://help.github.com/articles/cloning-a-repository/#platform-windows>

