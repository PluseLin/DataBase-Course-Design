from . import db

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
