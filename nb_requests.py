import requests

API_KEY = "2ab455ebf6cd672fc7bb24430283fd6f52bcd33f86bf7fd5ba99e2b82695d838"
url = f"https://serpapi.com/account?api_key={API_KEY}"

try:
    reponse = requests.get(url).json()
    utilisees = reponse.get('this_month_usage', 0)
    total = reponse.get('searches_per_month', 100)
    
    print(f"Requêtes utilisées ce mois-ci : {utilisees} / {total}")
except Exception as e:
    print(f"Impossible de vérifier le quota : {e}")