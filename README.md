Команды для запуска сервера
1) git clone git@github.com:husia777/task-manager.git
2) cd task-manager
3) make env
4) docker-compose up --build
5) http://localhost:8080/docs


Конфиг для локально запуска тестов
Команды можно посмотреть в Makefile

```python
class PostgresSettings(BaseSettings):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5433
    db: str = "postgres"
    driver: Literal["asyncpg", "psycopg", "psycopg2"] = "asyncpg"
```