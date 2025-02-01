from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []  # Simple in-memory task storage

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    tasks.append(data)
    return jsonify({"message": "Task added successfully", "tasks": tasks})

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)