include .env

start:
	docker compose up

stop:
	docker compose down --remove-orphans

purge:
	docker compose down -v --remove-orphans

build:
	docker compose build

fresh: build purge start

run: stop start
