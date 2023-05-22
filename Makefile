build: install migrate collectstatic populate_table

install:
	cd backend/ && poetry install --quiet

migrate:
	cd backend/ && poetry run python manage.py migrate

collectstatic:
	cd backend/ && poetry run python manage.py collectstatic

populate_table:
	cd backend/ && poetry run python manage.py populate_currencies_table

run:
	cd backend/ && poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: install migrate collectstatic populate_table run
