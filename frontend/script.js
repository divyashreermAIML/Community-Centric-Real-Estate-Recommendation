
const searchForm = document.getElementById("searchForm");
const resultsContainer = document.getElementById("results");
const message = document.getElementById("message");
const resultCount = document.getElementById("resultCount");
const searchButton = document.getElementById("searchButton");

searchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const budget = Number(document.getElementById("budget").value);
    const maxDistance = Number(document.getElementById("distance").value);

    const requiredAmenities = Array.from(
        document.querySelectorAll('input[name="amenity"]:checked')
    ).map(input => input.value);

    const transportRequired =
        document.getElementById("transport").checked;

    if (budget <= 0 || maxDistance <= 0) {
        alert("Please enter a valid budget and distance.");
        return;
    }

    const userPreferences = {
        budget: budget,
        max_distance: maxDistance,
        required_amenities: requiredAmenities,
        transport_required: transportRequired
    };

    searchButton.disabled = true;
    searchButton.textContent = "Finding properties...";
    resultsContainer.innerHTML = "";
    message.style.display = "block";
    message.innerHTML = "<h3>Searching properties...</h3><p>Please wait.</p>";
    resultCount.textContent = "Searching";

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/recommend",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userPreferences)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to get recommendations.");
        }

        displayResults(data.recommendations);

    } catch (error) {
        message.style.display = "block";
        message.innerHTML = `
            <h3>Unable to connect</h3>
            <p>${escapeHTML(error.message)}</p>
            <p>Check whether your Flask backend is running.</p>
        `;
        resultCount.textContent = "Error";

    } finally {
        searchButton.disabled = false;
        searchButton.innerHTML =
            'Find suitable properties <span>→</span>';
    }
});


function displayResults(properties) {
    resultsContainer.innerHTML = "";

    resultCount.textContent = `${properties.length} results`;

    if (properties.length === 0) {
        message.style.display = "block";
        message.innerHTML = `
            <div class="empty-icon">⌂</div>
            <h3>No matching properties found</h3>
            <p>Try increasing your budget or distance.</p>
        `;
        return;
    }

    message.style.display = "none";

    properties.forEach(property => {
        const card = document.createElement("article");
        card.className = "property-card";

        const verificationClass =
            property.verification_status.toLowerCase() === "verified"
                ? "verified"
                : "pending";

        card.innerHTML = `
            <div class="property-top">
                <div>
                    <h3>${escapeHTML(property.name)}</h3>
                    <p class="property-category">
                        ${escapeHTML(property.category)}
                    </p>
                </div>

                <div>
                    <div class="score">
                        ${Number(property.suitability_score).toFixed(2)}%
                    </div>
                    <div class="score-label">Suitability match</div>
                </div>
            </div>

            <div class="property-details">
                <span>₹${Number(property.rent).toLocaleString("en-IN")} / month</span>
                <span>${property.distance} km away</span>
            </div>

            <p class="verification ${verificationClass}">
                ● ${escapeHTML(property.verification_status)}
            </p>
        `;

        resultsContainer.appendChild(card);
    });
}


function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}
