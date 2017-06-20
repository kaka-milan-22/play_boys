#!/usr/bin/python
#coding:utf-8

import MySQLdb
import sys
import json

__author__ = 'laopangzhang'


reload(sys)
sys.setdefaultencoding('utf-8')


HOST = {}
PROJSQL = "select p.application_name,h.address,h.dxip,h.hostname from project as p\
    left join proj_ser as ps on ps.proj_id = p.id\
    left join hostinfo as h on ps.host_id = h.id\
    where isShow = 1\
    order by application_name; "

GETALLHOST = "select hostname from hostinfo;"

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="root123",db="cmdb",charset="utf8")
cursor = conn.cursor()


def getHostVars():
    global HOST
    HOST["_meta"] = {}
    HOST["_meta"] ["hostvars"] = {}
    count = cursor.execute(GETALLHOST)
    results = cursor.fetchall()
    for r in results:
        hostname = r[0]
        HOST["_meta"]["hostvars"][hostname] = {}
        HOST["_meta"]["hostvars"][hostname]['hostname'] = hostname
        # print HOST["_meta"]["hostvars"][hostname]['hostname']



def getHosts():
    global HOST
    count = cursor.execute(PROJSQL)
    results = cursor.fetchall()
    for r in results:
        hostname = r[3]
        groupname = "%s-%s" % (hostname[0:2],r[0])
        if not HOST.has_key(groupname):
            HOST[groupname] = {}
            HOST[groupname] = []
            HOST[groupname].append(hostname)
        else:
            HOST[groupname].append(hostname)



def setGroups():
    global HOST
    count = cursor.execute(PROJSQL)
    results = cursor.fetchall()
    for r in results:
        groupList = ("dg-%s,vn-%s,hk-%s,th-%s,sg-%s" % (r[0],r[0],r[0],r[0],r[0])).split(",")
        HOST[r[0]] = {}
        HOST[r[0]]['hosts'] = []
        HOST[r[0]]['children'] = []
        for g in groupList:
            if HOST.has_key(g):
                HOST[r[0]]['children'].append(g)



if __name__  == "__main__":
    getHostVars()
    getHosts()
    setGroups()
    print json.dumps(HOST)
    cursor.close()
    conn.close()
