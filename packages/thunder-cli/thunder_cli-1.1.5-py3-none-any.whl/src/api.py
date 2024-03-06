import requests
import click

FIREBASE_API_KEY = 'AIzaSyDFojZdCcPvKAczWrZTl-6DMtSq8E2X3Xk'

def authenticate_user():
    email = click.prompt("Please enter your email", type=str)
    password = click.prompt("Please enter your password", type=str, hide_input=True)
    
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }

    response = requests.post(
        f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}',
        data=data
    )

    if response.ok:
        id_token = response.json()['idToken']
        refresh_token = response.json()['refreshToken']
        uid = response.json()['localId']

        return id_token, refresh_token, uid
    else:
        click.echo("Authentication failed.")
        return None, None, None

def refresh_id_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    response = requests.post(
        f'https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}',
        data=data
    )

    if response.ok:
        id_token = response.json()['id_token']
        new_refresh_token = response.json()['refresh_token']
        uid = response.json()['user_id']
        return id_token, new_refresh_token, uid
    else:
        return None, None, None
    

def is_token_valid(id_token):
    # Endpoint to verify the ID token
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    
    data = {
        'idToken': id_token
    }

    response = requests.post(url, data=data)
    # If the response is successful, the token is valid
    return response.ok