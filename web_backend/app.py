from http import HTTPStatus

from fastapi import FastAPI

from web_backend.routers import admin, auth, workers
from web_backend.schemas import Message

app = FastAPI()
# app.include_router(workers.router)
# app.include_router(auth.router)
app.include_router(admin.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}
