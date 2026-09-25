let yenChartInstance = null;
let flightChartInstance = null;

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

const countryCurrency = {
    "Japon": "JPY",
    "USA": "USD",
    "Indonesie": "IDR"
};

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

function loadDashboardData() {
    const country = document.getElementById("countrySelect").value;
    const airport = document.getElementById("airportSelect").value;
    const date = document.getElementById("travelDate").value;
    const currency = countryCurrency[country];

    fetch(`api.php?airport=${airport}&date=${date}&currency=${currency}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) return console.error("Erreur:", data.error);
            initYenChart(data.currencies);
            initFlightChart(data.flights);
        })
        .catch(error => console.error('Erreur Fetch:', error));
}

document.addEventListener("DOMContentLoaded", () => {
    updateAirportList();
    loadDashboardData();

    document.getElementById("countrySelect").addEventListener("change", () => {
        updateAirportList();
        loadDashboardData();
    });

    document.getElementById("airportSelect").addEventListener("change", loadDashboardData);

    // Vérification du samedi
    document.getElementById("travelDate").addEventListener("change", function () {
        const selectedDate = new Date(this.value);
        if (selectedDate.getDay() !== 6) { // 6 = Samedi
            alert("Merci de sélectionner un samedi (les relevés sont uniquement basés sur les départs du samedi).");
            this.value = "2027-07-03"; // Remet une date valide par défaut
        }
        loadDashboardData();
    });

    document.getElementById("updateBtn").addEventListener("click", loadDashboardData);
});

function initYenChart(data) {
    if (yenChartInstance !== null) yenChartInstance.destroy();
    const ctx = document.getElementById('yenChart').getContext('2d');
    yenChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.date),
            datasets: [{
                label: 'Taux de change',
                data: data.map(item => item.exchange_rate),
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2, fill: true, tension: 0.3, pointRadius: 4, pointBackgroundColor: '#e74c3c'
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });
}

function initFlightChart(data) {
    if (flightChartInstance !== null) flightChartInstance.destroy();
    const ctx = document.getElementById('flightChart').getContext('2d');
    flightChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.date),
            datasets: [{
                label: 'Prix (EUR)',
                data: data.map(item => item.price_eur),
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2, fill: true, tension: 0.3, pointRadius: 4, pointBackgroundColor: '#3498db'
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: false } } }
    });
}