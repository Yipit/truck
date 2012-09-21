init:
	python setup.py develop
	pip install -r requirements.txt

test:
	nosetests tests/test_loader.py
