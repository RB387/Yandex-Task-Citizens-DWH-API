lint:
	black citizens_dwh_api && \
	black tests && \
	pylint citizens_dwh_api

test:
	pytest -vv

install-dev:
	pip install -r requirements-dev.txt

install:
	pip install -r requirements.txt

debug:
	docker rm -f dev_mongo || echo "Mongo container was not found"
	docker-compose run -d --service-ports --name dev_mongo dev_mongo
	docker exec -it dev_mongo ./usr/local/bin/initiate_replica.sh --dev