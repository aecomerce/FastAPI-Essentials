from fastapi import Depends, HTTPException
import secrets, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi.security import OAuth2PasswordBearer  # извлекает токен из заголовка "Authorization: Bearer <token>"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


# Функция для создания JWT токена с заданным временем жизни
def create_jwt_token(data: Dict) -> str:
    # Копируем данные, чтобы не изменить исходный словарь
    to_encode = data.copy() 
    # Задаем время истечения токена
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Добавляем время истечения в словарь
    to_encode.update({"exp": expire})
    # Кодируем токен и возвращаем его
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для получения пользователя из токена
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

