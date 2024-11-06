from fastapi import FastAPI
import uvicorn
from routes import nettool
from routes import webhook


app = FastAPI()


@app.get('/')
def hello():
    return "Hello Alert!2"


app.include_router(nettool.router, prefix='/nettool', tags=['网络工具'])
app.include_router(webhook.router, prefix='/webhook', tags=['告警'])


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
