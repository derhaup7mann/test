from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Preluare date din formular
        num_batteries = int(request.form['num_batteries'])
        processing_capacity_per_hour = int(request.form['processing_capacity_per_hour'])
        available_shifts = int(request.form['available_shifts'])
        oldest_pallet_time_minutes = int(request.form['oldest_pallet_time_minutes'])
        downtime_minutes = int(request.form['downtime_minutes'])

        # Convertire minute în ore
        oldest_pallet_time_hours = oldest_pallet_time_minutes / 60
        downtime_hours = downtime_minutes / 60  # Convertim downtime în ore

        # Timpuri fixe
        high_temp_time = 20  # ore
        formation_time = 2 + 10/60  # 2 ore și 10 minute
        high_temp_limit = 72  # Limita maximă de 72 ore

        # Calcul total timp procesare
        total_processing_time = high_temp_time + formation_time

        # Calcul ore necesare pentru producție
        total_production_time = num_batteries / processing_capacity_per_hour

        # Calcul ture necesare
        required_shifts = total_production_time / 8  # presupunem că o tură = 8 ore
        extra_shifts = max(0, required_shifts - available_shifts)

        # Calcul baterii pe oră cu turele disponibile rămase
        if available_shifts > 0:
            production_rate_remaining_shifts = num_batteries / (available_shifts * 8)
        else:
            production_rate_remaining_shifts = 0

        # Calcul baterii pe oră în cazul unei ture suplimentare
        production_rate_with_extra_shift = num_batteries / ((available_shifts + 1) * 8)

        # Calcul ture suplimentare necesare din cauza downtime-ului
        extra_shifts_due_to_downtime = downtime_hours / 8  # câte ture suplimentare sunt necesare

        return jsonify({
            "total_processing_time": round(total_processing_time, 2),
            "total_production_time": round(total_production_time, 2),
            "required_shifts": round(required_shifts, 2),
            "extra_shifts": round(extra_shifts, 2),
            "production_rate_remaining_shifts": round(production_rate_remaining_shifts, 2),
            "production_rate_with_extra_shift": round(production_rate_with_extra_shift, 2),
            "extra_shifts_due_to_downtime": round(extra_shifts_due_to_downtime, 2),
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
