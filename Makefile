.PHONY: test validate docs
.PHONY: docs\:install docs\:dev docs\:up docs\:down
.PHONY: hooks\:install hooks\:test

test:
	python3 .github/scripts/test-marketplaces.py

validate:
	python3 .github/scripts/validate.py
	claude plugin validate --strict .
	claude plugin validate --strict plugins/tab

docs:
	npm --prefix docs run build

docs\:install:
	npm --prefix docs ci

docs\:dev:
	npm --prefix docs run dev

docs\:up:
	docker compose -f docs/compose.yaml up --build

docs\:down:
	docker compose -f docs/compose.yaml down

hooks\:install:
	hooks/install.sh

hooks\:test:
	hooks/test.sh
