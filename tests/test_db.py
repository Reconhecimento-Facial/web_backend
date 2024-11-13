from sqlalchemy import select

from web_backend.models import (
    Enviroment,
    Group,
    User,
    UserStatus,
)


def test_create_user(session):
    new_user = User(
        status=UserStatus.disabled,
        username='alice',
        password='secret',
        email='teste@test',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
    assert user.status == UserStatus.disabled
    assert user.email == 'teste@test'
    assert user.password == 'secret'


def test_create_group(session):
    new_group = Group(name='Professores')
    session.add(new_group)
    session.commit()

    group = session.scalar(select(Group).where(Group.name == 'Professores'))

    assert group.name == 'Professores'


def test_create_env(session):
    new_env = Enviroment(name='lab_3')
    session.add(new_env)
    session.commit()

    env = session.scalar(select(Enviroment).where(Enviroment.name == 'lab_3'))

    assert env.name == 'lab_3'
