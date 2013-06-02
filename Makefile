all: tests
tests:
	export PYTHONPATH=.
	coverage run manage-testing.py test meetups companies accounts --settings=pygraz_website.settings.testing
	coverage report --include='pygraz_website*' --omit='*migrations*','*admin.py','*settings*'
