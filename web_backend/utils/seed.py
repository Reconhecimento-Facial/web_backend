import time
from datetime import datetime, timedelta
from random import choice, randint

from faker import Faker
from sqlalchemy import create_engine, delete, text
from sqlalchemy.orm import Session
from unidecode import unidecode

from web_backend.models import AccessLog, Admin, Device, Environment, User
from web_backend.models.user_environment import association_table
from web_backend.security import get_password_hash
from web_backend.settings import Settings

faker = Faker('pt_BR')
engine = create_engine(Settings().DATABASE_URL)


def create_devices(
    how_many_devices: int,
    admin: Admin,
    environments: list[Environment],
    session: Session,
) -> list[Device]:
    print('Creating Devices...', end='')
    devices = []
    for _ in range(how_many_devices):
        serial_number = faker.unique.ean13()
        environment = choice(environments)
        new_device = Device(
            serial_number=serial_number,
            environment_id=environment.id,
            environment=environment,
            creator_admin_id=admin.id,
        )
        session.add(new_device)
        session.commit()
        session.refresh(new_device)
        devices.append(new_device)

    print(' OK')
    return devices


def create_access_logs(
    users: list[User], environments: list[Environment], session: Session
) -> None:
    print('Creating Access Logs...', end='')
    logs = []

    for environment in environments:
        environment.last_accessed_by_user_id = choice(users).id
        environment.last_access_time = datetime.now() - timedelta(
            days=randint(0, 30),
            hours=randint(0, 23),
            minutes=randint(0, 59),
            seconds=randint(0, 59),
        )

    for user in users:
        user.last_accessed_environment_id = choice(environments).id
        user.last_access_time = datetime.now() - timedelta(
            days=randint(0, 30),
            hours=randint(0, 23),
            minutes=randint(0, 59),
            seconds=randint(0, 59),
        )
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
            new_log.access_time = datetime.now() - timedelta(
                days=randint(0, 30),
                hours=randint(0, 23),
                minutes=randint(0, 59),
                seconds=randint(0, 59),
            )
            logs.append(new_log)

    logs.sort(key=lambda log: log.access_time)
    session.add_all(logs)
    session.commit()
    print(' OK')


def create_users(
    how_many_users: int,
    admin: Admin,
    environments: list[Environment],
    session: Session,
) -> list[User]:
    print('Creating Users...')
    user_status = ['active', 'inactive']

    users = []

    start_time = time.time()  # Marca o início do processo
    last_print_time = start_time

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
        for environment in user_environments:
            new_user.environments.append(environment)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        users.append(new_user)

        current_time = time.time()
        if current_time - last_print_time >= 1:
            print('.', end='', flush=True)
            last_print_time = current_time

    print(' OK')
    return users


def create_environments(admin: Admin, session: Session) -> list[Environment]:
    print('Creating Environments...', end='')
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

    print(' OK')
    return environments


def create_admin(session: Session) -> Admin:
    print('Creating Admin...', end='')
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

    print(' OK')
    return admin


def delete_records(session: Session) -> None:
    print('Deleting records...', end='')
    session.execute(delete(association_table))
    session.execute(delete(AccessLog))
    session.execute(delete(Device))
    session.execute(text("UPDATE environments SET last_accessed_by_user_id = NULL"))
    session.execute(delete(User))
    session.execute(delete(Environment))
    session.execute(delete(Admin))
    session.commit()
    print(' OK')


if __name__ == '__main__':
    with Session(engine) as session:
        delete_records(session)
        admin = create_admin(session)
        environments = create_environments(admin, session)
        users = create_users(100, admin, environments, session)
        create_access_logs(users, environments, session)
        devices = create_devices(20, admin, environments, session)
