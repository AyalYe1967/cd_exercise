from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# מידע לדוגמה על שחקני המפתח של בארסה
BARCA_SQUAD = [
    {"id": 1, "name": "Lamine Yamal", "position": "Forward", "number": 19},
    {"id": 2, "name": "Pedri", "position": "Midfielder", "number": 8},
    {"id": 3, "name": "Gavi", "position": "Midfielder", "number": 6},
    {"id": 4, "name": "Robert Lewandowski", "position": "Striker", "number": 9},
    {"id": 5, "name": "Pau Cubarsi", "position": "Defender", "number": 2},
]

# תבנית HTML בעיצוב קלאוטר (Blaugrana) שמוצגת בעמוד הבית
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <title>FC Barcelona Flask App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #004d98, #a50044);
            color: #ffffff;
            margin: 0;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #edbb00;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-size: 2.8rem;
            margin-bottom: 10px;
        }
        p.subtitle {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: #f7f7f7;
        }
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            width: 100%;
            max-width: 900px;
        }
        .player-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .player-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.25);
        }
        .number {
            font-size: 2rem;
            color: #edbb00;
            font-weight: bold;
        }
        .name {
            font-size: 1.3rem;
            font-weight: 600;
            margin: 10px 0 5px 0;
            color: #edbb00; /* שונה לצבע הצהוב של בארסה, אפשר להחליף לכל קוד HEX שתרצה */
        }
        .position {
            font-size: 0.9rem;
            color: #dedede;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <h1>Visca el Barça! 🔴🔵</h1>
    <p class="subtitle">FC Barcelona Squad Dashboard powered by Flask</p>
    
    <div class="card-container">
        {% for player in players %}
        <div class="player-card">
            <div class="number">#{{ player.number }}</div>
            <div class="name">{{ player.name }}</div>
            <div class="position">{{ player.position }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, players=BARCA_SQUAD)

@app.route("/api/squad", methods=["GET"])
def get_squad():
    return jsonify(BARCA_SQUAD)

if __name__ == "__main__":
    # מאזין לכל כתובות ה-IP כדי שיוכל לרוץ תקין בתוך קונטיינר בפורט 5000
    app.run(host="0.0.0.0", port=5000, debug=True)