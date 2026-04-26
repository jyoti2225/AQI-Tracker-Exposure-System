let aqiChart, tempChart, rainChart, uvChart;

function getShortHourLabels(times) {
    return times.map(t => {
        if (!t) return "";
        const d = new Date(t);
        if (isNaN(d.getTime())) return String(t);

        let h = d.getHours();
        const s = h >= 12 ? "PM" : "AM";
        h = h % 12 || 12;
        return `${h} ${s}`;
    });
}

function getAqiText(aqi) {
    if (aqi <= 50) return "Good";
    if (aqi <= 100) return "Satisfactory";
    if (aqi <= 150) return "Moderate";
    if (aqi <= 200) return "Poor";
    if (aqi <= 300) return "Unhealthy";
    return "Hazardous";
}

function getUvText(uv) {
    if (uv <= 2) return "Low";
    if (uv <= 5) return "Moderate";
    if (uv <= 7) return "High";
    if (uv <= 10) return "Very High";
    return "Extreme";
}

function updateCards(aqi, temp, rain, uv) {
    document.querySelector(".aqi h1").innerText = aqi;
    document.querySelector(".aqi p").innerText = getAqiText(aqi);
    document.querySelector(".temp h1").innerText = temp + "°C";
    document.querySelector(".rain h1").innerText = rain + "%";
    document.querySelector(".uv h1").innerText = uv;
    document.querySelector(".uv p").innerText = getUvText(uv);
}

function showNotifications(aqi, uv) {
    let airMsg = "";
    let uvMsg = "";

    if (aqi <= 50) airMsg = "🟢 Air is clean.";
    else if (aqi <= 100) airMsg = "🟡 Air acceptable. Stay hydrated.";
    else if (aqi <= 150) airMsg = "🟠 Limit outdoor time. Stay hydrated.";
    else if (aqi <= 200) airMsg = "🔶 Avoid heavy activity. Turn on air purifier.";
    else if (aqi <= 300) airMsg = "🔴 Stay indoors. Turn on air purifier.";
    else airMsg = "🟣 Dangerous air! Stay indoors and use purifier.";

    if (uv <= 2) uvMsg = "🟢 UV safe.";
    else if (uv <= 5) uvMsg = "🟡 Use sunscreen.";
    else if (uv <= 7) uvMsg = "🟠 Limit sun exposure. Wear a cap.";
    else if (uv <= 10) uvMsg = "🔴 Avoid sunlight. Use sunscreen and cap.";
    else uvMsg = "🟣 Extreme UV! Stay indoors.";

    let msg = `${airMsg}<br>${uvMsg}`;
    showPopup(msg);
}

function renderCharts(labels, aqi, temp, rain, uv) {
    if (aqiChart) aqiChart.destroy();
    if (tempChart) tempChart.destroy();
    if (rainChart) rainChart.destroy();
    if (uvChart) uvChart.destroy();

    aqiChart = new Chart(document.getElementById("aqiChart"), {
        type: "line",
        data: { labels, datasets: [{ label: "AQI", data: aqi, borderColor: "red", fill: true ,tension: 0.4 }] }
    });

    tempChart = new Chart(document.getElementById("tempChart"), {
        type: "line",
        data: { labels, datasets: [{ label: "Temp", data: temp, borderColor: "orange", fill: true , tension: 0.4}] }
    });

    rainChart = new Chart(document.getElementById("rainChart"), {
        type: "bar",
        data: { labels, datasets: [{ label: "Rain", data: rain, backgroundColor: "blue" , tension: 0.4}] }
    });

    uvChart = new Chart(document.getElementById("uvChart"), {
        type: "line",
        data: { labels, datasets: [{ label: "UV", data: uv, borderColor: "purple", fill: true , tension: 0.4 }] }
    });
}

function searchLiveCity() {
    const city = document.getElementById("cityInput").value.trim();
    if (!city) return alert("Enter city");

    fetch(`/api/city_data?city=${encodeURIComponent(city)}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const labels = getShortHourLabels((data.hourly.time || []).slice(0, 24));

            updateCards(
                data.current.aqi || 0,
                data.current.temperature || 0,
                data.current.rain || 0,
                data.current.uv || 0
            );

            renderCharts(
                labels,
                (data.hourly.aqi || []).slice(0, 24),
                (data.hourly.temperature || []).slice(0, 24),
                (data.hourly.rain || []).slice(0, 24),
                (data.hourly.uv || []).slice(0, 24)
            );

            showNotifications(data.current.aqi || 0, data.current.uv || 0);
        })
        .catch(() => alert("Database data load error"));
}

window.onload = function () {
    const cityInput = document.getElementById("cityInput");
    if (cityInput) {
        cityInput.value = "Patiala";
        searchLiveCity();
    }
};
document.addEventListener("DOMContentLoaded", () => {
    ["loginForm", "signupForm"].forEach(id => {
        const form = document.getElementById(id);
        if (!form) return;

        form.addEventListener("submit", e => {
            const email = document.getElementById("email").value.trim();
            const pass = document.getElementById("password").value.trim();

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#^()_+\-=\[\]{};':"\\|,.<>\/?])[A-Za-z\d@$!%*?&.#^()_+\-=\[\]{};':"\\|,.<>\/?]{8,}$/;

            if (!emailPattern.test(email)) {
                alert("Enter a valid email address");
                e.preventDefault();
                return;
            }

            if (!passwordPattern.test(pass)) {
                alert(
                    "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."
                );
                e.preventDefault();
                return;
            }
        });
    });
});
function showPopup(msg) {
    const box = document.getElementById("popupBox");
    const text = document.getElementById("popupMessage");

    if (box && text) {
        text.innerHTML = msg;
        box.style.display = "block";

        setTimeout(() => {
            box.style.display = "none";
        }, 10000);    }
}

function closePopup() {
    document.getElementById("popupBox").style.display = "none";
}