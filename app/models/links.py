
from fastapi import FastAPI
from sqladmin import Admin, ModelView

from sqlalchemy.orm import Mapped, mapped_column
from db.session import Base

class LinksOrm(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    timestamp: Mapped[int]

class LinksAdminView(ModelView, model = LinksOrm):
    can_create = True

    column_list = ('id', 'link', 'timestamp')
    form_columns = ('id', 'link', 'timestamp')


def setup_admin(app: FastAPI, engine):
    admin = Admin(app, engine, title='Admin panel')

    admin.add_view(LinksAdminView)