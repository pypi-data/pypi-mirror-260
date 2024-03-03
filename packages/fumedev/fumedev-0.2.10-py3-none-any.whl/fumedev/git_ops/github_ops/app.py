import os
from dotenv import load_dotenv
load_dotenv(override=True)
import jwt
import time
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from fumedev import env


class GithubApp:
    def __init__(self):
        self.app_id = os.getenv("GITHUB_APP_ID")
        self.private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")
        self.org_name = env.ORG_NAME

        with open(self.private_key_path, 'rb') as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
                )
        self.generate_jwt()
        self.get_installations()
        self.fetch_installation_access_token()
    
    def generate_jwt(self):
        # Current time and expiration time (10 minutes)
        now = int(time.time())
        payload = {
            'iat': now,
            'exp': now + (10 * 60),
            'iss': self.app_id
        }
        self.jwt = jwt.encode(payload, self.private_key, algorithm='RS256')

    def get_installations(self):
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get('https://api.github.com/app/installations', headers=headers)

        if response.status_code == 200:
            installations = response.json()
            for installation in installations:
                if installation['account']['login'] == self.org_name:
                    self.installation = installation
        else:
            print("Error fetching installations")

    def fetch_installation_access_token(self):
        self.generate_jwt()
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Accept': 'application/vnd.github.v3+json'
        }
        url = f'https://api.github.com/app/installations/{self.installation["id"]}/access_tokens'
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            env.GITHUB_TOKEN['TOKEN'] =  response.json()['token']
            env.GITHUB_TOKEN['EXPIRTATION'] = time.time() + 3550
        else:
            raise Exception("Failed to obtain installation access token")
        
    
