from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()

# Пример извлечения заголовков
@app.get('/headers')
async def get_headers(request: Request, user_agent: str = Header(None), accept_language: str = Header(None)):
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail='Invalid request')
    return {'User-Agent': user_agent, 'Accept-Language': accept_language}
