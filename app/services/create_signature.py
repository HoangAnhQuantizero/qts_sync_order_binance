import time
import hmac
import hashlib

def create_signature(payload, secret_key):
    ordered_payload = [(key, value) for key, value in payload.items()]
    ordered_payload.append(("timestamp", int(time.time() * 1000)))
    query_string = '&'.join([f"{key}={value}" for key, value in ordered_payload])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature
