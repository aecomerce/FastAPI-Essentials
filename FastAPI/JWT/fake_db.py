from hashlib import sha256

USERS_DATA = [
    {
        "username": "Atom", 
        "password": sha256("atomicheart".encode()).hexdigest()
    },
    {
        "username": "John", 
        "password": sha256("Libert".encode()).hexdigest()
    }
]


def get_user_from_db(username: str):
    """
    Функция для поиска пользователя по имени. 
    В реальном проекте это должно быть запросом к базе данных.
    """
    for user in USERS_DATA:
        if user['username'] == username:
            return user
    return None
