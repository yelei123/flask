from flask import Flask, render_template, request, redirect, make_response
import datetime
from orm import ormmanage

app = Flask(__name__)
# 配置缓存更新时间
app.send_file_max_age_default = datetime.timedelta(seconds=1)
app.debug = True


# 登录界面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error='')
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # 查询数据库
        # print(username,password)
        # return "登录成功"

        # 内容需要查询数据库
        # 第一种 不带接口
        # return render_template("list.html",infoarray = [1,2,3,4,5])
        # 第二种 带接口 重定向
        # 自动在URL 发起请求 请求list

        # 为了让响应可以携带头信息 ，需要构造响应
        try:
            result = ormmanage.checkUser(username, password)
            if result == -1:
                print("111111111111111111111111111111111111111111111111111111111111111111111111111111111")
                return render_template("login.html", error=1)
            res = make_response(redirect('/list'))
            res.set_cookie('id', str(result), expires=datetime.datetime.now() + datetime.timedelta(days=7))
            print("登录成功")
            return res
        except:
            return render_template("login.html", error=1)


# 注册界面
@app.route("/regist", methods=["POST", "GET"])
def regist():
    if request.method == "GET":
        # print(name, value1)
        # print('收到get请求','返回注册页面')
        return render_template("regist.html")
    elif request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("regist.html", error="两次密码输入不一致")
        # print(username, password)
        # print('收到post请求', '可以提取表单参数')
        # return  "注册成功"
        # 自动在URL 发起请求 请求list

        try:
            error = ormmanage.insertUser(username, password)
            print(error)
            if error == '':
                return redirect('/login')
            return render_template("regist.html", error=error)
        except:
            error = "异常出错"
            return render_template("regist.html", error=error)


# 数据列表
@app.route('/')
@app.route("/list")
def list():
    user = None
    user = request.cookies.get("id")
    dirc = {}
    good_list = ormmanage.get_good_id()
    for i in good_list:
        id = i[0]
        dirc2 = {}
        good_intro = ormmanage.get_good_intro(id)
        good_price = ormmanage.get_good_price(id)
        good_name = ormmanage.get_good_name(id)
        good_img = ormmanage.get_good_img(id)
        dirc2["good_intro"] = good_intro
        dirc2["good_price"] = good_price
        dirc2["good_name"] = good_name
        dirc2["good_img"] = good_img
        dirc[id] = dirc2
    # 内容需要查询数据库
    return render_template("list.html", infoarray=dirc, userinfo=user)


# 数据内容
@app.route("/detail/<id>")
def detail(id):
    user = None
    user = request.cookies.get("id")
    good_intro = ormmanage.get_good_intro(id)
    good_price = ormmanage.get_good_price(id)
    good_name = ormmanage.get_good_name(id)
    good_img = ormmanage.get_good_img(id)
    # 从数据库查询商品详情
    return render_template("detail.html", good_intro=good_intro, good_price=good_price, good_id=id, good_name=good_name,
                           userinfo=user, good_img=good_img)


# 添加商品
@app.route("/addgood", methods=["GET", "POST"])
def add_good():
    user = None
    user = request.cookies.get("id")
    if request.method == "GET":
        # print(name, value1)
        # print('收到get请求','返回注册页面')
        return render_template("addgood.html", userinfo=user)
    elif request.method == "POST":

        good_name = request.form["goodname"]
        good_intro = request.form["goodintro"]
        good_price = request.form["goodprice"]
        good_img = request.form["imgfile"] + request.form["imgname"]

        ormmanage.add_good(good_name, good_price, good_intro, good_img)

        return redirect('/list')


# 查询商品
@app.route("/querygood", methods=["GET", "POST"])
def query_good():
    user = None
    user = request.cookies.get("id")
    dirc = {}
    if request.method == "GET":
        return render_template("querygood.html", infoarray=dirc, userinfo=user)
    elif request.method == "POST":
        good_name = request.form["goodname"]
        good_list = ormmanage.query_good(good_name)
        if good_list == -1:
            return render_template("querygood.html", infoarray=dirc, error=1, userinfo=user)
        # good_list = ormmanage.get_good_id()
        for i in good_list:
            id = i[0]
            dirc2 = {}
            good_intro = ormmanage.get_good_intro(id)
            good_price = ormmanage.get_good_price(id)
            good_name = ormmanage.get_good_name(id)
            good_img = ormmanage.get_good_img(id)
            dirc2["good_intro"] = good_intro
            dirc2["good_price"] = good_price
            dirc2["good_name"] = good_name
            dirc2["good_img"] = good_img
            dirc[id] = dirc2

        return render_template("querygood.html", infoarray=dirc, error='', userinfo=user)


# 修改商品
@app.route("/changegood/<id>", methods=["GET", "POST"])
def change_good(id):
    if request.method == "GET":
        good_name = ormmanage.get_good_name(id)
        good_intro = ormmanage.get_good_intro(id)
        good_price = ormmanage.get_good_price(id)
        print("aaaa")
        return render_template("changegood.html", good_id=id, good_name=good_name, good_intro=good_intro,
                               good_price=good_price)
    elif request.method == "POST":
        print("sssss")
        good_name = request.form["goodname"]
        good_intro = request.form["goodintro"]
        good_price = request.form["goodprice"]
        good_img = request.form["imgfile"] + request.form["imgname"]
        # pic = request.form["pic"]
        # print(pic)
        ormmanage.change_good(id, good_name, good_price, good_intro, good_img)
        return redirect('/detail/{}'.format(id))


# 删除商品
@app.route("/removegood", methods=["GET", "POST"])
def remove_good():
    if request.method == "GET":
        return render_template("removegood.html")
    elif request.method == "POST":
        goodid = request.form["goodid"]
        try:
            ormmanage.remove_good(goodid)
            return redirect('/list')
        except:
            return redirect("/removegood")


# 用户退出
@app.route("/quit")
def quit():
    res = make_response(redirect("/list"))
    res.delete_cookie("id")
    return res


if __name__ == '__main__':
    app.run(host="192.168.12.158", port=8888)
