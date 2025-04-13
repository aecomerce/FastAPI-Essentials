from fastapi import FastAPI, Depends, HTTPException
from security import get_user_from_token, create_jwt_token
from model_user import User
from fake_db import get_user_from_db, USERS_DATA
from hashlib import sha256

app = FastAPI()

# Маршрут для аутентификации пользователя. 
# Если данные правильные, возвращается JWT токен.
@app.post('/login')
async def login(user_in: User):
    hashed_password = sha256(user_in.password.encode()).hexdigest()
    for user_db in USERS_DATA:
        if user_db['username'] == user_in.username:
            if user_db['password'] == hashed_password:
                # Если проверка прошла успешно, генерируем токен для пользователя
                token = create_jwt_token({'sub': user_in.username})
                # "sub" — это subject, в нашем случае имя пользователя
                return{'access_token': token, 'token_type': 'bearer'}
    raise HTTPException(status_code=401, detail='Unauthorized')


# Защищённый маршрут, который возвращает сообщение об успешном доступе, 
# если токен в запросе действителен.
@app.get('/protected_resource')
async def protected_resource(current_user: str = Depends(get_user_from_token)):
    """
    Этот маршрут защищен и требует токен. 
    Если токен действителен, мы возвращаем сообщение об успешном доступе.
    """
    user = get_user_from_db(current_user)
    if user:
        return {'message': 'Successful access'}
    raise HTTPException(status_code=401, detail='Unauthorized')