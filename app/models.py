#! .venv/bin/python

from datetime import datetime, timezone
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

    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author')

    def __repr__(self) -> str:
        return f'User: {self.username}; Email: {self.email}'
    

class Post(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    body: orm.Mapped[str] = orm.mapped_column(sql.String(144))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(index=True,
                                        default=lambda: datetime.now(timezone.utc))
    user_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey(User.id),
                                                 index=True)
    
    author: orm.Mapped[User] = orm.relationship(back_populates='posts')
