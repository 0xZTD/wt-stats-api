docker-api-build:
	docker build -t zeth5/wt-stats:dev -f wt_stats_api/Dockerfile wt_stats_api/
	docker push zeth5/wt-stats:dev

api-run:
	docker run --rm -p 8650:8650 zeth5/wt-stats:dev

docker-bot-build:
	docker build -t zeth5/wt-stats-bot:dev -f wt_tg_bot/Dockerfile wt_tg_bot/

bot-run:
	docker run --rm --env-file wt_tg_bot/.env zeth5/wt-stats-bot:dev