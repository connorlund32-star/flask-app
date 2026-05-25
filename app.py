import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
)

# Home
@app.route("/")
def home():
    if "user" in session:
        return f"""
        <h2>Logged in as {session['user']['email']}</h2>
        <a href="/logout">Logout</a>
        """
    return '<a href="/login">Login with Google</a>'

# Login
@app.route("/login")
def login():
    return google.authorize_redirect(url_for("authorize", _external=True))

# Callback
@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()
    session["user"] = user
    return redirect(url_for("home"))

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
