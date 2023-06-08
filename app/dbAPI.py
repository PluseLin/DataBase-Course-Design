from os import name
from . import db
from .models import *

import os
#from .main.forms import *

import time

# ''' User API '''
def User_Query(username,password):
    if(username is None or password is None):
        return None
    user=User.query.filter_by(
        username=username,password=password
    ).first()
    return user   

def User_Query_by_username(username):
    if(username is None):
        return None
    user=User.query.filter_by(username=username).first()
    return user

def User_Query_by_id(id):
    if(id is None):
        return None
    return User.query.filter_by(id=id).first()

def User_Insert(username,password):
    new_user=User(
        username=username,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()

def User_Update_password(username,password):
    db.session.query(User).filter_by(username=username).update({"password":password})
    db.session.commit()

def User_Update_username(ori_username,new_username):
    db.session.query(User).filter_by(username=ori_username).update({"username":new_username})
    db.session.commit()

""" Linename API """
def LineName_Query_all():
    return LineName.query.all()

def LineName_Query_by_id(lid):
    return LineName.query.filter_by(id=lid).first()

def LineName_Query_by_name(lname):
    return LineName.query.filter_by(name=lname).first()

""" StationName API """
def StationName_Query_all():
    return StationName.query.all()

def StationName_Query_by_name(sname):
    return StationName.query.filter_by(name=sname).first()

def StationName_Query_by_id(id):
    return StationName.query.filter_by(id=id).first()

def StationName_Query_by_substr(substr):
    return StationName.query.filter(
        StationName.name.like(f'%{substr}%')
    ).all()

""" Station API """
def Station_Query_by_id(id):
    return Station.query.filter_by(id=id).first()

def Station_Query_by_snid(snid):
    return Station.query.filter_by(snid=snid).all()

def Station_Query_by_lnid(lnid):
    return Station.query.filter_by(lnid=lnid).all()

def Station_Query_by_snid_and_lnid(snid,lnid):
    return Station.query.filter_by(snid=snid,lnid=lnid).first()

""" Direction API """
def Direction_Query_by_sid(sid):
    return Direction.query.filter_by(sid=sid).all()

""" Picture API """
def Picture_Query_by_sid(sid):
    return Picture.query.filter_by(sid=sid).first()

""" Entrance API """
def Entrance_Query_by_sid(sid):
    return Entrance.query.filter_by(sid=sid).all()

""" Collection API """
def Collection_Query_by_uid_and_sid(uid,sid):
    return Collection.query.filter_by(sid=sid,uid=uid).first()

def Collection_Insert(uid,sid):
    new_collection=Collection(
        uid=uid,
        sid=sid
    )
    db.session.add(new_collection)
    db.session.commit()

def Collection_Query_by_uid(uid):
    return Collection.query.filter_by(uid=uid).all()

def Collection_Delete(uid,sid):
    collection=Collection_Query_by_uid_and_sid(uid,sid)
    if(collection is not None):
        db.session.delete(collection)
        db.session.commit()

def Collection_Delete_by_id(id):
    collection=Collection.query.filter_by(id=id).first()
    if collection is not None:
        db.session.delete(collection)
        db.session.commit()