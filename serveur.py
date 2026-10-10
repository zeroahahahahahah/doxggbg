from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import requests

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/*": {"origins": "*"}})
limiter = Limiter(get_remote_address, app=app, default_limits=[])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@app.route("/")
def accueil():
    return send_file("index.html")

@app.route("/enregistrer", methods=["POST"])
@limiter.limit("1 per minute")
def enregistrer():
    data = request.get_json()
    ip = data.get("ip", "inconnue")
    pseudo = data.get("pseudo", "inconnu")

    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/visiteurs",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            },
            json={"pseudo": pseudo, "ip": ip}
        )
    except Exception as e:
        print("Erreur Supabase :", e)

    print(f"{pseudo} : {ip}")
    return jsonify({"statut": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
