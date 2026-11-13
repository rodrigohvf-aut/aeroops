const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("airport-form");
const airportList = document.getElementById("airport-list");
const airportSearch = document.getElementById("airport-search");
const airportMapElement = document.getElementById("airport-map");
const previousPageButton = document.getElementById("previous-page");
const nextPageButton = document.getElementById("next-page");
const pageInfo = document.getElementById("page-info");


const airportMap = L.map("airport-map").setView([20, 0], 2);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
}).addTo(airportMap);

const airportMarkers = L.layerGroup().addTo(airportMap);
const aircraftMarkers = L.layerGroup().addTo(airportMap);
const aircraftTrack = L.layerGroup().addTo(airportMap);
const runwayLines = L.featureGroup().addTo(airportMap);

let airports = [];
let selectedAircraftIcao24 = null;

function showAirportMarkers() {
    airportMarkers.clearLayers();

    const search = airportSearch.value.trim().toLowerCase();

    const matchingAirports = airports.filter((airport) =>
        [airport.ident, airport.name, airport.country].some((value) =>
            value.toLowerCase().includes(search)
        )
    );

    matchingAirports.forEach((airport) => {
        const latitude = Number(airport.latitude);
        const longitude = Number(airport.longitude);

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
            return;
        }

        const popup = document.createElement("span");
        popup.textContent =
            `${airport.ident} — ${airport.name} (${airport.country})`;

        L.marker([latitude, longitude])
            .bindPopup(popup)
            .on("click", () => selectAirport(airport))
            .addTo(airportMarkers);
    });

    if (search && matchingAirports.length === 1) {
        const airport = matchingAirports[0];
        airportMap.setView(
            [Number(airport.latitude), Number(airport.longitude)],
            12
        );
    }
}

function drawRunways(runways) {
    runwayLines.clearLayers();

    runways.forEach((runway) => {
        const values = [
            runway.le_latitude_deg,
            runway.le_longitude_deg,
            runway.he_latitude_deg,
            runway.he_longitude_deg,
        ];

        if (
            values.some(
                (value) =>
                    value === null ||
                    value === undefined ||
                    !Number.isFinite(Number(value))
            )
        ) {
            return;
        }

        const ends = [
            [
                Number(runway.le_latitude_deg),
                Number(runway.le_longitude_deg),
            ],
            [
                Number(runway.he_latitude_deg),
                Number(runway.he_longitude_deg),
            ],
        ];

        L.polyline(ends, {
            color: "#ef4444",
            weight: 6,
            runwayId: runway.id,
        })
            .bindPopup(
                `Runway ${runway.le_ident ?? "?"}/${runway.he_ident ?? "?"}`
            )
            .addTo(runwayLines);
    });

    if (runwayLines.getLayers().length > 0) {
        airportMap.fitBounds(runwayLines.getBounds(), {
            padding: [50, 50],
            maxZoom: 15,
        });
    }
}

async function selectAirport(airport) {
    const details = document.getElementById("airport-details");
    const content = document.getElementById("airport-details-content");
    const runwayList = document.getElementById("airport-runways");

    content.textContent =
        `${airport.ident} — ${airport.name} — ${airport.country} | ` +
        `Latitude: ${airport.latitude}, Longitude: ${airport.longitude}`;

    details.hidden = false;
    runwayList.replaceChildren();
    runwayLines.clearLayers();

    airportMap.setView(
        [Number(airport.latitude), Number(airport.longitude)],
        8
    );

    airportMapElement.scrollIntoView({ behavior: "smooth" });

    try {
        const response = await fetch(
            `${API_URL}/airports/${encodeURIComponent(airport.ident)}/runways`
        );

        if (!response.ok) {
            throw new Error("Could not load runways");
        }

        const data = await response.json();

        if (data.runways.length === 0) {
            const item = document.createElement("li");
            item.textContent = "No runways found.";
            runwayList.appendChild(item);
        }

        data.runways.forEach((runway) => {
            const item = document.createElement("li");

            item.textContent =
                `${runway.le_ident ?? "?"}/${runway.he_ident ?? "?"} — ` +
                `Length: ${runway.length_ft ?? "Unknown"} ft — ` +
                `Width: ${runway.width_ft ?? "Unknown"} ft — ` +
                `Surface: ${runway.surface ?? "Unknown"} — ` +
                `Lighted: ${
                    runway.lighted === null
                        ? "Unknown"
                        : runway.lighted
                          ? "Yes"
                          : "No"
                } — ` +
                `Closed: ${
                    runway.closed === null
                        ? "Unknown"
                        : runway.closed
                          ? "Yes"
                          : "No"
                }`;
                item.style.cursor = "pointer";

                item.addEventListener("click", () => {
                    const line = runwayLines
                        .getLayers()
                        .find((layer) => layer.options.runwayId === runway.id);

                    if (!line) return;

                    airportMap.fitBounds(line.getBounds(), {
                        padding: [50, 50],
                        maxZoom: 17,
                    });
                    line.openPopup();
                    airportMapElement.scrollIntoView({ behavior: "smooth" });
                });
                runwayList.appendChild(item);
        });

        drawRunways(data.runways);
        airportMap.invalidateSize();
    } catch (error) {
        const item = document.createElement("li");
        item.textContent = "Could not load runways.";
        runwayList.appendChild(item);
        console.error(error);
    }
}

function showAirports() {
    const search = airportSearch.value.trim().toLowerCase();
    airportList.replaceChildren();

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
            text.style.cursor = "pointer";
            text.addEventListener("click", () => selectAirport(airport));

            deleteButton.type = "button";
            deleteButton.textContent = "Delete";

            deleteButton.addEventListener("click", async () => {
                const confirmed = window.confirm(
                    `Delete ${airport.name}?`
                );

                if (!confirmed) {
                    return;
                }

                const response = await fetch(
                    `${API_URL}/airports/${airport.id}`,
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

let currentPage = 1;
const pageLimit = 20;
let latestAirportRequest = 0;

async function loadAirports() {
    const requestId = ++latestAirportRequest;
    const search = encodeURIComponent(airportSearch.value.trim());

    const response = await fetch(
        `${API_URL}/airports?search=${search}&page=${currentPage}&limit=${pageLimit}`
    );
    const data = await response.json();

    if (requestId !== latestAirportRequest) return;

    airports = data.airports;
    showAirports();
    showAirportMarkers();

    const totalPages = Math.max(1, Math.ceil(data.total / pageLimit));
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    previousPageButton.disabled = currentPage === 1;
    nextPageButton.disabled = currentPage >= totalPages;
}

airportSearch.addEventListener("input", () => {
    currentPage = 1;
    loadAirports();
});

previousPageButton.addEventListener("click", () => {
    currentPage -= 1;
    loadAirports();
});

nextPageButton.addEventListener("click", () => {
    currentPage += 1;
    loadAirports();
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const airport = {
        ident: document.getElementById("ident").value,
        name: document.getElementById("name").value,
        country: document.getElementById("country").value,
        latitude: Number(document.getElementById("latitude").value),
        longitude: Number(document.getElementById("longitude").value),
    };

    const response = await fetch(`${API_URL}/airports`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(airport),
    });

    if (!response.ok) {
        window.alert("Could not add the airport.");
        return;
    }

    form.reset();
    await loadAirports();
    await loadProductMetrics();
    window.alert("Airport added successfully.");
});

async function checkTechnicalStatus() {
    const apiStatus = document.getElementById("api-status");
    const databaseStatus = document.getElementById("database-status");
    const lastCheck = document.getElementById("last-check");

    try {
        const apiResponse = await fetch(`${API_URL}/health`);
        const databaseResponse = await fetch(
            `${API_URL}/health/database`
        );

        if (!apiResponse.ok || !databaseResponse.ok) {
            throw new Error("Health check failed");
        }

        const apiData = await apiResponse.json();
        const databaseData = await databaseResponse.json();

        apiStatus.textContent = apiData.status;
        databaseStatus.textContent = databaseData.database;
    } catch (error) {
        apiStatus.textContent = "unavailable";
        databaseStatus.textContent = "unavailable";
    }

    lastCheck.textContent = new Date().toLocaleString("en-US");
}

async function loadProductMetrics() {
    const airportTotal = document.getElementById("airport-total");
    const countryTotal = document.getElementById("country-total");

    const response = await fetch(`${API_URL}/airports`);
    const data = await response.json();

    airportTotal.textContent = data.total;

    const countries = new Set(
        data.airports
            .map((airport) => airport.country)
            .filter((country) => country)
    );

    const countryResponse = await fetch(`${API_URL}/countries/count`);
    const countryData = await countryResponse.json();
    countryTotal.textContent = countryData.total_countries;
    const runwayTotal = document.getElementById("runway-total");
    const runwayResponse = await fetch(`${API_URL}/runways/count`);
    const runwayData = await runwayResponse.json();

runwayTotal.textContent = runwayData.total_runways;
}

async function loadLatestAircraftPositions() {
    const response = await fetch(`${API_URL}/aircraft/positions/latest`);

    if (!response.ok) {
        console.error("Could not load aircraft positions.");
        return;
    }

    const data = await response.json();
    aircraftMarkers.clearLayers();

    data.positions.forEach((position) => {
        const latitude = Number(position.latitude);
        const longitude = Number(position.longitude);

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
            return;
        }

        L.circleMarker([latitude, longitude], {
            radius: 8,
            color: "#f97316",
            fillColor: "#f97316",
            fillOpacity: 0.9,
        })
            .bindPopup(
                `Aircraft ${position.icao24}<br>` +
                `Observed: ${position.observed_at}<br>` +
                `Source: ${
                    position.source === "simulated"
                        ? "Simulated (test data)"
                        : position.source
                }`
            )
            .on("click", () => showAircraftTrack(position.icao24))
            .addTo(aircraftMarkers);
    });

    if (selectedAircraftIcao24) {
        await showAircraftTrack(selectedAircraftIcao24);
    }
}


async function showAircraftTrack(icao24) {
    selectedAircraftIcao24 = icao24;

    const response = await fetch(
        `${API_URL}/aircraft/${encodeURIComponent(icao24)}/positions`
    );

    if (!response.ok) {
        console.error("Could not load aircraft track.");
        return;
    }

    const data = await response.json();
    aircraftTrack.clearLayers();

    const points = data.positions
        .slice()
        .reverse()
        .map((position) => [
            Number(position.latitude),
            Number(position.longitude),
        ])
        .filter(([latitude, longitude]) =>
            Number.isFinite(latitude) && Number.isFinite(longitude)
        );

    if (points.length < 2) return;

    const line = L.polyline(points, {
        color: "#f97316",
        weight: 4,
    }).addTo(aircraftTrack);

    L.circleMarker(points[0], {
        radius: 6,
        color: "#2563eb",
        fillColor: "#2563eb",
        fillOpacity: 1,
    })
        .bindPopup("First recorded position")
        .addTo(aircraftTrack);

    airportMap.fitBounds(line.getBounds(), {
        padding: [50, 50],
    });
}

loadAirports();
checkTechnicalStatus();
loadProductMetrics();
loadLatestAircraftPositions();
setInterval(loadLatestAircraftPositions, 15000);