all: install_deps test

export PYTHONPATH:=  ${PWD}:${PWD}/tests/resources
export DJANGO_SETTINGS_MODULE:= tests.settings

filename=truck-`python -c 'from truck import version; print version'`.tar.gz
install_deps:
	@pip install -r requirements.txt

test:
	@echo "running python tests..."
	@nosetests -sv --with-coverage --cover-package=truck --rednose --verbosity=2 tests
	@echo "running documentation examples..."
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: clean test publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) truck setup.py README.md COPYING
	@echo "DONE!"

publish:
	@python setup.py sdist register upload
