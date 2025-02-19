from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://Diah:tH2m1vVBKYnuqRfc@cluster0.hco8p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyDatabase"]
collection = db["MyCollection"]

# Route to Receive Data from ESP32
@app.route("/api/dht", methods=["POST"])
def receive_data():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Data saved"}), 201

# Route to Get Data from MongoDB
@app.route("/api/dht", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB "_id" field
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
