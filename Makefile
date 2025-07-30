docker-api:
	docker build -t zeth5/wt-stats:dev -f wt_stats_api/Dockerfile .
	docker push zeth5/wt-stats:dev