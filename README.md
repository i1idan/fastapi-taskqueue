# fastapi-taskqueue

## How to run 

```bash
 docker compose up --build
```

## Swagger 

http://localhost:8000/docs


## components
| Endpoint | Method | Description
| --- | --- | --- | 
| http://localhost:8000 | POST/GET | FastAPI
| http://localhost:15672   | GET  | RabbitMQ monitor. User: guest ,Password: guest.
| http://localhost:5556   | GET  | Flower
