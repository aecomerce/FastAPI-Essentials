# Реализация базовой аутентификации

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models.Login import LoginRequest


app = FastAPI()
security = HTTPBasic()  # security — это зависимость, которая извлекает учетные данные из запроса

# Симуляция базы данных в виде списка объектов пользователей
USER_DATA = [
    LoginRequest(**{"username": "Pluto", "password": "god_of_death"}),
    LoginRequest(**{"username": "Arkadiy", "password": "N1"})
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Basic'})
    return user


@app.get('/login')
def get_protected_resource(user: LoginRequest = Depends(authenticate_user)):
    return {'massage': 'You got my secret, welcome'}


@app.get('/logout')
def logout():
        # Возвращаем 401 с заголовком WWW-Authenticate, чтобы сбросить кэш браузера
    raise HTTPException(status_code=401, detail='Logged out', headers={'WWW-Authenticate': 'Basic'})