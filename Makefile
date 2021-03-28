compose = docker-compose -f compose/docker-compose.yaml

init:
	cp taxi24/env.example taxi24/.env
	$(compose) build
	make migrate
	$(compose) run api python manage.py loaddata core users

migrate:
	$(compose) run api bash -c "python manage.py makemigrations \
		&& python manage.py migrate"

serve:
	$(compose) up

bash:
	$(compose) run api bash

test:
	$(compose) run api python manage.py test

lint:
	$(compose) run api pylint taxi24 core --ignore=migrations --disable=duplicate-code

coverage:
	$(compose) run api bash -c "coverage run --source='.' manage.py test && coverage report"

destroy:
	$(compose) down