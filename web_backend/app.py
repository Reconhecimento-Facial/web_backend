from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from starlette.exceptions import HTTPException as StarletteHTTPException

from web_backend.routers import admin, auth, enviroment, user
from web_backend.schemas import ExistingUser, Message

app = FastAPI()
add_pagination(app)

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

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(enviroment.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    if isinstance(exc.detail, dict) and 'existing_user' in exc.detail:
        existing_user = ExistingUser(
            message=exc.detail['message'],
            existing_user=exc.detail['existing_user'],
        )
        content = jsonable_encoder(existing_user)
    else:
        message = Message(message=str(exc.detail))
        content = jsonable_encoder(message)
    return JSONResponse(status_code=exc.status_code, content=content)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Hello World!'}
