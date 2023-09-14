#!/usr/bin/env python3
"""Flask app module
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Index or home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    create a new session for the user,
    store the session ID as a cookie with key
    "session_id" on the response
    and return a JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Destroy a user’s session
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
