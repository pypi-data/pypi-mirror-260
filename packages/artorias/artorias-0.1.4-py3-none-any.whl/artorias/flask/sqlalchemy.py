import functools
from datetime import datetime
from typing import Any
from typing import Callable
from typing import Self

from sqlalchemy import delete
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from artorias.flask.exts import db


def transaction(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        else:
            return data

    return wrapper


class Model(db.Model):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs) -> Self:
        instance = cls(**kwargs)
        db.session.add(instance)
        return instance

    def set(self, **kwargs) -> None:
        for field, value in kwargs.items():
            if not hasattr(self, field):
                continue
            setattr(self, field, value)


class PkModel(Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-999)

    @classmethod
    def get_by_pk(cls, pk: int):
        return db.session.get(cls, pk)

    @classmethod
    def get_or_404(cls, pk: int):
        return db.get_or_404(cls, pk)

    @classmethod
    def delete_by_pk(cls, pk: int):
        return db.session.execute(delete(cls).where(cls.id == pk))


class TimeModel(Model):
    __abstract__ = True

    create_at: Mapped[datetime] = mapped_column(default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
