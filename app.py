from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Definim traducerile pentru limbi
translations = {
    "en": {
        "total_processing_time": "Total processing time per battery",
        "total_production_time": "Total time required for production",
        "required_shifts": "Required shifts",
        "extra_shifts": "Extra shifts needed",
        "production_rate_remaining_shifts": "Production rate with available shifts",
        "production_rate_with_extra_shift": "Production rate with 1 extra shift",
        "extra_shifts_due_to_downtime": "Extra shifts needed due to downtime",
        "overtime_time": "Overtime will occur at"
    },
    "de": {
        "total_processing_time": "Gesamtverarbeitungszeit pro Batterie",
        "total_production_time": "Gesamtzeit für die Produktion",
        "required_shifts": "Erforderliche Schichten",
        "extra_shifts": "Zusätzliche Schichten erforderlich",
        "production_rate_remaining_shifts": "Produktionsrate mit verfügbaren Schichten",
        "production_rate_with_extra_shift": "Produktionsrate mit 1 zusätzlicher Schicht",
        "extra_shifts_due_to_downtime": "Zusätzliche Schichten erforderlich aufgrund von Ausfallzeiten",
        "overtime_time": "Überzeit tritt auf um"
    }
}

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
        lang = request.form['language']  # Preluăm limba selectată

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
        production_rate_remaining_shifts = num_batteries / (available_shifts * 8) if available_shifts > 0 else 0

        # Calcul baterii pe oră în cazul unei ture suplimentare
        production_rate_with_extra_shift = num_batteries / ((available_shifts + 1) * 8)

        # Calcul ture suplimentare necesare din cauza downtime-ului
        extra_shifts_due_to_downtime = downtime_hours / 8  # câte ture suplimentare sunt necesare

        # Calcul data și ora exactă când paletul va atinge 72h
        utc_now = datetime.utcnow()
        oldest_pallet_timestamp = utc_now - timedelta(minutes=oldest_pallet_time_minutes)
        overtime_timestamp = oldest_pallet_timestamp + timedelta(hours=high_temp_limit)
        overtime_formatted = overtime_timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Formatăm data și ora

        return jsonify({
            translations[lang]["total_processing_time"]: round(total_processing_time, 2),
            translations[lang]["total_production_time"]: round(total_production_time, 2),
            translations[lang]["required_shifts"]: round(required_shifts, 2),
            translations[lang]["extra_shifts"]: round(extra_shifts, 2),
            translations[lang]["production_rate_remaining_shifts"]: round(production_rate_remaining_shifts, 2),
            translations[lang]["production_rate_with_extra_shift"]: round(production_rate_with_extra_shift, 2),
            translations[lang]["extra_shifts_due_to_downtime"]: round(extra_shifts_due_to_downtime, 2),
            translations[lang]["overtime_time"]: overtime_formatted
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
