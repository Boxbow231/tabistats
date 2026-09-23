import os
import time
from datetime import datetime, date, timedelta
import mysql.connector
from mysql.connector import Error
from serpapi import GoogleSearch

from dotenv import load_dotenv
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

DB_CONFIG = {
    'host': 'localhost',
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'database': 'tabistats'
}

DESTINATIONS = ["KIX", "NRT", "HND", "JFK", "LAX", "DPS"]

def get_exact_saturdays(year, months):
    saturdays = []
    for month in months:
        for day in range(1, 32):
            try:
                d = date(year, month, day)
                if d.weekday() == 5:  # 5 correspond au samedi
                    saturdays.append(d)
            except ValueError:
                break  # Fin du mois atteinte
    return saturdays

def fetch_flight_price(destination, departure_date, return_date, cursor, db):
    outbound_str = departure_date.strftime("%Y-%m-%d")
    return_str = return_date.strftime("%Y-%m-%d")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] CDG -> {destination} ({outbound_str} au {return_str})")

    params = {
        "engine": "google_flights",
        "departure_id": "CDG",
        "arrival_id": destination,
        "outbound_date": outbound_str,
        "return_date": return_str,
        "currency": "EUR",
        "hl": "fr",
        "api_key": SERPAPI_KEY
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        print(f"  -> Erreur API : {e}")
        return

    best_flights = results.get("best_flights", [])
    other_flights = results.get("other_flights", [])
    top_flight = best_flights[0] if best_flights else (other_flights[0] if other_flights else None)

    if not top_flight:
        print("  -> Aucun vol ouvert à la vente pour cette date.")
        return

    price = top_flight.get("price", 0)
    airlines_list = top_flight.get("airlines", ["Inconnue"])
    airline = airlines_list[0] if airlines_list else "Multiple"

    sql = """
    INSERT INTO flight_prices (
        departure_date, return_date, origin_airport, destination_airport,
        airline, price_eur, duration_outbound_mins, duration_return_mins,
        stops_outbound, stops_return
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valeurs = (
        outbound_str, return_str, "CDG", destination,
        airline, price, 0, 0, 0, 0
    )

    try:
        cursor.execute(sql, valeurs)
        db.commit()
        print(f"  -> Succès : {price}€ enregistré.")
    except Error as e:
        print(f"  -> Erreur SQL : {e}")

def main():
    target_year = 2027
    target_months = [7, 10]  # Uniquement les mois 7 (Juillet) et 10 (Octobre)
    saturdays = get_exact_saturdays(target_year, target_months)

    print(f"Dates de départ ciblées : {[s.strftime('%Y-%m-%d') for s in saturdays]}")

    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        for dest in DESTINATIONS:
            for sat in saturdays:
                return_sat = sat + timedelta(days=14)
                fetch_flight_price(dest, sat, return_sat, cursor, db)
                time.sleep(1)  # Pause pour éviter de bloquer l'API

    except Error as e:
        print(f"Erreur connexion MySQL : {e}")
    finally:
        if 'cursor' in locals() and cursor: cursor.close()
        if 'db' in locals() and db.is_connected(): db.close()

if __name__ == "__main__":
    main()