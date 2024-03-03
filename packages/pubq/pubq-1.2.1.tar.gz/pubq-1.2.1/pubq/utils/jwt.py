import base64
from .storage import storage


def getSignedAuthToken(auth_token_name: str):
    storage.get(auth_token_name)


def getJwtPayload(token):
    if token:
        # Split the JWT into its three parts: header, payload, and signature
        parts = token.split(".")

        # Ensure there are three parts
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")

        # Decode the Base64-encoded payload
        decoded_payload = base64.b64decode(parts[1]).decode('utf-8')

        # Parse the JSON payload
        parsed_payload = json.loads(decoded_payload)

        return parsed_payload
