from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()
