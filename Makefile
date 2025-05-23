PORT ?= 10000

install:
	pip install -r requirements.txt

check:
	uv run ruff check .

check-fix:
	uv run ruff check --fix .

start:
	python manage.py runserver 0.0.0.0:$(PORT)

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)

build:
	./build.sh

sync:
	uv sync

migrate:
	python manage.py makemigrations && python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input

translate-compile:
	django-admin compilemessages

translate-makemessages:
	django-admin makemessages -l ru

tests:
	python manage.py test

