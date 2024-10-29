format:
	black .

lint:
	flake8 --ignore E501 .

open-home-page:
	python test.py > test.html && open test.html

deploy:
	chalice deploy

