from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = '1253874946095185951'
CLIENT_SECRET = 'CF_vkoepoq3ggOqVEzVFtgLD6cUPqn2L'
REDIRECT_URI = 'https://banana-niku87729.github.io/login'
DISCORD_OAUTH2_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/users/@me"

@app.route("/")
def home():
    return '<a href="/login">Discordでログイン</a>'

@app.route("/login")
def login():
    return redirect(f"{DISCORD_OAUTH2_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route("/callback")
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
    r.raise_for_status()
    token = r.json().get('access_token')

    headers = {
        'Authorization': f"Bearer {token}"
    }
    user = requests.get(DISCORD_API_URL, headers=headers).json()

    session['user'] = user
    return f"こんにちは、{user['username']}#{user['discriminator']}さん！"

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
