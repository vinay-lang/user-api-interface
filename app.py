from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user data
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# Home route
@app.route('/')
def home():
    return "Welcome to the User API! Visit /users to see all users."

# ✅ GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# ✅ GET one user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# ➕ POST: Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email required"}), 400

    user_id = max(users.keys()) + 1 if users else 1
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"message": "User added", "user": users[user_id]}), 201

# ✏️ PUT: Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["email"] = data.get("email", users[user_id]["email"])
    return jsonify({"message": "User updated", "user": users[user_id]})

# 🗑️ DELETE: Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted_user = users.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted_user})
    return jsonify({"error": "User not found"}), 404

# Run app
if __name__ == '__main__':
    app.run(debug=True)
