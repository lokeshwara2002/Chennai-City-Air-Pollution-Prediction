document.addEventListener("DOMContentLoaded", () => {
    const historicalChartDiv = document.getElementById("historical-chart");
    const predictionForm = document.getElementById("prediction-form");
    const predictionResultDiv = document.getElementById("prediction-result");
    const loadingIndicator = document.createElement("div");
    loadingIndicator.textContent = "Loading...";
    loadingIndicator.style.display = "none"; // Initially hidden
    predictionForm.appendChild(loadingIndicator);

    // Fetch historical data and render chart for 1091 days
    function fetchData() {
        fetch("/data?days=1091")
            .then((response) => response.json())
            .then((data) => {
                const pm25Values = data.map((row) => row["PM 2.5"]);
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
                predictionResultDiv.textContent = `Predicted PM2.5: ${data.prediction}`;
                loadingIndicator.style.display = "none"; // Hide loading indicator
                // Removed the line that resets the form
            })
            .catch((error) => {
                console.error("Error fetching prediction:", error);
                predictionResultDiv.textContent = "Failed to fetch prediction.";
                loadingIndicator.style.display = "none"; // Hide loading indicator
            });
    });
});
