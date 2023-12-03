# -*- coding: utf-8 -*-
# @Time    : 2023/12/1 18:41
# @Author  : 逝不等琴生
# @File    : database_utils.py
# @PROJECT_NAME: DeveloperRelationCrawler
# @Software: PyCharm
import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:1234567@localhost/gh_user')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    login = Column(String(255))
    name = Column(String(255))
    company = Column(String(255))
    blog = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    bio = Column(String(255))
    public_repos = Column(Integer)
    followers = Column(Integer)
    following = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    record_time = Column(DateTime)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)


class Database:
    def __init__(self):
        Base.metadata.create_all(engine)

    def add_or_update(self, new_user: User):
        session = Session()
        user = session.query(User).filter_by(id=new_user.id).first()
        if not user:
            session.add(new_user)
            session.commit()
        else:
            user.login = new_user.login
            user.name = new_user.name
            user.company = new_user.company
            user.blog = new_user.blog
            user.location = new_user.location
            user.email = new_user.email
            user.bio = new_user.bio
            user.public_repos = new_user.public_repos
            user.followers = new_user.followers
            user.following = new_user.following
            user.created_at = new_user.created_at
            user.updated_at = new_user.updated_at
            session.commit()
        session.close()

    def add_user(self, new_user: User):
        session = Session()
        session.add(new_user)
        session.commit()
        session.close()

    def get_user(self, user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user

    def update_user(self, user_id, new_user: User):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user = new_user
            session.commit()
        session.close()

    def delete_user(self, user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
        session.close()
