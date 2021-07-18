FIG=docker-compose
NAME=djangod
RUN=$(FIG) run --rm
SERVICE=web
EXEC=$(FIG) exec
MANAGE=python manage.py

.DEFAULT_GOAL := help
.PHONY: help start stop reset db test tu
.PHONY: build up tty db-migrate shell createsuperuser web/built

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##
## Project setup
##---------------------------------------------------------------------------

start:          ## Install and start the project
start: build up


reset:          ## Reset the whole project
reset: stop start

tty:            ## Run django container in interactive mode
tty:
	$(RUN) /bin/bash

server:			## Run server maunaly
server:
	$(RUN) $(MANAGE)
shell:          ## Run django shell
shell:
	$(RUN) $(MANAGE) shell

dbshell:          ## Run django dbshell
dbshell:
	$(RUN) $(MANAGE) dbshell


##
## Command
##---------------------------------------------------------------------------

showcommand:	## show all personnal command
showcommand:
	$(RUN) $(MANAGE)

executecommand: ## usage: name=[command]
executecommand:
	$(RUN) $(SERVICE) $(MANAGE) $(name)

##
## Database
##---------------------------------------------------------------------------

db-migrate:     ## Migrate database schema to the latest available version
db-migrate:
	$(EXEC) $(SERVICE) $(MANAGE) migrate $(model)

db-diff:     ## Make migrations
db-diff:
	$(EXEC) $(SERVICE) $(MANAGE) makemigrations $(modelm)

db-populate:  ## Populate db
db-populate:
	$(EXEC) $(MANAGE) populate_db

db-delete:   ## delete all migrations files
db-delete:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

db-flush:
	$(RUN) $(MANAGE) flush --noinput

clean-pyc:	## Clean python cache
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	


##
## Internal rules
##---------------------------------------------------------------------------

build:
	$(FIG) build

up:	## Start project container
	$(FIG) up

stop: ## Stop project container
	$(FIG) down

app:   ## make django app appname=[name]
app:
	$(EXEC) $(SERVICE) bash -c "cd apps && django-admin startapp $(appname)"

appermission:	## make django app with user right appname=[name]
appermission: app
	sudo chown -R ${USER}:${USER} ./apps/$(appname)

createsuperuser:	## Create Django super user
createsuperuser:
	$(RUN) $(SERVICE) $(MANAGE) createsuperuser"

project:	## Make django project with apps and data folders
project:
	$(RUN) $(SERVICE) django-admin startproject $(NAME) .
	mkdir apps
	sudo chown -R ${USER}:${USER} ./data

permissions:	## Give current user right on project
permissions:
	sudo chown -R ${USER}:${USER} ./$(NAME)

show-host:	## Allowed Host: Copy / Paste this line on init project 
show-host:
	@echo ALLOWED_HOSTS = [\"0.0.0.0\", \"127.0.0.0\", \"localhost\"]

userproject: project permissions show-host

# take params to choose witch project 