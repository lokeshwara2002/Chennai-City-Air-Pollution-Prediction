document.addEventListener("DOMContentLoaded", async function () {
    console.log("Loading forecast page...");

    const forecastChartDiv = document.getElementById("forecast-chart");
    const forecastRange = document.getElementById("forecast-range");
    const forecastBtn = document.getElementById("forecast-btn");
    const conclusionDiv = document.createElement("div"); // Conclusion box
    conclusionDiv.id = "forecast-conclusion";
    conclusionDiv.classList.add("conclusion-box");
    forecastChartDiv.after(conclusionDiv); // Insert below the chart

    async function loadForecast(days) {
        console.log(`Fetching forecast for ${days} days...`);

        try {
            const response = await fetch("/static/forecast.json");
            if (!response.ok) {
                throw new Error(`Failed to fetch forecast data: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("Forecast data received:", data);

            if (!Array.isArray(data) || data.length === 0) {
                throw new Error("Invalid or empty forecast data.");
            }

            const selectedData = data.slice(0, days); // Select the required number of days
            const dates = selectedData.map(entry => entry.date);
            const pm25Values = selectedData.map(entry => entry.predicted_pm25);

            let trace = {
                x: dates,
                y: pm25Values,
                type: "scatter",
                mode: "lines+markers",
                name: `PM2.5 Prediction for ${days} Days`,
                marker: { color: "orange" }
            };

            let layout = {
                title: `PM2.5 Forecast for ${days} Days`,
                xaxis: { title: "Date" },
                yaxis: { title: "PM2.5 Levels" },
                plot_bgcolor: "#f4f4f4",
                paper_bgcolor: "#fff"
            };

            Plotly.newPlot(forecastChartDiv, [trace], layout);

            updateConclusions(selectedData); // Generate conclusion for displayed data

        } catch (error) {
            console.error("Error loading forecast:", error);
            forecastChartDiv.innerHTML = "<p>Error loading forecast data.</p>";
            conclusionDiv.innerHTML = "";
        }
    }

    // 🟢 Function to Generate Daily PM2.5 Conclusions
    function updateConclusions(data) {
        if (data.length === 0) {
            conclusionDiv.innerHTML = "<p>No forecast data available.</p>";
            return;
        }

        let conclusionsHTML = "<h2>Daily PM2.5 Conclusions</h2><ul>";

        data.forEach(entry => {
            let conclusionText = getPM25Conclusion(entry.predicted_pm25);
            conclusionsHTML += `<li><strong>${entry.date}:</strong> ${conclusionText}</li>`;
        });

        conclusionsHTML += "</ul>";
        conclusionDiv.innerHTML = conclusionsHTML;
    }

    // 🟢 Function to Determine Air Quality Conclusion
    function getPM25Conclusion(pm25) {
        if (pm25 <= 50) return "🟢 Good Air Quality - Enjoy the fresh air! ✅";
        if (pm25 <= 100) return "🟡 Moderate Air Quality - Sensitive people should be cautious. ⚠️";
        if (pm25 <= 150) return "🟠 Unhealthy for Sensitive Groups - Reduce outdoor activities. ⚠️";
        if (pm25 <= 200) return "🔴 Unhealthy - Everyone should reduce prolonged outdoor activities! ❌";
        if (pm25 <= 300) return "🟣 Very Unhealthy - Serious health effects! Wear masks outdoors. 🚨";
        return "⚫ Hazardous - Stay indoors! Use air purifiers! 🚨";
    }

    // 🟢 Event Listener for Forecast Button
    forecastBtn.addEventListener("click", function () {
        let days = parseInt(forecastRange.value);
        loadForecast(days);
    });

    // 🟢 Load default forecast (7 days) on page load
    loadForecast(7);
});
