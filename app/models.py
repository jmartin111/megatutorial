#! .venv/bin/python

from typing import Optional
import sqlalchemy as sql
import sqlalchemy.orm as orm
from app import db

class User(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(
                                sql.String(64),
                                index=True, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(sql.String(120),
                                               index=True, unique=True)
    pw_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sql.String(256))

    def __repr__(self) -> str:
        return f'User: {self.username}; Email: {self.email}'
