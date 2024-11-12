from sqlalchemy import select

from web_backend.models import User, Userstatus


def test_create_user(session):
    new_user = User(
        status=Userstatus.active,
        username='alice',
        password='secret',
        email='teste@test',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
