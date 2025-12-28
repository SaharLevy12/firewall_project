from flask import Flask, render_template, request, make_response, redirect, url_for
import secrets

app = Flask(__name__)

# ===== Login Page =====
@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login-success")
def login_success():
    csrf_token = secrets.token_hex(16)

    resp = make_response(redirect(url_for("profile_page")))
    resp.set_cookie("session", "victim_session_123", samesite="Lax")
    resp.set_cookie("csrf_token", csrf_token, samesite="Lax")

    return resp


# ===== Profile =====
@app.route("/profile")
def profile_page():
    session_cookie = request.cookies.get("session")
    csrf_token = request.cookies.get("csrf_token")

    if not session_cookie:
        return redirect(url_for("login_page"))

    return render_template("profile.html", csrf_token=csrf_token)


# ===== Protected Action =====
@app.route("/change-email", methods=["POST"])
def change_email():
    session_cookie = request.cookies.get("session")
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_form = request.form.get("csrf_token")

    if not session_cookie:
        return "Victim Not logged in", 401

    if not csrf_cookie or csrf_cookie != csrf_form:
        return "CSRF blocked", 403

    email = request.form.get("email")
    return f"Email changed to: {email}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
