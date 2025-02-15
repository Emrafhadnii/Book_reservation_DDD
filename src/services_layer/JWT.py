from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, status
from config.jwtsetting import jwt_settings
from jose import jwt,ExpiredSignatureError

class JWTService:
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,jwt_settings.SECRET_KEY,algorithm=jwt_settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,jwt_settings.SECRET_KEY,algorithm=jwt_settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                jwt_settings.SECRET_KEY,
                algorithms=[jwt_settings.ALGORITHM]
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    @staticmethod
    def get_current_user(token: str) -> dict:
        payload = JWTService.decode_token(token)
        return {"user_id": payload.get("sub"),"phone": payload.get("phone"),"role": payload.get("role")}
