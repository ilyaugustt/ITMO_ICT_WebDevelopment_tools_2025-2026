docker compose down
docker compose build --no-cache celery_worker parser
docker compose up


curl -X POST "http://localhost:8002/parse/async" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

curl "http://localhost:8002/parse/task/856cb9d1-4eac-48a9-8082-ba92ed9832f9"
