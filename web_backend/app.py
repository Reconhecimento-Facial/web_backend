from http import HTTPStatus

from fastapi import FastAPI

from web_backend.routers import auth, workers
from web_backend.schemas import MessageSchema

app = FastAPI()
app.include_router(workers.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'Hello World!'}
