from sqlalchemy import select

from web_backend.models import Admin
from web_backend.security import get_password_hash, verify_password


def test_create_admin(session):
    new_admin = Admin(
        email='teste@example.com',
        password=get_password_hash('teste'),
    )

    session.add(new_admin)
    session.commit()

    admin = session.scalar(
        select(Admin).where(Admin.email == 'teste@example.com')
    )
    
    assert admin is not None    
    assert admin.email == 'teste@example.com'
    assert verify_password('teste', admin.password) == True
    assert admin.super_admin == False
