## How to run without Docker compose


## How to run with Docker compose

```bash
 docker compose up --build
```
## components
| Endpoint | Method | Description
| --- | --- | --- | 
| http://localhost:8000 | POST/GET | FastApi
| http://localhost:15672   | GET  | RabbitMQ monitor. User: guest ,Password: guest.
| http://localhost:5556   | GET  | Flower
