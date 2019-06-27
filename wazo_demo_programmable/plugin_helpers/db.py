# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Text, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database


Session = scoped_session(sessionmaker())


def init_db(db_uri):
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        print('Create DB...')
        create_database(engine.url)
        metadata = MetaData(engine)
        config = Table('config', metadata,
            Column('id', Integer(), primary_key=True),
            Column('number', Text(), nullable=False),
            Column('user_uuid', Text(), nullable=False),
        )
        metadata.create_all()
    Session.configure(bind=engine)


def daosession(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        session = Session()
        return func(session, *args, **kwargs)
    return wrapped


@daosession
def get_dao_session(session):
    return session


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        Session.remove()
