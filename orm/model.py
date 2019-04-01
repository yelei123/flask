"""
ORM :O 用于生产数据库中表
"""



from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                       encoding='utf8', echo=True)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(bind=engine)

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)

class Goods(Base):
    __tablename__ = "good"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    goodname = Column(String(20), nullable=False)
    goodintro = Column(String(50), nullable=False)
    goodimg = Column(String(500), nullable=False)
    goodprice = Column(Integer, nullable=False)

if __name__ == "__main__":
    # 创建表  必须卸载main模块
    Base.metadata.create_all(bind=engine)
