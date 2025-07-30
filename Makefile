docker-api:
	docker build -t zeth5/wt-stats:dev -f wt_stats_api/Dockerfile wt_stats_api/
	docker push zeth5/wt-stats:dev

docker-api-build:
	docker build -t zeth5/wt-stats:dev -f wt_stats_api/Dockerfile wt_stats_api/

api-run:
	docker run --rm -p 8650:8650 zeth5/wt-stats:dev