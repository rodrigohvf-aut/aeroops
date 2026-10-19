const form = document.getElementById("airport-form");
const airportList = document.getElementById("airport-list");

async function loadAirports() {
    const response = await fetch("http://127.0.0.1:8000/airports");
    const data = await response.json();

    airportList.innerHTML = "";

    data.airports.forEach((airport) => {
        const item = document.createElement("li");
        item.textContent = `${airport.ident} - ${airport.name} (${airport.country})`;
        airportList.appendChild(item);
    });
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const airport = {
        ident: document.getElementById("ident").value,
        name: document.getElementById("name").value,
        country: document.getElementById("country").value,
        latitude: Number(document.getElementById("latitude").value),
        longitude: Number(document.getElementById("longitude").value),
    };

    const response = await fetch("http://127.0.0.1:8000/airports", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(airport),
    });

    if (!response.ok) {
        alert("Não foi possível cadastrar o aeroporto.");
        return;
    }

    form.reset();
    await loadAirports();
    alert("Aeroporto cadastrado com sucesso.");
});

loadAirports();

async function checkTechnicalStatus() {
    const apiStatus = document.getElementById("api-status");
    const databaseStatus = document.getElementById("database-status");
    const lastCheck = document.getElementById("last-check");

    try {
        const apiResponse = await fetch("http://127.0.0.1:8000/health");
        const databaseResponse = await fetch(
            "http://127.0.0.1:8000/health/database"
        );

        const apiData = await apiResponse.json();
        const databaseData = await databaseResponse.json();

        apiStatus.textContent = apiData.status;
        databaseStatus.textContent = databaseData.database;
        lastCheck.textContent = new Date().toLocaleString("pt-BR");
    } catch (error) {
        apiStatus.textContent = "indisponível";
        databaseStatus.textContent = "indisponível";
        lastCheck.textContent = new Date().toLocaleString("pt-BR");
    }
}

checkTechnicalStatus();

async function loadProductMetrics() {
    const airportTotal = document.getElementById("airport-total");

    const response = await fetch("http://127.0.0.1:8000/airports");
    const data = await response.json();

    airportTotal.textContent = data.airports.length;
}

loadProductMetrics();