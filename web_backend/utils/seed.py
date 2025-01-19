from random import randint, choice

from faker import Faker
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from unidecode import unidecode

from web_backend.models import Admin, Environment, User, AccessLog
from web_backend.models.user_environment import association_table
from web_backend.security import get_password_hash
from web_backend.settings import Settings

faker = Faker('pt_BR')
engine = create_engine(Settings().DATABASE_URL)


def create_access_logs(
    users: list[User], environments: list[Environment], session: Session
) -> None:
    for user in users:
        for _ in range(randint(1, 5)):
            environment = choice(environments)
            allowed_access = choice([True, False])
            new_log = AccessLog(
                user_id=user.id,
                user_name=user.name,
                user_name_unaccent=user.name_unaccent,
                user_email=user.email,
                user_cpf=user.cpf,
                user_phone_number=user.phone_number,
                environment_id=environment.id,
                environment_name=environment.name,
                environment_name_unaccent=environment.name_unaccent,
                allowed_access=allowed_access,
            )
            session.add(new_log)

    session.commit()


def create_users(
    how_many_users: int,
    admin: Admin,
    environments: list[Environment],
    session: Session,
) -> None:
    user_status = ['active', 'inactive']

    users = []
    for _ in range(how_many_users):
        name = faker.name()
        user_environments = environments[: randint(0, len(environments))]
        new_user = User(
            name=name,
            name_unaccent=unidecode(name),
            email=faker.email(),
            date_of_birth=faker.date_of_birth(),
            cpf=faker.cpf(),
            phone_number=faker.phone_number(),
            status=user_status[randint(0, 2) % 2],
            registered_by_admin_id=admin.id,
        )
        session.add(new_user)
        for environment in user_environments:
            new_user.environments.append(environment)

        session.refresh(new_user)
        users.append(new_user)

    session.commit()

    return users


def create_environments(admin: Admin, session: Session) -> list[Environment]:
    env_names = [
        'Laboratório 1',
        'Laboratório 2',
        'Mini Auditório',
        'Sala de Aula 1',
        'Sala de Aula 2',
        'Laboratório Richard BellmanEASY',
        'TOCA',
        'TIPS',
    ]

    environments = []
    for name in env_names:
        new_env = Environment(
            name=name, name_unaccent=unidecode(name), creator_admin_id=admin.id
        )
        session.add(new_env)
        session.commit()
        session.refresh(new_env)
        environments.append(new_env)

    return environments


def create_admin(session: Session) -> Admin:
    hashed_password = get_password_hash('adm123')
    admin = Admin(
        name='Admin',
        email='admin@mail.com',
        password=hashed_password,
        date_of_birth='10/03/2000',
        cpf='123.456.789-01',
        phone_number='82999999999',
        super_admin=True,
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin


def delete_records(session: Session) -> None:
    session.execute(delete(association_table))
    session.execute(delete(AccessLog))
    session.execute(delete(User))
    session.execute(delete(Environment))
    session.execute(delete(Admin))
    session.commit()


if __name__ == '__main__':
    with Session(engine) as session:
        delete_records(session)
        admin = create_admin(session)
        environments = create_environments(admin, session)
        users = create_users(200, admin, environments, session)
        create_access_logs(users, environments, session)
