format:
	black .

lint:
	flake8 --ignore E501 .

open-home-page:
	python test_menu_page.py > test.html && open test.html

open-recipes-page:
	python test_recipes_page.py > test.html && open test.html

deploy:
	chalice deploy

