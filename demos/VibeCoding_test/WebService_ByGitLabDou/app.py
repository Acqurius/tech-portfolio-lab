from flask import Flask, jsonify, request

# 初始化 Flask 應用
app = Flask(__name__)

# 範例資料
tasks = [
    {"id": 1, "title": "學習 Python", "completed": False},
    {"id": 2, "title": "開發 Web Service", "completed": False}
]

# 根路由
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "歡迎使用簡易任務管理 API"})

# 獲取所有任務
@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({"tasks": tasks})

# 獲取特定任務
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify({"task": task})
    return jsonify({"error": "找不到任務"}), 404

# 新增任務
@app.route('/api/tasks', methods=['POST'])
def add_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "請提供任務標題"}), 400
    
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": request.json["title"],
        "completed": request.json.get("completed", False)
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

# 更新任務
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "找不到任務"}), 404
    
    if not request.json:
        return jsonify({"error": "無效的請求"}), 400
    
    task["title"] = request.json.get("title", task["title"])
    task["completed"] = request.json.get("completed", task["completed"])
    return jsonify({"task": task})

# 刪除任務
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "找不到任務"}), 404
    
    tasks.remove(task)
    return jsonify({"result": "任務已刪除"})

# 啟動應用
if __name__ == '__main__':
    app.run(debug=True)