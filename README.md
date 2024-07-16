
# Features

Swagger documentation:

![swagger documentaion](README%20assets/swagger%20documentaion.png)

Rule creation:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/rules/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "urls": ["https://example.com/"],
  "methods": ["GET"],
  "requests": 10,
  "refresh_rate": 30
}'
[{"url":"https://example.com/","method":"GET","refresh_rate":30,"requests":10}]
```

Access validation:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/validate/?url=https%3A%2F%2Fexample.com%2F&method=GET&ip_address=0.0.0.0' \
  -H 'accept: application/json' \
  -d ''
{"is_allowed":true,"requests_left":9,"seconds_to_next_refresh":30}

curl -X 'POST' \
  'http://127.0.0.1:8000/v1/validate/?url=https%3A%2F%2Fexample.com%2F&method=GET&ip_address=0.0.0.0' \
  -H 'accept: application/json' \
  -d ''
{"is_allowed":true,"requests_left":8,"seconds_to_next_refresh":28.917512893676758}

...

curl -X 'POST' \
  'http://127.0.0.1:8000/v1/validate/?url=https%3A%2F%2Fexample.com%2F&method=GET&ip_address=0.0.0.0' \
  -H 'accept: application/json' \
  -d ''
{"is_allowed":false,"requests_left":0,"seconds_to_next_refresh":24.325567960739136}
```

Analytics:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/bucket_analytics/data/json' \
  -H 'accept: application/json'
[{"url":"https://example.com/","method":"GET","ip_address":"0.0.0.0","timestamp":1721105457.358816,"was_allowed":true}]
```

# Launching

1. `git clone`
2. `cp .env.sample .env` and edit if necessary
3. `docker compose up`
4. Read docs at `localhost:8080`

# FAQ

> Why are backend and frontend separate?

This project is my assignment for 'distributed systems' course at university and having at least 3 services was required
