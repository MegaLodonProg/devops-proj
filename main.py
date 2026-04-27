from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from datetime import date
from contextlib import asynccontextmanager

# Подключение к БД через переменные окружения
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "money"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "secret")
    )

# Инициализация таблицы
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            amount FLOAT,
            category VARCHAR(100),
            card_name VARCHAR(100),
            date DATE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Money Manager API", lifespan=lifespan)

# Модель для запроса
class Transaction(BaseModel):
    amount: float
    category: str
    card_name: str

# Добавить транзакцию
@app.post("/transaction")
def add_transaction(transaction: Transaction):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (amount, category, card_name, date) VALUES (%s, %s, %s, %s)",
        (transaction.amount, transaction.category, transaction.card_name, date.today())
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "ok"}

# Получить статистику
@app.get("/stats")
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT card_name, SUM(amount) FROM transactions GROUP BY card_name")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"stats": [{"card": row[0], "total": row[1]} for row in rows]}

@app.get("/")
def root():
    return {"message": "Money Manager API"}