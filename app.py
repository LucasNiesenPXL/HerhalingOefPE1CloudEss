import os
import time
import socket
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Schakel CORS in zodat frontend requests vanaf S3 Static Website worden toegestaan
CORS(app, resources={r"/api/*": {"origins": "*"}})

START_TIME = time.time()

# Eenvoudige in-memory database
tasks = [
    {
        "id": 1,
        "title": "VPC & Subnets configureren in AWS Academy",
        "category": "Cloud Infra",
        "priority": "Hoog",
        "completed": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 2,
        "title": "EC2 Userdata script testen met Docker",
        "category": "Compute",
        "priority": "Hoog",
        "completed": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 3,
        "title": "S3 Static Website hosting activeren",
        "category": "Storage",
        "priority": "Gemiddeld",
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]
next_task_id = 4


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welkom bij de Cloud Essentials Backend API!",
        "endpoints": {
            "health": "/api/health",
            "info": "/api/info",
            "tasks": "/api/tasks"
        }
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/api/info", methods=["GET"])
def info():
    uptime_seconds = int(time.time() - START_TIME)
    return jsonify({
        "app_name": os.getenv("APP_NAME", "Cloud Essentials Task API"),
        "environment": os.getenv("ENVIRONMENT", "AWS Academy Learner Lab"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "hostname": socket.gethostname(),
        "uptime_seconds": uptime_seconds,
        "tasks_count": len(tasks),
        "in_memory_db": True
    }), 200


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/api/tasks", methods=["POST"])
def add_task():
    global next_task_id
    data = request.get_json(silent=True) or {}
    
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Titel is verplicht"}), 400

    new_task = {
        "id": next_task_id,
        "title": title,
        "category": data.get("category", "Algemeen").strip() or "Algemeen",
        "priority": data.get("priority", "Normaal"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    next_task_id += 1
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH", "PUT"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return jsonify(task), 200
    return jsonify({"error": "Taak niet gevonden"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    initial_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) < initial_len:
        return jsonify({"message": f"Taak {task_id} succesvol verwijderd"}), 200
    return jsonify({"error": "Taak niet gevonden"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # In productie container start gunicorn of app.run
    app.run(host="0.0.0.0", port=port, debug=False)

