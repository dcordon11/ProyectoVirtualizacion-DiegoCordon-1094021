from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os

app = Flask(__name__)
CORS(app)

SECRET_KEY = "clave_secreta_backlog_juegos"

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_database = os.getenv("MONGO_DATABASE")

mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)
db = client[mongo_database]

games_collection = db["games"]
users_collection = db["users"]


def create_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_user_id_from_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except Exception:
        return None


def serialize_game(game):
    return {
        "id": str(game["_id"]),
        "title": game.get("title", ""),
        "platform": game.get("platform", ""),
        "genre": game.get("genre", ""),
        "status": game.get("status", "pendiente"),
        "rating": game.get("rating", 0),
        "hoursPlayed": game.get("hoursPlayed", 0),
        "review": game.get("review", ""),
        "imageUrl": game.get("imageUrl", ""),
        "createdAt": game.get("createdAt", "")
    }


@app.route("/")
def home():
    return jsonify({
        "message": "API de Backlog de Videojuegos funcionando"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "backend"
    })


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Usuario y contraseña son obligatorios"}), 400

    existing_user = users_collection.find_one({"username": username})

    if existing_user:
        return jsonify({"message": "El usuario ya existe"}), 409

    new_user = {
        "username": username,
        "password": generate_password_hash(password),
        "createdAt": datetime.now().isoformat()
    }

    result = users_collection.insert_one(new_user)

    token = create_token(result.inserted_id)

    return jsonify({
        "message": "Usuario registrado correctamente",
        "token": token,
        "username": username
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Credenciales incorrectas"}), 401

    token = create_token(user["_id"])

    return jsonify({
        "message": "Inicio de sesión correcto",
        "token": token,
        "username": username
    })


@app.route("/games", methods=["GET"])
def get_games():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"message": "Token inválido o no enviado"}), 401

    games = games_collection.find({"userId": user_id}).sort("createdAt", -1)

    return jsonify([serialize_game(game) for game in games])


@app.route("/games", methods=["POST"])
def add_game():
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"message": "Token inválido o no enviado"}), 401

    data = request.json

    if not data.get("title"):
        return jsonify({"message": "El título es obligatorio"}), 400

    rating = int(data.get("rating", 0))

    if rating < 0 or rating > 5:
        return jsonify({"message": "La calificación debe estar entre 0 y 5"}), 400

    new_game = {
        "userId": user_id,
        "title": data.get("title"),
        "platform": data.get("platform", ""),
        "genre": data.get("genre", ""),
        "status": data.get("status", "pendiente"),
        "rating": rating,
        "hoursPlayed": int(data.get("hoursPlayed", 0)),
        "review": data.get("review", ""),
        "imageUrl": data.get("imageUrl", ""),
        "createdAt": datetime.now().isoformat()
    }

    result = games_collection.insert_one(new_game)

    return jsonify({
        "message": "Juego agregado correctamente",
        "id": str(result.inserted_id)
    }), 201


@app.route("/games/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    user_id = get_user_id_from_token()

    if not user_id:
        return jsonify({"message": "Token inválido o no enviado"}), 401

    result = games_collection.delete_one({
        "_id": ObjectId(game_id),
        "userId": user_id
    })

    if result.deleted_count == 0:
        return jsonify({"message": "Juego no encontrado"}), 404

    return jsonify({"message": "Juego eliminado correctamente"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)