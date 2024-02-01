from flask import Flask, request, redirect, session, url_for
import requests
import os

app = Flask(__name__)

# Bungie API credentials
CLIENT_ID = "46232"
CLIENT_SECRET = "502d35cafb294f65b1b8e6a70f68eedd"
REDIRECT_URI = "http://localhost:5000/callback"  # Update with your actual redirect URI

# Bungie API endpoints
AUTH_URL = "https://www.bungie.net/en/oauth/authorize"
TOKEN_URL = "https://www.bungie.net/platform/app/oauth/token/"

# Flask secret key for session
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return "Welcome to the Bungie API OAuth Example. <a href='/login'>Login</a> to view your items."

@app.route("/login")
def login():
    return redirect(f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}")

@app.route("/callback")
def callback():
    # Handle the callback after the user logs in on Bungie's site
    code = request.args.get("code")
    token_data = get_access_token(code)
    
    # Save the access token in the session
    session["access_token"] = token_data["access_token"]
    
    return redirect(url_for("view_items"))

@app.route("/view-items")
def view_items():
    # Check if the user is authenticated
    if "access_token" not in session:
        return redirect(url_for("login"))

    # Fetch the user's Destiny 2 profile
    profile_response = make_bungie_api_request("Destiny2/1/Profile/", {"components": "100,200"})
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        # Process the profile data and extract item information
        items = profile_data["Response"]["profileInventory"]["data"]["items"]
        return f"Items: {items}"

    return f"Error: Unable to fetch profile data. Status code: {profile_response.status_code}"

def get_access_token(code):
    # Exchange the authorization code for an access token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, data=data)
    return response.json()

def make_bungie_api_request(endpoint, params=None):
    # Make a request to the Bungie API
    headers = {
        "Authorization": f"Bearer {session['access_token']}",
    }
    url = f"https://www.bungie.net/platform/app/oauth/{endpoint}"

    response = requests.get(url, headers=headers, params=params)
    return response

if __name__ == "__main__":
    app.run(debug=True)
