start:
	@docker-compose -f docker/docker-compose.yaml up -d opensearch opensearch-dashboards grafana

build:
	@docker-compose -f docker/docker-compose.yaml build

cur:
	@docker-compose -f docker/docker-compose.yaml run cur

stop:
	@docker-compose -f docker/docker-compose.yaml down -v

logs:
	@docker-compose -f docker/docker-compose.yaml logs -f

status:
	@docker-compose -f docker/docker-compose.yaml ps

all: build start cur
