import base64
import requests

def fetch_and_encode_image(image_url, token):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(image_url, headers=headers, allow_redirects=True)  # Ensure redirects are followed
    if response.status_code == 200:
        # Default to using the Content-Type header
        content_type = response.headers.get('Content-Type', '')

        encoded_image = base64.b64encode(response.content).decode('utf-8')
        return encoded_image, content_type
    else:
        raise Exception(f"Failed to fetch image, status code: {response.status_code}")
