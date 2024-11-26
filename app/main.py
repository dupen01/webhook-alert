from fastapi import FastAPI
from routes import nettool
from routes import webhook


app = FastAPI()


@app.get('/')
def hello():
    return "Hello Alert!2"


app.include_router(nettool.router, prefix='/nettool', tags=['网络工具'])
app.include_router(webhook.router, prefix='/webhook', tags=['告警'])
