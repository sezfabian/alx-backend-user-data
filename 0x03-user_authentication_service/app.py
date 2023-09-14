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
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    Return the current user’s profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    If the email is not registered,
    respond with a 403 status code.
    Otherwise, generate a token and respond with a 200
    """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200

    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Update the password.
    If the token is invalid, catch the exception
    and respond with a 403 HTTP code.
    """
    email = request.form.get("email")
    password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
