import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'giguerr231',
    'password': 'Miashs2025', 
    'database': 'tabistats'
}

def fetch_and_store_rates():
    # On demande le Yen (Japon), le Dollar (USA) et la Roupie (Bali)
    target_currencies = "JPY,USD,IDR"
    
    try:
        url = f"https://api.frankfurter.app/latest?from=EUR&to={target_currencies}"
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        rates = response.json()['rates']
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Erreur API : {e}")
        return

    db = None
    cursor = None
    
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        sql = """
        INSERT INTO currency_rates (currency_from, currency_to, exchange_rate)
        VALUES (%s, %s, %s)
        """

        # On boucle sur chaque devise récupérée pour l'insérer en base
        for currency, rate in rates.items():
            try:
                cursor.execute(sql, ("EUR", currency, rate))
                print(f"[{datetime.now()}] Succès : 1 EUR = {rate} {currency}")
            except mysql.connector.IntegrityError:
                print(f"[{datetime.now()}] Info : Taux EUR -> {currency} déjà enregistré aujourd'hui.")

        db.commit()

    except Error as e:
        print(f"[{datetime.now()}] Erreur SQL : {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()

if __name__ == "__main__":
    fetch_and_store_rates()