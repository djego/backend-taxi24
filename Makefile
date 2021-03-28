compose = docker-compose -f compose/docker-compose.yaml

init:
	cp taxi24/env.example taxi24/.env
	$(compose) build
	$(compose) run api python manage.py makemigrations
	$(compose) run api python manage.py migrate
	$(compose) run api python manage.py loaddata core users

serve:
	$(compose) up

bash:
	$(compose) run api bash

test:
	$(compose) run api python manage.py test

lint:
	$(compose) run api pylint taxi24 core --ignore=migrations --disable=duplicate-code

coverage:
	$(compose) run api coverage run --source='.' manage.py test
	$(compose) run api coverage report

destroy:
	$(compose) down