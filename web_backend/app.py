from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from web_backend.routers import admin, auth, enviroment
from web_backend.schemas import Message

from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException

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
app.include_router(enviroment.router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = Message(message=str(exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(message)
    )



@app.get(
    '/', 
    status_code=HTTPStatus.OK, 
    response_model=Message,
)
def read_root():
    return {'message': 'Hello World!'}
