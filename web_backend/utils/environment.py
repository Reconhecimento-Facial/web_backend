from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from web_backend.models import Device, Environment


def relate_devices_to_environment(
    session: Session,
    environment_db: Environment,
    devices_ids: list[UUID] | None = None,
) -> list[Device]:
    """
    Take a list of devices_ids and relate the
    valid ones to the specified environment.

    Return a list of added devices.
    """
    if not devices_ids:
        return ['']
    
    devices_to_relate = session.scalars(
        select(Device).where(Device.id.in_(devices_ids))
    ).all()

    environment_db.devices = devices_to_relate
    session.commit()

    return devices_to_relate
