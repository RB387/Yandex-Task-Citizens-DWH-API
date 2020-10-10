lint:
	black citizens_dwh_api && \
	black lib && \
	black tests && \
	pylint citizens_dwh_api && \
	pylint lib

test:
	pytest -vv

install-dev:
	pip install -r requirements-dev.txt

install:
	pip install -r requirements.txt