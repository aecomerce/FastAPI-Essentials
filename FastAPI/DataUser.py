from fastapi import FastAPI
from models.ValidateData import User
app = FastAPI()


# Отправка данных о польздователе и проверка возраста
@app.post('/user')
def post_user_data(user: User):
    is_adult = user.age >= 18

    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }
