from orm import model
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                       encoding='utf8', echo=True)
from sqlalchemy.orm import sessionmaker

session = sessionmaker()()


def insertUser(username, password):
    re = session.query(model.User.username).filter(model.User.username == username).all()
    if re == []:
        result = session.add(model.User(username=username, password=password))
        session.commit()
        session.close()
        print(result)
        print("*************************************************************************************************")
        print(re)
        print(re == [])
        return ""
    return "账户已存在"


def checkUser(username, password):
    try:
        result = session.query(model.User).filter(model.User.username == username).filter(
            model.User.password == password).first().id

        return result
    except:
        return -1


def get_good_id():
    result = session.query(model.Goods.id).all()
    if result:
        return result
    else:
        return -1


def add_good(goodname, goodprice, goodintro,goodimg):
    result = session.add(model.Goods(goodname=goodname, goodprice=goodprice, goodintro=goodintro,goodimg=goodimg))
    session.commit()
    session.close()
    print(result)


def change_good(goodid, goodname, goodprice, goodintro,goodimg):
    result = session.query(model.Goods).filter_by(id=goodid).first()
    result.goodname = goodname
    result.goodprice = goodprice
    result.goodintro = goodintro
    result.goodimg = goodimg
    session.commit()
    session.close()
    print(result)


def query_good(goodname):

    result = session.query(model.Goods.id).filter(model.Goods.goodname.like('%{}%'.format(goodname))).all()
    if result:
        return result
    else:
        return -1



def remove_good(goodid):
    result = session.query(model.Goods).filter(model.Goods.id == goodid).first()
    session.delete(result)
    session.commit()
    session.close()


def get_good_intro(goodid):
    result = session.query(model.Goods).filter(model.Goods.id == goodid).first().goodintro
    # jiage = session.query(model.User).filter(model.Goods.goodname == goodname).first().goodprice
    if result:
        return result
    else:
        return -1


def get_good_price(goodid):
    # result = session.query(model.User).filter(model.Goods.goodname == goodname).first().goodintro
    result = session.query(model.Goods).filter(model.Goods.id == goodid).first().goodprice
    if result:
        return result
    else:
        return -1


def get_good_name(goodid):
    # result = session.query(model.User).filter(model.Goods.goodname == goodname).first().goodintro
    result = session.query(model.Goods).filter(model.Goods.id == goodid).first().goodname
    if result:
        return result
    else:
        return -1

def get_good_img(goodid):
    # result = session.query(model.User).filter(model.Goods.goodname == goodname).first().goodintro
    result = session.query(model.Goods).filter(model.Goods.id == goodid).first().goodimg
    if result:
        return result
    else:
        return -1

def get_good_id_one(goodname):
    # result = session.query(model.User).filter(model.Goods.goodname == goodname).first().goodintro
    result = session.query(model.Goods).filter(model.Goods.goodname == goodname).first().id
    if result:
        return result
    else:
        return -1

