import os
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from serpapi import GoogleSearch

SERPAPI_KEY = "2ab455ebf6cd672fc7bb24430283fd6f52bcd33f86bf7fd5ba99e2b82695d838"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'giguerr231',
    'password': 'Miashs2025', 
    'database': 'tabistats'
}

def fetch_progressive_flight():
    # On définit l'aéroport que l'on veut interroger aujourd'hui (ex: KIX pour le Japon)
    destination = "KIX"
    
    # Stratégie intelligente : on cible un vol prévu exactement dans 6 mois (ou 330 jours)
    # Chaque jour, la date visée avancera d'un jour, balayant ainsi toute l'année progressivement.
    target_departure = datetime.now() + timedelta(days=200) # Par exemple dans 200 jours
    target_return = target_departure + timedelta(days=14)   # 2 semaines de voyage
    
    outbound_str = target_departure.strftime("%Y-%m-%d")
    return_str = target_return.strftime("%Y-%m-%d")

    print(f"[{datetime.now()}] Analyse du vol CDG -> {destination} pour le départ du {outbound_str}...")

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
        print(f"Erreur SerpApi : {e}")
        return

    best_flights = results.get("best_flights", [])
    other_flights = results.get("other_flights", [])
    top_flight = best_flights[0] if best_flights else (other_flights[0] if other_flights else None)

    if not top_flight:
        print("Aucun vol trouvé pour cette date.")
        return

    price = top_flight.get("price", 0)
    airlines_list = top_flight.get("airlines", ["Inconnue"])
    airline = airlines_list[0] if airlines_list else "Multiple"

    # Connexion et insertion SQL
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        sql = """
        INSERT INTO flight_prices (
            departure_date, return_date, origin_airport, destination_airport,
            airline, price_eur, duration_outbound_mins, duration_return_mins,
            stops_outbound, stops_return
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Note: on récupère les durées/escales de façon simplifiée ici
        valeurs = (
            outbound_str, return_str, "CDG", destination,
            airline, price, 0, 0, 0, 0
        )

        cursor.execute(sql, valeurs)
        db.commit()
        print(f"Succès : Prix de {price}€ enregistré pour le départ du {outbound_str}.")

    except Error as e:
        print(f"Erreur SQL : {e}")
    finally:
        if 'cursor' in locals() and cursor: cursor.close()
        if 'db' in locals() and db.is_connected(): db.close()

if __name__ == "__main__":
    fetch_progressive_flight()