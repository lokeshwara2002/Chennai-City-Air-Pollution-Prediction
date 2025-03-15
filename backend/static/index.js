document.addEventListener("DOMContentLoaded", () => {
    const historicalChartDiv = document.getElementById("historical-chart");
    const predictionForm = document.getElementById("prediction-form");
    const predictionResultDiv = document.getElementById("prediction-result");
    const conclusionDiv = document.createElement("div"); // Conclusion box
    conclusionDiv.id = "conclusion";
    conclusionDiv.classList.add("conclusion-box");
    predictionResultDiv.after(conclusionDiv); // Insert after prediction result

    const loadingIndicator = document.createElement("div");
    loadingIndicator.textContent = "Loading...";
    loadingIndicator.style.display = "none"; // Initially hidden
    predictionForm.appendChild(loadingIndicator);

    // Fetch historical data and render chart for 1091 days
    function fetchData() {
        fetch("/data?days=1091")
            .then((response) => response.json())
            .then((data) => {
                console.log("Historical Data:", data); // Debugging

                if (!Array.isArray(data) || data.length === 0) {
                    console.error("No historical data available.");
                    return;
                }

                const pm25Values = data.map((row) => row["PM 2.5"]); // Fixed Key
                const dates = data.map((_, index) => index);

                Plotly.newPlot(historicalChartDiv, [
                    {
                        x: dates,
                        y: pm25Values,
                        type: "scatter",
                        mode: "lines+markers",
                        marker: { color: "blue" },
                        name: "Historical PM2.5",
                    },
                ]);
            })
            .catch((error) => {
                console.error("Error fetching historical data:", error);
            });
    }

    // Initial fetch for 1091 days
    fetchData();

    // Handle prediction form submission
    predictionForm.addEventListener("submit", (e) => {
        e.preventDefault();
        loadingIndicator.style.display = "block"; // Show loading indicator

        const formData = new FormData(predictionForm);
        const inputData = {};
        formData.forEach((value, key) => {
            inputData[key] = parseFloat(value);
        });

        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(inputData),
        })
            .then((response) => response.json())
            .then((data) => {
                const pm25 = data.prediction;
                predictionResultDiv.innerHTML = `<p>Predicted PM2.5: <strong>${pm25}</strong></p>`;

                // 🟢 Categorizing PM2.5 levels (AQI-based)
                let conclusionText = "";
                let color = "";
                if (pm25 <= 50) {
                    conclusionText = "🟢 Good Air Quality - Enjoy the fresh air! ✅";
                    color = "green";
                } else if (pm25 <= 100) {
                    conclusionText = "🟡 Moderate Air Quality - Sensitive people should be cautious. ⚠️";
                    color = "yellow";
                } else if (pm25 <= 150) {
                    conclusionText = "🟠 Unhealthy for Sensitive Groups - Reduce outdoor activities. ⚠️";
                    color = "orange";
                } else if (pm25 <= 200) {
                    conclusionText = "🔴 Unhealthy - Everyone should reduce prolonged outdoor activities! ❌";
                    color = "red";
                } else if (pm25 <= 300) {
                    conclusionText = "🟣 Very Unhealthy - Serious health effects! Wear masks outdoors. 🚨";
                    color = "purple";
                } else {
                    conclusionText = "⚫ Hazardous - Stay indoors! Use air purifiers! 🚨";
                    color = "black";
                }

                conclusionDiv.innerHTML = `<p>${conclusionText}</p>`;
                conclusionDiv.style.color = color;
                loadingIndicator.style.display = "none"; // Hide loading indicator
            })
            .catch((error) => {
                console.error("Error fetching prediction:", error);
                predictionResultDiv.textContent = "Failed to fetch prediction.";
                loadingIndicator.style.display = "none"; // Hide loading indicator
            });
    });
});
