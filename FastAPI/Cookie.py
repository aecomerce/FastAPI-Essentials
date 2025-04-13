# Простой проект на FastAPI, реализующий аутентификацию на основе 
# файлов cookie.

from fastapi import FastAPI, Response, Request, HTTPException
from models.Login import LoginRequest
from uuid import uuid4
from hashlib import sha256

# Response нужен для создания куки файлов
# Request нужен для получения куки файлов
# uuid4 используется для генерации токена сессии
# sha256 здесь используется для хэширования паролей. Так безопаснее.

app = FastAPI()

# Хранение тестовых данных
fake_db = [
    {
      "username": "Joe",
      "password": sha256("password123".encode()).hexdigest(),
      "session_token": None
    },
    {
      "username": "Robert",
      "password": sha256("password123".encode()).hexdigest(),
      "session_token": None
    }
]


@app.post('/login')
async def login(user: LoginRequest, response: Response):
    """
    Логика работы:
    1. Получение пост запроса на авторизацию. Отправляем json. response отправляется автоматически
    2. Хэшируем пароль юзера
    3. Проверяем наличие пользователя в бд
    4. Если пользователь есть:
        1. Создаем токен сессии
        2. Сохраняем токен в куки
        3. Возвращаем токен
    4. Если пользователя нет, то возвращаем сообщение об ошибке
    """
    hashed_password = sha256(user.password.encode()).hexdigest()
    for user_db in fake_db:
        if user_db['username'] == user.username:
            if user_db['password'] == hashed_password:
                session_token = str(uuid4())
                user_db['session_token'] = session_token
                response.set_cookie(key='session_token', value=session_token, httponly=True, secure=True, samesite='lax')
                return {"message": "Login successful!", "session_token": session_token}
    raise HTTPException(status_code=401, detail='Unauthorized')


@app.get('/user')
async def get_user(request: Request):
    """
    Запрашиваем у пользователя его куки через метод get.
    Если токен найден, перебираем пользователей и ищем совпадение по session_token
    и возвращаем его данные.
    Если нет, выдаем ошибку.
    """
    token = request.cookies.get('session_token')
    if token:
        for user_db in fake_db:
            if user_db.get('session_token') == token:
                return {'username': user_db['username'], 'password': user_db['password']}
    raise HTTPException(status_code=401, detail="Unauthorized")

"""
Для лучшего понимания:
Сигнатура Response.set_cookie:

def set_cookie(
    self,
    key: str,
    value: str = "",
    max_age: Optional[int] = None,
    expires: Optional[int] = None,
    path: str = "/",
    domain: Optional[str] = None,
    secure: bool = False,
    httponly: bool = False,
    samesite: Literal["lax", "strict", "none"] = "lax",
) -> None:

Параметры:
- key (str): Имя куки.
- value (str, optional): Значение куки. По умолчанию "".
- max_age (Optional[int], optional): Максимальное время жизни куки в секундах. По умолчанию None.
- expires (Optional[int], optional): Время истечения срока действия куки в секундах с начала эпохи Unix. По умолчанию None.
- path (str, optional): Путь, для которого будет доступна куки. По умолчанию "/".
- domain (Optional[str], optional): Домен, для которого будет доступна куки. По умолчанию None.
- secure (bool, optional): Указывает, что куки должна передаваться только по защищенному соединению (HTTPS). По умолчанию False.
- httponly (bool, optional): Указывает, что куки должна быть доступна только через HTTP(S) и не должна быть доступна через JavaScript. По умолчанию False.
- samesite (Literal["lax", "strict", "none"], optional): Политика SameSite для куки. По умолчанию "lax".

"""