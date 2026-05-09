#!/usr/bin/env python3
import requests
import sys
import json

BASE_URL = "http://localhost:8000"

def add_transaction(amount, category, card_name):
    url = f"{BASE_URL}/transaction"
    data = {
        "amount": float(amount),
        "category": category,
        "card_name": card_name
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Добавлено: {amount}р | {category} | карта {card_name}")
    else:
        print(f"Ошибка: {response.text}")

def show_stats():
    url = f"{BASE_URL}/stats"
    response = requests.get(url)
    if response.status_code == 200:
        stats = response.json()["stats"]
        print("\nСтатистика по картам:")
        for stat in stats:
            print(f"   {stat['card']}: {stat['total']}р")
    else:
        print(f"❌ Ошибка: {response.text}")

def show_help():
    print("""
Money Manager CLI

Использование:
  python cli.py add <сумма> <категория> <карта>
  python cli.py stats

Примеры:
  python cli.py add 500 кофе тинькофф
  python cli.py add 1200 продукты сбер
  python cli.py stats
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "add" and len(sys.argv) == 5:
        add_transaction(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "stats":
        show_stats()
    else:
        show_help()