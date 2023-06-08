from . import main
from app.main.forms import *
from ..dbAPI import *
from flask import jsonify, render_template,redirect,flash, request,url_for,session

#拦截器
@main.before_request
def check():
    # url=request.path
    # #注册登录：ip:host/ /register
    # #用户界面：ip:host/<username>/...
    # parts=url.split("/")
    # if(url=='/' or url=='/register'):
    #     return None
    # if(len(parts)>=3):
    #     if(not session.get(parts[1])):
    #         return redirect("/")
    # return None
    pass

''' errors '''
# @main.app_errorhandler(404)
# def error404(error):
#     return render_template("errorpage/error_404.html"),404

# @main.app_errorhandler(500)
# def error500(error):
#     return render_template("errorpage/error_500.html"),500

''' login and register '''

#登录作为主页
@main.route('/',methods=['GET','POST'])
def login():
    username=""
    password=""
    form=LoginForm()
    if(form.validate_on_submit()):
        username=form.username.data
        password=form.password.data
        user = User_Query(username,password)
        if(user is None):
            flash('密码或用户名有误！','warning')
        else:
            session[username]=True
            return redirect(url_for('main.index',username=username))
    data={
        "loginform":form
    }
    return render_template('loginpage/login.html',data=data)

#注册
@main.route("/register",methods=['GET','POST'])
def register():
    form=RegisterForm()
    if(form.validate_on_submit()):
        #不需要检查有无空字段，因为DataRequired已保证

        #检查两次密码是否一致
        if(form.password.data!=form.repassword.data):
            flash('两次密码不一致！','warning')
        #检查用户名是否重复
        elif(User_Query_by_username(form.name.data) is not None):
            flash('用户名已存在！','warning')
        #注册成功
        else:
            User_Insert(form.name.data,form.password.data)
            return redirect('/')
    data={
        "registerform":form
    }
    return render_template('loginpage/register.html',data=data)

''' index '''

@main.route("/logout",methods=['POST','GET'])
def logout():
    args=request.args
    username=args.get('username')
    session[username]=False
    return redirect('/')

#登录后主页
@main.route('/index',methods=['GET','POST'])
def index():
    args=request.args
    username=args.get('username')
    data={
        "username":username
    }
    return render_template('indexpage/index.html',data=data)

# 展示所有站点

@main.route('/all_stations',methods=['GET','POST'])
def view_stations():
    args=request.args
    username=args.get('username')
    all_stations={}
    # 查出所有路线
    all_line=LineName_Query_all()
    for line in all_line:
        # 每个路线查出所有站点
        stations=Station_Query_by_lnid(line.id)
        station_names=[]
        for st in stations:
            st_name=StationName_Query_by_id(st.snid)
            station_names.append(st_name.name)
        all_stations[line.name]=station_names
    data={
        "title":"所有站点",
        "stations":all_stations,
        "username":username
    }
    print(data["stations"]["1号线"])
    return render_template('indexpage/all_stations.html',data=data)

# 按照站点查询
@main.route('/station',methods=['GET','POST'])
def view_station():
    args=request.args
    username=args.get('username')
    station_name=args.get('station')
    line_name=args.get('line')
    data=request.get_json()

    # 取出站点的其他线路
    snid=StationName_Query_by_name(station_name).id
    lnid=LineName_Query_by_name(line_name).id
    all_line=[LineName_Query_by_id(st.lnid).name for st in Station_Query_by_snid(snid)]
    sid=Station_Query_by_snid_and_lnid(snid,lnid).id

    if(data is not None):
        uid=User_Query_by_username(username).id
        act=data["action"]
        collection=Collection_Query_by_uid_and_sid(uid,sid)
        if(act=="tagging"):
            if(collection==None):
                Collection_Insert(uid,sid)
                return jsonify({"message":"添加成功！"})
            else:
                return jsonify({"message":"您已添加到常用站点中了！"})
        elif(act=="untagging"):
            if(collection==None):
                return jsonify({"message":"您尚未添加到常用站点！"})
            else:
                Collection_Delete(uid,sid)
                return jsonify({"message":"删除成功！"})
        else:
            return jsonify({"message":"请检查前端代码是否有误！"})
    # 取出站点的首末班车信息
    directions=Direction_Query_by_sid(sid)
    directions=[[d.dire,d.time1,d.time2] for d in directions]
    # 取出站点的图片url
    pic_url=Picture_Query_by_sid(sid).imgurl
    # 取站点的出口名称
    entrances=Entrance_Query_by_sid(sid)
    entrances_name=[]
    for each in entrances:
        span=each.ename.split(" ")
        entrances_name.append([span[0]," ".join(span[1:])])
        
    data={
        "username":username,
        "station_name":station_name,
        "line_name":line_name,
        "all_line":all_line,
        "directions":directions,
        "pic_url":pic_url,
        "entrance":entrances_name
    }

    return render_template('indexpage/station_detail.html',data=data)

@main.route('/info',methods=['GET','POST'])
def info():
    args=request.args
    username=args.get("username")
    form=ResetUsernameForm()
    if(form.validate_on_submit()):
        new_username=form.new_name.data
        # 检查用户名是否重复
        if User_Query_by_username(username=new_username) is not None:
            flash("用户名已存在！",'warning')
        else:
            print(username,new_username)
            User_Update_username(username,new_username)
            username=new_username
            flash("修改成功！",'success')
        return redirect(url_for("main.info",username=username))
    data={
        "username":username,
        "form":form
    }

    return render_template("infopage/info.html",data=data)

@main.route('/info/resetpswd',methods=['GET','POST'])
def editinfo():
    args=request.args
    username=args.get("username")
    form=ResetPasswordForm()
    if(form.validate_on_submit()):
        ori_password=form.ori_password.data
        new_password=form.new_password.data
        new_password_1=form.repassword.data
        # 检查旧密码是否正确
        if User_Query(username=username,password=ori_password) is None:
            flash("旧密码不正确","warning")
        # 检查两次新密码是否一致
        elif new_password!=new_password_1:
            flash("两次密码不一致！","warning")
        else:
            User_Update_password(username,new_password)
            flash("修改成功","success")
        return redirect(url_for("main.editinfo",username=username))
        # 修改密码
    data={
        "form":form,
        "username":username,
    }

    return render_template("infopage/editinfo.html",data=data)

@main.route('/info/collection',methods=['GET','POST'])
def collection():
    args=request.args 
    username=args.get("username")
    ret_data=request.get_json()
    if ret_data is not None:
        cid=int(ret_data["cid"])
        Collection_Delete_by_id(cid)
        return jsonify({"message":"取消标记成功！"})
    uid=User_Query_by_username(username).id
    collections=Collection_Query_by_uid(uid)
    collections_1=[]
    for collection in collections:
        station=Station_Query_by_id(collection.sid)
        st_name=StationName_Query_by_id(station.snid)
        line_name=LineName_Query_by_id(station.lnid)
        collections_1.append(
            {
                "st_name":st_name.name,
                "line_name":line_name.name,
                "cid":collection.id
            }
        )
    data={
        "username":username,
        "collections":collections_1
    }
    return render_template("infopage/collection.html",data=data)
    
@main.route('/search/',methods=['GET','POST'])
def search():
    args=request.args
    username=args.get("username")
    form=SearchForm()
    all_stations=[]
    _search=False
    if form.validate_on_submit():
        # 先查询站点名称
        search_result=StationName_Query_by_substr(form.input.data)
        # 再查询相应的站点名称
        for result in search_result:
            station=Station_Query_by_snid(result.id)
            for st in station:
                line_name=LineName_Query_by_id(st.lnid)
                all_stations.append({
                    "st_name":result.name,
                    "line_name":line_name.name
                })
        _search=True
    data={
        "username":username,
        "stations":all_stations,
        "form":form,
        "search":_search
    }
    print(data)
    return render_template("indexpage/search.html",data=data)