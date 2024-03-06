import base64
import json
import secrets
import uuid

from werkzeug.security import generate_password_hash, check_password_hash


def generate_password():
    return secrets.token_hex(16)


def encode_key(username, password):
    key = json.dumps({
        'key_id': str(uuid.uuid4()),
        'username': username,
        'password': password
    })
    return base64.b64encode(key.encode("ascii")).decode('utf-8')


def decode_key(key):
    decoded = base64.b64decode(key).decode('utf-8')
    payload = json.loads(decoded)
    return payload['username'], payload['password']


def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


def hash_password(password):
    return generate_password_hash(password)
