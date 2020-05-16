INTEGRATION_DIR = test/integration
GENERATED_DOCKERFILE=$(INTEGRATION_DIR)/Dockerfile.generated
TEMPLATE_DOCKERFILE=$(INTEGRATION_DIR)/Dockerfile.template
UNIT_DIR = test/unit
TEST_DOCKER_IMAGE=utt-integration
SOURCE_DIRS=utt test
PYPI_REPO_NAME=pypi
PYPI_JSON_API_URL=https://pypi.org/pypi
PYPI_LEGACY_API_URL=https://upload.pypi.org/legacy/
TEST_PYPI_REPO_NAME=test-pypi
TEST_PYPI_JSON_API_URL=https://test.pypi.org/pypi
TEST_PYPI_LEGACY_API_URL=https://test.pypi.org/legacy/

.PHONY: build
build:
	poetry build

.PHONY: bootstrap
bootstrap: bootstrap.install

.PHONY: bootstrap.install
bootstrap.install:
	poetry install

.PHONY: check
check: lint test

.PHONY: ci.bootstrap
ci.bootstrap:
	pip install poetry
	make bootstrap

.PHONY: ci.configure-poetry
ci.configure-poetry:
	poetry config repositories.$(PYPI_REPO_NAME) $(PYPI_LEGACY_API_URL)
	@poetry config pypi-token.$(PYPI_REPO_NAME) $(PYPI_API_TOKEN)
	poetry config repositories.$(TEST_PYPI_REPO_NAME) $(TEST_PYPI_LEGACY_API_URL)
	@poetry config pypi-token.$(TEST_PYPI_REPO_NAME) $(TEST_PYPI_API_TOKEN)
	poetry config --list

.PHONY: ci.publish.pypi
ci.publish.pypi:
	python scripts/publish.py $(PYPI_REPO_NAME) $(PYPI_JSON_API_URL)

.PHONY: ci.publish.test-pypi
ci.publish.test-pypi:
	python scripts/publish.py $(TEST_PYPI_REPO_NAME) $(TEST_PYPI_JSON_API_URL)

.PHONY: ci.update-version-in-pyproject
ci.update-version-in-pyproject:
	python scripts/update_version_in_pyproject.py $(CHANGELOG_FILENAME)
	python scripts/update_version_txt.py utt/version.txt

.PHONY: clean
clean:
	rm -rf dist
	rm -f $(INTEGRATION_DIR)/*.whl

.PHONY: format
format:
	poetry run black $(SOURCE_DIRS)
	poetry run isort --recursive $(SOURCE_DIRS)

.PHONY: lint
lint: lint.format  # lint.types

.PHONY: lint.format
lint.format:
	poetry run flake8 $(SOURCE_DIRS)
	poetry run isort --check-only --diff --ignore-whitespace --recursive --quiet $(SOURCE_DIRS)
	poetry run black --check --diff $(SOURCE_DIRS)

#.PHONY: lint.types
#lint.types:
#	poetry run mypy $(SOURCE_DIRS)

.PHONY: test
test: test.unit test.integration

.PHONY: test.unit
test.unit:
	poetry run pytest --verbose

.PHONY: test.integration
test.integration: clean build
	cp dist/utt-*-py3-none-any.whl $(INTEGRATION_DIR)

	python -c 'import sys; print(f"FROM python:{sys.version_info.major}.{sys.version_info.minor}-buster")' > $(GENERATED_DOCKERFILE)
	cat $(TEMPLATE_DOCKERFILE) >> $(GENERATED_DOCKERFILE)
	docker build --tag $(TEST_DOCKER_IMAGE) --file $(GENERATED_DOCKERFILE) $(INTEGRATION_DIR)
	docker run --rm $(TEST_DOCKER_IMAGE) $(INTEGRATION_CMD)
