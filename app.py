<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Battery Processing Calculator</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            margin: 40px;
        }
        .container {
            max-width: 600px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin: auto;
        }
        input {
            padding: 10px;
            margin: 5px;
            width: 80%;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h2>Battery Processing Calculator</h2>

        <input type="number" id="num_batteries" placeholder="Enter total number of batteries"><br>
        <input type="number" id="processing_capacity_per_hour" placeholder="Enter processing capacity per hour"><br>
        <input type="number" id="available_shifts" placeholder="Enter available shifts"><br>
        <input type="number" id="oldest_pallet_time_minutes" placeholder="Oldest pallet time (minutes)"><br>
        <input type="number" id="downtime_minutes" placeholder="Enter downtime (minutes)"><br>

        <button onclick="calculate()">Calculate</button>

        <div id="result"></div>
    </div>

    <script>
        function calculate() {
            let num_batteries = document.getElementById("num_batteries").value;
            let processing_capacity_per_hour = document.getElementById("processing_capacity_per_hour").value;
            let available_shifts = document.getElementById("available_shifts").value;
            let oldest_pallet_time_minutes = document.getElementById("oldest_pallet_time_minutes").value;
            let downtime_minutes = document.getElementById("downtime_minutes").value;

            fetch('/calculate', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `num_batteries=${num_batteries}&processing_capacity_per_hour=${processing_capacity_per_hour}&available_shifts=${available_shifts}&oldest_pallet_time_minutes=${oldest_pallet_time_minutes}&downtime_minutes=${downtime_minutes}`
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerHTML = `
                    <p>🔹 Total processing time per battery: <strong>${data.total_processing_time} hours</strong></p>
                    <p>🔹 Total time required for production: <strong>${data.total_production_time} hours</strong></p>
                    <p>🔹 Required shifts: <strong>${data.required_shifts}</strong></p>
                    <p>🔹 Extra shifts needed: <strong>${data.extra_shifts}</strong></p>
                    <p>🔹 📈 Production rate with remaining shifts: <strong>${data.production_rate_remaining_shifts} batteries/hour</strong></p>
                    <p>🔹 🚀 Production rate with one extra shift: <strong>${data.production_rate_with_extra_shift} batteries/hour</strong></p>
                    <p>🔹 ⚠️ Extra shifts needed due to downtime: <strong>${data.extra_shifts_due_to_downtime}</strong></p>
                `;
            })
            .catch(error => console.error('Error:', error));
        }
    </script>

</body>
</html>
