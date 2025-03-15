document.addEventListener("DOMContentLoaded", async function () {
    try {
        console.log("Fetching history data...");

        const response = await fetch("/get-history");
        if (!response.ok) {
            throw new Error(`Failed to fetch history data: ${response.statusText}`);
        }

        const historyData = await response.json();

        if (!Array.isArray(historyData)) {
            console.error("Invalid history data format:", historyData);
            return;
        }

        const tableBody = document.querySelector("#history-table tbody");
        tableBody.innerHTML = ""; // Clear previous entries

        historyData.forEach(entry => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${entry.date || "N/A"}</td>
                <td>${entry.T || "N/A"}</td>
                <td>${entry.TM || "N/A"}</td>
                <td>${entry.Tm || "N/A"}</td>
                <td>${entry.SLP || "N/A"}</td>
                <td>${entry.H || "N/A"}</td>
                <td>${entry.V || "N/A"}</td>
                <td>${entry.predicted_pm25 || "N/A"}</td>
            `;

            tableBody.appendChild(row);
        });

        console.log("History data successfully loaded.");
    } catch (error) {
        console.error("Error loading history data:", error);
        document.getElementById("history-container").innerHTML = "<p>Error loading history.</p>";
    }
});

// 🔹 Toggle menu visibility
function toggleMenu() {
    document.getElementById("menu").classList.toggle("show");
}
