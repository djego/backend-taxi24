init:
	cp taxi24/env.example taxi24/.env
	docker-compose -f compose/docker-compose.yaml build
	docker-compose -f compose/docker-compose.yaml run api python manage.py makemigrations
	docker-compose -f compose/docker-compose.yaml run api python manage.py migrate

serve:
	docker-compose -f compose/docker-compose.yaml up

bash:
	docker-compose -f compose/docker-compose.yaml run api bash