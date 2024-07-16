import requests
import hmac
import hashlib
import json

WEBHOOK_SECRET = "eos3nx26om42a0b"


def handler(pd: "pipedream"):
    request_headers = pd.steps["trigger"]["event"]["headers"]
    request_body = pd.steps["trigger"]["event"]["body"]

    signature = get_signature(request_headers, "X-Moveo-Signature")

    if is_verified := verify_signature(signature, request_body):
        pd.respond(
            {
                "status": 200,
                "body": {
                    "responses": [],
                    "output": {"signature": signature, "verified": True},
                },
            }
        )
    if not is_verified:
        pd.respond(
            {
                "status": 200,
                "body": {
                    "responses": [],
                    "output": {"signature": signature, "verified": False},
                },
            }
        )
    else:
        pd.respond(
            {
                "status": 200,
                "body": {"responses": [], "output": {"message": "DEU RUIM"}},
            }
        )


def verify_signature(signature, payload):
    if not signature:
        return False

    bytes_payload = payload.encode("utf-8")
    token_bytes = WEBHOOK_SECRET.encode("utf-8")
    computed_hmac = hmac.new(
        token_bytes,
        bytes_payload,
        hashlib.sha256,
    ).hexdigest()

    # Debugging information
    print(f"Payload: {bytes_payload}")
    print(f"Token Bytes: {token_bytes}")
    print(f"Computed HMAC: {computed_hmac}")
    print(f"Received Signature: {signature}")

    return hmac.compare_digest(computed_hmac, signature)


def get_signature(headers, key):
    try:
        index = headers.index(key)
        return headers[index + 1]
    except (ValueError, IndexError) as e:
        return str(e)
