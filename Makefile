build:
	docker build -t asciify_service .

service:
	docker run -it --rm -p 8080:8080 asciify_service:latest

test:
	docker run -it --entrypoint python asciify_service:latest manage.py test

format:
	poetry run black ./