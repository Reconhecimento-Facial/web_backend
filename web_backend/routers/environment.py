from dataclasses import asdict
from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session
from unidecode import unidecode

from web_backend.database import get_session
from web_backend.models import Admin, Environment, User
from web_backend.schemas import (
    EnvironmentCreated,
    EnvironmentFilter,
    EnvironmentPublic,
    EnvironmentPublicWithPhotoURL,
    EnvironmentSchema,
    EnvironmentUpdated,
    Message,
    PhotoUploaded,
    UserNameId,
)
from web_backend.security import get_current_admin
from web_backend.utils.file_path import file_path
from web_backend.utils.upload_photo import upload_photo
from web_backend.utils.file_path import file_path

router = APIRouter(prefix='/environments', tags=['environments'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=EnvironmentCreated,
    responses={
        HTTPStatus.CONFLICT: {'model': Message},
        HTTPStatus.UNAUTHORIZED: {'model': Message},
    },
)
def create_environment(
    request: Request,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
    environment: Annotated[EnvironmentSchema, Depends()],
    photo: Annotated[UploadFile | str, File()] = None,
) -> EnvironmentCreated:
    environment_db = session.scalar(
        select(Environment).where(Environment.name == environment.name)
    )

    if environment_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Environment name already in use',
        )

    environment_db = Environment(
        name=environment.name,
        name_unaccent=unidecode(environment.name),
        creator_admin_id=current_admin.id,
    )

    session.add(environment_db)
    session.commit()
    session.refresh(environment_db)

    photo_url = ''
    if not isinstance(photo, str):
        upload_photo(photo, environment_db.id, 'environments_photos')
        photo_url = file_path(environment_db.id, 'environments_photos')
        photo_url = str(request.base_url) + photo_url

    environment_dict = environment_db.as_dict()
    environment_dict['photo_url'] = photo_url
    return environment_dict


@router.get(
    path='/{environment_id}',
    status_code=HTTPStatus.OK,
    response_model=EnvironmentPublicWithPhotoURL,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
    dependencies=[Depends(get_current_admin)],
)
def get_environment_by_id(
    environment_id: int,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> EnvironmentPublicWithPhotoURL:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    file = file_path(environment_db.id, 'environments_photos')
    environment_db.photo_url = ''
    if file:
        environment_db.photo_url = str(request.base_url) + file

    return environment_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Page[EnvironmentPublic],
    dependencies=[Depends(get_current_admin)],
)
def get_environments(
    session: Annotated[Session, Depends(get_session)],
    filters: Annotated[EnvironmentFilter, Depends()],
) -> Page[EnvironmentPublic]:
    query = select(Environment)
    if filters.name:
        query = query.where(
            Environment.name_unaccent.ilike(f'%{unidecode(filters.name)}%')
        )

    query = query.order_by(
        desc(Environment.name)
        if filters.sort_order
        == EnvironmentFilter.AscendingOrDescending.descending
        else asc(Environment.name)
    )
    return paginate(session, query)


@router.delete(
    path='/{environment_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
)
def delete_environment(
    environment_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Message:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    session.delete(environment_db)
    session.commit()

    return {'message': 'Environment deleted successfully!'}


@router.put(
    '/{environment_id}',
    status_code=HTTPStatus.OK,
    response_model=EnvironmentUpdated,
    dependencies=[Depends(get_current_admin)]
)
def update_environment(
    environment_id: int,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    new_environment: Annotated[EnvironmentSchema, Depends()],
    photo: Annotated[UploadFile | str, File()] = None,
) -> EnvironmentUpdated:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    environment_db.name = new_environment.name
    environment_db.name_unaccent = unidecode(new_environment.name)
    session.commit()
    session.refresh(environment_db)

    if not isinstance(photo, str):
        upload_photo(photo, environment_db.id, 'environments_photos')
    
    photo_url = file_path(environment_db.id, 'environments_photos')
    if photo_url:
        photo_url = str(request.base_url) +  photo_url

    environment_dict = environment_db.as_dict()
    environment_dict['photo_url'] = photo_url

    return {
        'message': 'Environment updated successfully!',
        'environment_updated': environment_dict,
    }


@router.get(
    path='/users/{environment_id}',
    status_code=HTTPStatus.OK,
    response_model=Page[UserNameId],
    dependencies=[Depends(get_current_admin)],
)
def get_environment_users(
    environment_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Page[UserNameId]:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found!'
        )

    query = (
        select(User)
        .join(Environment.users)
        .where(Environment.id == environment_id)
    )

    return paginate(session, query)


@router.post(
    path='/upload-image/{environment_id}',
    status_code=HTTPStatus.CREATED,
    response_model=PhotoUploaded,
    dependencies=[Depends(get_current_admin)],
)
def environment_photo_upload(
    environment_id: int,
    session: Annotated[Session, Depends(get_session)],
    request: Request,
    photo: Annotated[UploadFile, File()],
) -> PhotoUploaded:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Environment not found'
        )
    
    upload_photo(photo, environment_id, 'environments_photos')
    photo_url = file_path(environment_db.id, 'environments_photos')
    photo_url = str(request.base_url) +  photo_url

    return {
        'message': 'Image uploaded successfully!',
        'photo_url': photo_url,
    }
