.PHONY: test validate

test:
	python3 .github/scripts/test-marketplaces.py

validate:
	python3 .github/scripts/validate.py
	claude plugin validate --strict .
	claude plugin validate --strict plugins/tab
