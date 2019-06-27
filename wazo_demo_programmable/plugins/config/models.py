# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Config(Base):

    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    number = Column(Text(), nullable=False)
    user_uuid = Column(Text(), nullable=False)
