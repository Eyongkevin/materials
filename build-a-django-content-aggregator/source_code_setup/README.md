# CONTENT AGGREGATOR
This is a project build on Django 


## Set up
This details the set up process for this project 
### Clone this project
### Set up a virtual environment 
`cd` into this project directory, create and activate a virtual environment

` python -m venv .venv`

` source .venv/bin/activate`

### Install dependencies 
`pythion -m pip install -r requirements.txt`

### Start Server
`python manage.py runserver`

Open http://127.0.0.1:8000/ to view the application

## Podcasts Model
Here we are going to be designing the podcasts model. Here are some few suggestions from the original article

```text
As a user, I would like to:

  - Know the title of an episode
  - Read a description of the episode
  - Know when an episode was published
  - Have a clickable URL so I can listen to the episode
  - See an image of the podcast so I can scroll to look
    for my favorite podcasts
  - See the podcast name

As a developer, I would like to:

  - Have a uniquely identifiable attribute for each episode
    so I can avoid duplicating episodes in the database
```

Some suggestions are
```text
As a user, I would like to:

 - Know the host of an episode
 - See the guests for each episodes if present.
 - Know the duration of the episode
 - See any tags about the episode if available.
```