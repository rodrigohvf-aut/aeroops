const form = document.getElementById("airport-form");
const airportList = document.getElementById("airport-list");
const airportSearch = document.getElementById("airport-search");

let airports = [];

function showAirports() {
    const search = airportSearch.value.trim().toLowerCase();

    airportList.innerHTML = "";

    airports
        .filter((airport) =>
            [airport.ident, airport.name, airport.country].some((value) =>
                value.toLowerCase().includes(search)
            )
        )
        .forEach((airport) => {
            const item = document.createElement("li");
            const text = document.createElement("span");
            const deleteButton = document.createElement("button");

            text.textContent =
                `${airport.ident} - ${airport.name} (${airport.country}) `;
            deleteButton.type = "button";
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", async () => {
                const confirmed = window.confirm(`Delete ${airport.name}?`);
                if (!confirmed) return;

                const response = await fetch(
                    `http://127.0.0.1:8000/airports/${airport.id}`,
                    { method: "DELETE" }
                );

                if (!response.ok) {
                    window.alert("Could not delete the airport.");
                    return;
                }

                await loadAirports();
                await loadProductMetrics();
            });

            item.appendChild(text);
            item.appendChild(deleteButton);
            airportList.appendChild(item);
        });
}

async function loadAirports() {
    const response = await fetch("http://127.0.0.1:8000/airports");
    const data = await response.json();

    airports = data.airports;
    showAirports();
}

airportSearch.addEventListener("input", showAirports);

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
        alert("Could not add the airport.");
        return;
    }

    form.reset();
    await loadAirports();
    alert("Airport added successfully.");
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
        lastCheck.textContent = new Date().toLocaleString("en-US");
    } catch (error) {
        apiStatus.textContent = "unavailable";
        databaseStatus.textContent = "unavailable";
        lastCheck.textContent = new Date().toLocaleString("en-US");
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