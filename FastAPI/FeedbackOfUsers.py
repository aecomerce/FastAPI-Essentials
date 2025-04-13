from fastapi import FastAPI
from typing import List
from models.Feedback import UserFeedback


app = FastAPI()

feedback_storage: List[UserFeedback] = []


# Создание конечной точки POST, которая позволяет пользователям отправлять отзывы.
@app.post('/feedback')
# Функция для обработки входящих данных обратной связи и ответа сообщением об успешном завершении.
def post_feedback(user: UserFeedback):
    feedback_storage.append(user)
    return {
        "message": f"Feedback received. Thank you, {user.name}"
    }


# Получение всех отзывов
@app.get('/feedback')
def get_feedback():
    return feedback_storage
