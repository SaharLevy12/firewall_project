from flask import Flask, render_template, request, make_response, redirect, url_for, session
import secrets
import json

app = Flask(__name__)
app.secret_key = "super-secret-key"

with open('firewall_settings.json', 'r') as file:
    settings = json.load(file)

# ===== Login Page =====
@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login-success")
def login_success():

    
    csrf_token = secrets.token_hex(16)
    session["csrf_token"] = csrf_token

    resp = make_response(redirect(url_for("profile_page")))
    resp.set_cookie("session", "victim_session_123", samesite="Lax")

    return resp


# ===== Profile =====
@app.route("/profile")
def profile_page():
    session_cookie = request.cookies.get("session")

    if not session_cookie:
        return redirect(url_for("login_page"))

    csrf_token = session.get("csrf_token")

    return render_template("profile.html", csrf_token=csrf_token)

@app.route("/logout")
def logout():
    session.clear()

    resp = make_response(redirect(url_for("login_page")))
    resp.delete_cookie("session")

    return resp


# ===== Protected Action =====
@app.route("/change-email", methods=["POST"])
def change_email():
    session_cookie = request.cookies.get("session")

    if not settings["csrf"]:
        if not session_cookie:
            return "Victim Not logged in", 401
        
        email = request.form.get("email")
        return f"Email changed to: {email}"

    csrf_session = session.get("csrf_token")
    csrf_form = request.form.get("csrf_token")

    if not session_cookie:
        return "Victim Not logged in", 401

    if not csrf_session or csrf_session != csrf_form:
        return "CSRF blocked", 403

    email = request.form.get("email")
    return f"Email changed to: {email}"



if __name__ == "__main__":
    app.run(port=5000, debug=True)
