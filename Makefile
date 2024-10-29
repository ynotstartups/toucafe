format:
	black .

lint:
	flake8 --ignore E501 .

deploy:
	chalice deploy
