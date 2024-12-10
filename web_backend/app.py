from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from web_backend.routers import admin, auth
from web_backend.schemas import Message

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(admin.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}
