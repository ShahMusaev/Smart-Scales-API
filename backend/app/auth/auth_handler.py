import time
from fastapi import HTTPException
import jwt
from config import config


def token_response(token: str):
    return {
        "access_token": token
    }


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(f'Decode JWR ERROR: {e}')
        return {}


def verify_jwt(jwtoken: str) -> bool:
    is_token_valid: bool = False
    try:
        payload = decodeJWT(jwtoken)
    except:
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid


def get_user_id_by_jwt(token: str):
    if not verify_jwt(token):
        raise HTTPException(status_code=403, detail="Invalid token or expired token")

    payload = decodeJWT(token)
    if 'user_id' not in payload:
        raise HTTPException(status_code=403, detail="Invalid user")
    user_id = payload.get('user_id')

    return user_id
