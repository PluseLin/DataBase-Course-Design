from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:012704@localhost/shmetro'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY= "ahsdilwjaidajldjawlidjal"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

app1=Flask(__name__)
app1.config.from_object(Config)
db=SQLAlchemy(app1)

class User(db.Model):
    __tablename__='User'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20))   # 用户名
    password=db.Column(db.String(20))   # 密码

# 标记的站点
class Collection(db.Model):
    __tablename__='Collection'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.Integer,db.ForeignKey('User.id'))
    sid=db.Column(db.Integer,db.ForeignKey('Station.id'))

# 线路
class LineName(db.Model):
    __tablename__='LineName'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(20))

# 站点
class StationName(db.Model):
    __tablename__='StationName'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    # lid=db.Column(db.Integer,db.ForeignKey('Line.id'))
    name=db.Column(db.String(20))

# 站点线路关系
class Station(db.Model):
    __tablename__='Station'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    lnid=db.Column(db.Integer,db.ForeignKey('LineName.id'))
    snid=db.Column(db.Integer,db.ForeignKey('StationName.id'))

# 始末班车时间
class Direction(db.Model):
    __tablename__='Direction'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sid=db.Column(db.Integer,db.ForeignKey('Station.id'))
    dire=db.Column(db.String(32))
    time1=db.Column(db.String(32))
    time2=db.Column(db.String(32))

# 站层图
class Picture(db.Model):
    __tablename__='Picture'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sid=db.Column(db.Integer,db.ForeignKey('Station.id'))
    imgname=db.Column(db.String(20))
    imgurl=db.Column(db.String(512))

# 出口信息
class Entrance(db.Model):
    __tablename__='Entrance'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sid=db.Column(db.Integer,db.ForeignKey('Station.id'))
    ename=db.Column(db.String(100))

def load_data(src):
    with open(src,"r",encoding="utf-8") as f:
        datas=json.load(f)
    return datas

def init():
    # 初始化数据库
    db.drop_all()
    db.create_all()
    # 读取数据
    lines=load_data("data/lines.json")
    stations=load_data("data/stations.json")
    st_details=load_data("data/st_detail.json")
    #加入线路
    for line in lines:
        db.session.add(LineName(
            name=line
        ))
    db.session.commit()
    for st in stations:
        db.session.add(
            StationName(
                name=st
            )
        )
    db.session.commit()
    #加入站点
    for i,station in enumerate(st_details):
        line_name,st_name=station["st_name"].split('_')
        line_name=line_name if line_name=="浦江线" else line_name+"号线"
        lnid=lines.index(line_name)+1
        snid=stations.index(st_name)+1
        sid=i+1
        # 添加几号线的站点
        db.session.add(
            Station(
                lnid=lnid,
                snid=snid
            )
        )
        db.session.commit()
        #添加站层图
        db.session.add(
            Picture(
                sid=sid,
                imgname=station["img"],
                imgurl=station["img_url"]
            )
        )
        # 添加出口信息
        for en in station["entrances"]:
            db.session.add(
                Entrance(
                    sid=sid,
                    ename=en
                )
            )
        # 添加站点首末班车
        idx=1
        while True:
            timestamp=station.get("timestamp_{}".format(idx),None)
            if timestamp==None:break
            db.session.add(
                Direction(
                    sid=sid,
                    dire=timestamp[1],
                    time1=timestamp[2],
                    time2=timestamp[3]
                )
            )
            idx+=1
        db.session.commit()


if __name__=="__main__":
    init()