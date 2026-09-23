# ✈️ TabiStats* - Pipeline Data & Dashboard Analytique

TabiStats est un projet full-stack d'analyse de données conçu pour automatiser le suivi budgétaire d'un voyage (billets d'avion et taux de change). Il extrait les données tarifaires, les stocke dans une base de données relationnelle locale et les restitue via un tableau de bord interactif.

Ce projet démontre des compétences en **Data Extraction (Python)**, **Modélisation de base de données (MySQL)**, **Développement d'API (PHP)** et **Data Visualisation (JavaScript/Chart.js)**.

## 🛠️ Architecture technique

*   **Back-end / Data Collection :** Python (Requests, SerpApi, MySQL Connector)
*   **Base de données :** MySQL (hébergée localement via Laragon)
*   **API :** PHP (PDO)
*   **Front-end :** HTML5, CSS3, JavaScript (Chart.js)

## 🚀 Installation et Configuration

Pour faire tourner ce projet sur votre machine locale, suivez les étapes ci-dessous.

### 1. Prérequis environnementaux
*   **Python 3.x** installé.
*   Un environnement serveur local comme **[Laragon](https://laragon.org/)** (recommandé), WAMP ou XAMPP pour exécuter PHP et MySQL.

### 2. Configuration de la base de données (Exemple avec Laragon)
1. Lancez Laragon et démarrez les services **Apache** et **MySQL**.
2. Ouvrez un gestionnaire de base de données (comme **HeidiSQL**, intégré à Laragon).
3. Créez une nouvelle base de données nommée `tabistats`.
4. Créez un utilisateur MySQL dédié à l'application.
5. Exécutez le script fourni `init_db.sql` dans l'onglet Requête pour créer les tables (`currency_rates`, `flight_prices`, `accommodations`) et la vue analytique (`v_daily_flight_trends`).

### 3. Gestion des clés d'API (Données)
Ce projet utilise deux sources de données externes :
*   **Google Flights via SerpApi :** Créez un compte gratuit sur [SerpApi](https://serpapi.com/) pour obtenir une clé d'API (100 requêtes gratuites/mois). Cette API sert à extraire les tarifs des vols.
*   **Frankfurter API :** Utilisée pour récupérer les taux de change mis à jour. Cette API est publique et ne requiert aucune clé.

### 4. Sécurisation des identifiants
Les identifiants ne sont pas stockés dans le code source. Vous devez créer vos propres fichiers de configuration à partir des exemples fournis :

*   **Pour Python :** Copiez le fichier `.env.example` et renommez-le en `.env`. Insérez-y vos accès MySQL et votre clé SerpApi.
    ```env
    DB_USER=votre_utilisateur
    DB_PASS=votre_mot_de_passe
    SERPAPI_KEY=votre_cle_api_serpapi
    ```
*   **Pour PHP :** Copiez le fichier `db_config.example.php` et renommez-le en `db_config.php`.
    ```php
    <?php
    $db_user = 'votre_utilisateur';
    $db_pass = 'votre_mot_de_passe';
    ?>
    ```

### 5. Installation des dépendances Python
Ouvrez un terminal dans le dossier du projet et installez les bibliothèques requises :
```bash
pip install -r requirements.txt
 ```

### 6. Utilisation
Ouvrez votre terminal puis lancer ces fonction:
```bash
python fetch_rates.py
python fetch_flights_2.py
 ```

ATTENTION fetch_rates.py ne prends aucune requête.
En revanche fetch_flights_2.py en consomme en viront 27-30 si tout les billets ont un prix (si un billets na pas de prix alors elle ne prends pas de requête)

Visualisation : Placez le dossier du projet dans le répertoire racine de votre serveur local (ex: C:\laragon\www\tabistats).

Ouvrez votre navigateur et accédez à http://localhost/tabistats/ pour interagir avec le tableau de bord.

### Note du créateur
  Le but de ce projet est d'analyser l'évolution des prix des billets d'avion afin de déterminer la période optimale d'achat. L'objectif concret est d'optimiser le budget de mon prochain voyage de 3 semaines au Japon (prévu pour l'été 2027), un pays qui m'a fasciné lors d'un précédent séjour de 16 jours.

(Pour l'anecdote, "Tabi" signifie "voyage" en japonais).
