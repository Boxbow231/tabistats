// 1. Variables pour stocker les graphiques et éviter la superposition
let yenChartInstance = null;
let flightChartInstance = null;

// 2. Dictionnaire des destinations
const destinations = {
    "Japon": [
        { code: "KIX", name: "Osaka (KIX)" },
        { code: "NRT", name: "Tokyo Narita (NRT)" },
        { code: "HND", name: "Tokyo Haneda (HND)" }
    ],
    "USA": [
        { code: "JFK", name: "New York (JFK)" },
        { code: "LAX", name: "Los Angeles (LAX)" }
    ],
    "Indonesie": [
        { code: "DPS", name: "Bali (DPS)" }
    ]
};

// Dictionnaire pour associer le pays à sa monnaie
const countryCurrency = {
    "Japon": "JPY",
    "USA": "USD",
    "Indonesie": "IDR"
};

// 3. Fonction pour mettre à jour la liste des aéroports
function updateAirportList() {
    const country = document.getElementById("countrySelect").value;
    const airportSelect = document.getElementById("airportSelect");
    
    airportSelect.innerHTML = "";
    
    destinations[country].forEach(airport => {
        const option = document.createElement("option");
        option.value = airport.code;
        option.textContent = airport.name;
        airportSelect.appendChild(option);
    });
}

// 4. Fonction pour charger les données selon les filtres
function loadDashboardData() {
    const country = document.getElementById("countrySelect").value;
    const airport = document.getElementById("airportSelect").value;
    const date = document.getElementById("travelDate").value;
    
    // On déduit la monnaie grâce au pays choisi
    const currency = countryCurrency[country];

    // On ajoute la monnaie dans l'URL
    fetch(`api.php?airport=${airport}&date=${date}&currency=${currency}`)
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                console.error("Erreur serveur:", data.error);
                return;
            }
            initYenChart(data.currencies);
            initFlightChart(data.flights);
        })
        .catch(error => {
            console.error('Erreur Fetch:', error);
        });
}

// 5. Initialisation au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    updateAirportList(); 
    loadDashboardData(); 
    
    document.getElementById("countrySelect").addEventListener("change", updateAirportList);
    document.getElementById("updateBtn").addEventListener("click", loadDashboardData);
});

// 6. Fonction pour dessiner le graphique du Yen (ou de la devise)
function initYenChart(data) {
    if (yenChartInstance !== null) {
        yenChartInstance.destroy(); // Détruit l'ancien graphique s'il existe
    }
    
    const ctx = document.getElementById('yenChart').getContext('2d');
    const labels = data.map(item => item.date);
    const values = data.map(item => item.exchange_rate);

    yenChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Taux de change',
                data: values,
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#e74c3c'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: false } }
        }
    });
}

// 7. Fonction pour dessiner le graphique des Vols
function initFlightChart(data) {
    if (flightChartInstance !== null) {
        flightChartInstance.destroy(); // Détruit l'ancien graphique s'il existe
    }
    
    const ctx = document.getElementById('flightChart').getContext('2d');
    const labels = data.map(item => item.date);
    const values = data.map(item => item.price_eur);

    flightChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Prix du billet (EUR)',
                data: values,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#3498db'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: false } }
        }
    });
}