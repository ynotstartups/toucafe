format:
	black .

lint:
	flake8 --ignore E501 .

open-home-page:
	../.venv/bin/python test_menu_page.py > test.html && open test.html

open-recipes-page:
	../.venv/bin/python test_recipes_page.py > test.html && open test.html

open-gallery-page:
	../.venv/bin/python test_gallery_page.py > test.html && open test.html

deploy:
	AWS_PROFILE=personal ../.venv/bin/chalice deploy

