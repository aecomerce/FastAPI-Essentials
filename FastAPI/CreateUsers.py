from fastapi import FastAPI
from models.UserCreate import Data

app = FastAPI()


# Создание конечной точки FastAPI, которая принимает POST-запрос с данными о пользователе в теле запроса

@app.post('/create_user')
# Функция для обработки входящих пользовательских данных и возврата ответа с полученной пользовательской информацией
def create_user(data: Data):
    return {
        "name": data.name,
        "email": data.email,
        "age": data.age,
        "is_subscribed": data.is_subscribed
    }

