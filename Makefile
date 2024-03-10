check-tools: ## Check and install package management dependencies
	pip install pip==24.0 pip-tools==7.4.0

compile: check-tools ## Check and compile project dependencies (check-tools will be performed automatically)
	pip-compile --strip-extras --resolver=backtracking requirements.in

upgrade-all-packages: ## Upgrades all dependency packages
	pip-compile --strip-extras --resolver=backtracking requirements.in --upgrade

install: check-tools ## Installs project dependencies (check-tools will be performed automatically)
	pip-sync requirements.txt

sync: compile install ## Synchronizes project dependencies (compile and install will be performed automatically)

run-local:
	docker compose -f docker-compose-local.yml up --build

run-dev:
	docker compose -f docker-compose-dev.yml up --build -d
