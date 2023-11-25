SHELL := /bin/bash

.PHONY: run clean venv

build: .env docker-compose.yml
	@docker-compose up --build -d
	
rebuild: #rebuild container
	@docker-compose up --force-recreate --build -d

up: #start container
	@docker-compose up -d

stop: #stop container
	@docker-compose stop	

restart: #restart container
	@docker-compose restart

.env:
	@cp docker/bot/.env.dev docker/bot/.env

docker-compose.yml:
	@cp docker-compose.yml.dev docker-compose.yml

install-venv:
	@python3.11 -m venv venv
	@source venv/bin/activate && pip install -r docker/bot/requirements.txt
	@source venv/bin/activate && pip install -r docker/api/requirements.txt

run-watcher:
	@source venv/bin/activate && python3.11 src/watchdog_script.py

clean-venv:
	@echo "Cleaning up"
	@rm -rf venv
	@echo "Cleaned up"

clean-docker:
	@docker-compose down --rmi all --volumes --remove-orphans
