from enum import Enum

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db import metadata

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Text)
    is_admin = sa.Column(sa.Boolean, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('username'),
    )


class Message(Base):
    __tablename__ = 'messages'

    class MessageStatuses(Enum):
        PUBLISHED = 'PUBLISHED'
        SCHEDULED = 'SCHEDULED'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.Text, nullable=False)

    status = sa.Column(sa.String(16), nullable=False)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = relationship('User')

    datetime = sa.Column(sa.DateTime, nullable=False)
    created = sa.Column(sa.DateTime, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('url'),
    )
