from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/set-session")
def set_session():
    resp = make_response(redirect(url_for("profile_page")))
    resp.set_cookie(
        "session",
        "victim_session_123",
        samesite="Lax"
    )
    return resp

@app.route("/profile")
def profile_page():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return "Not logged in", 401

    return render_template("profile.html")

@app.route("/change-email", methods=["POST"])
def change_email():
    session_cookie = request.cookies.get("session")
    email = request.form.get("email")

    if not session_cookie:
        return "Unauthorized", 401

    return f"Email changed to: {email}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
