import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

BUILD_VERSION = os.environ.get("BUILD_VERSION", "Local Dev")

# מידע מורחב על שחקני המפתח של בארסה
BARCA_SQUAD = [
    {
        "id": 1,
        "name": "Lamine Yamal",
        "position": "Forward",
        "number": 19,
        "rating": 92,
        "assists": 14,
    },
    {
        "id": 2,
        "name": "Pedri",
        "position": "Midfielder",
        "number": 8,
        "rating": 90,
        "assists": 11,
    },
    {
        "id": 3,
        "name": "Gavi",
        "position": "Midfielder",
        "number": 6,
        "rating": 88,
        "assists": 6,
    },
    {
        "id": 4,
        "name": "Robert Lewandowski",
        "position": "Striker",
        "number": 9,
        "rating": 91,
        "assists": 8,
    },
    {
        "id": 5,
        "name": "Pau Cubarsi",
        "position": "Defender",
        "number": 2,
        "rating": 86,
        "assists": 3,
    },
]

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <title>FC Barcelona Squad Dashboard</title>
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
            margin-bottom: 5px;
        }
        .badge-container {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }
        .badge {
            background: #edbb00;
            color: #004d98;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.95rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .badge.api {
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.4);
            text-decoration: none;
            transition: background 0.2s;
        }
        .badge.api:hover {
            background: rgba(255, 255, 255, 0.35);
        }
        p.subtitle {
            font-size: 1.15rem;
            margin-bottom: 35px;
            color: #f7f7f7;
            letter-spacing: 0.5px;
        }
        .card-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 22px;
            width: 100%;
            max-width: 950px;
        }
        .player-card {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 22px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, background 0.3s ease;
        }
        .player-card:hover {
            transform: translateY(-6px);
            background: rgba(255, 255, 255, 0.22);
        }
        .number {
            font-size: 2.2rem;
            color: #edbb00;
            font-weight: bold;
        }
        .name {
            font-size: 1.35rem;
            font-weight: 700;
            margin: 10px 0 4px 0;
            color: #edbb00;
        }
        .position {
            font-size: 0.85rem;
            color: #dedede;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
        }
        .stats-row {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 12px;
            font-size: 0.9rem;
            color: #f0f0f0;
        }
        .stat-label {
            color: #dcdcdc;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <h1>Visca el Barça! 🔴🔵</h1>
    
    <div class="badge-container">
        <div class="badge">Pipeline Version: {{ build_version }}</div>
        <a href="/api/squad" class="badge api" target="_blank">View JSON API ↗</a>
    </div>
    
    <p class="subtitle">Official Blaugrana Key Players Dashboard</p>
    
    <div class="card-container">
        {% for player in players %}
        <div class="player-card">
            <div class="number">#{{ player.number }}</div>
            <div class="name">{{ player.name }}</div>
            <div class="position">{{ player.position }}</div>
            <div class="stats-row">
                <div>
                    <span class="stat-label">Rating</span><br>
                    <strong>{{ player.rating }}</strong>
                </div>
                <div>
                    <span class="stat-label">Assists/Gals</span><br>
                    <strong>{{ player.assists }}</strong>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, players=BARCA_SQUAD, build_version=BUILD_VERSION)

@app.route("/api/squad", methods=["GET"])
def get_squad():
    return jsonify(BARCA_SQUAD)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)