test:
	pip install --upgrade coveralls
	coverage run --source=. -m pytest test/
	coverage report
	coverage lcov
	coveralls

.PHONY: test
