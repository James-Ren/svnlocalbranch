# -*- coding: utf-8 -*-
import pprint
import svn.local
import os
import shutil
import time
from datetime import datetime
import json
import svnop


def filter_status(status):
    global localpath
    return svnop.filter_status(localpath,status)

def getFilerevision(l,filepath):
    global localpath
    return svnop.getFilerevision(localpath,l,filepath)

def revertFile(l,filepath):
    global localpath
    return svnop.revertFile(localpath,l,filepath)


# configinfo={'project':'E:\\project\\sitepro','svnusername':'renzhen','svnpassword':'rz196#cndns','revert':True}
# with open('config.json','w') as f:    
#     str=json.dumps(configinfo)
#     f.write(str)
# exit()   
with open('config.json','r') as f:  
    strj=f.read()
    configinfo=json.loads(strj)

print("请选择需要的操作：(默认是 1)")
print("1.创建分支")
print("2.合并分支")
theop =input()
try:
    theop=int(theop)
except:
    theop=1
if theop==1:
    localpath=configinfo['project'].replace('/','\\')
    needrevert=configinfo['revert']

    print(f"{localpath} 正在自动创建分支信息")
    now=datetime.now().strftime('%Y%m%d%H%M%S')
    dist=os.path.abspath(f"pybranch\\{now}")

    print("请先进行SVN Update，完成后回车继续(可不做)")
    input()

    if not os.path.isdir(dist):
        os.makedirs(dist)


    l = svn.local.LocalClient(localpath,username=configinfo['svnusername'],password=configinfo['svnpassword'])
    status=l.status()
    status=list(filter(filter_status,status))
    statushash={}
    filearr=[]
    for s in status:
        if os.path.exists(s.name):
            filearr.append(s.name)
            statushash[s.name]=s

    with open('svnchange.txt','w') as f:
        filestr="\n".join(filearr)
        f.write(filestr)

    print("打开目录svnchange.txt 筛选文件！完成后回车")
    input()
    newdiffnames=[]
    with open('svnchange.txt', 'r') as f:
        newdiffnames=filter(None,[s for s in f.read().split("\n")])

    # print(list(status))
    # exit()
    changedstatus=[]
    for filepath2 in newdiffnames:
        s=statushash.get(filepath2)
        if s and (s.type==9 or s.type==1):
            filepath=s.name.replace(localpath,dist) 
            orifilepath=s.name   
            if os.path.isdir(s.name) and not os.path.isdir(filepath):
                os.makedirs(filepath)
            elif os.path.isfile(orifilepath):
                filedir=os.path.dirname(filepath)
                if not os.path.exists(filedir):
                    os.makedirs(filedir)
                if not os.path.exists(filepath):
                    print(f"{s.name} 正在复制")
                    shutil.copy(s.name,filepath)
                    changedstatus.append({'name':s.name,'type':s.type,'revision':s.revision})
                    if needrevert:
                        print(f"{s.name} 正在恢复")
                        if s.type==9:
                            revertFile(l,s.name)
                        else:
                            os.remove(s.name)

    svnjson={'path':localpath,'info':changedstatus}
    with open(dist+"\\svn.json","w") as f:
        f.write(json.dumps(svnjson))
    os.system("explorer.exe "+dist)
    print("建议将当前目录改成有意义的名字，以便日后查看")
    time.sleep(2)
else:
    branchdir=os.path.abspath("pybranch")
    os.system("explorer.exe "+branchdir)
    print("复制要恢复的目录名并粘贴，回车继续")
    thebranch=input()
    thebranch=thebranch.strip()

    # thebranch="20171128135432"

    dist=branchdir+"\\"+thebranch
    jsonfile=dist+"\\svn.json"
    with open(jsonfile,'r') as f:
        jsonstr=f.read()
    svnjson=json.loads(jsonstr)

    localpath=svnjson['path']
    svnchanges=svnjson['info']


    l = svn.local.LocalClient(localpath,username=configinfo['svnusername'],password=configinfo['svnpassword'])

    for change in svnchanges:
        name=change['name']
        rev=change['revision']
        type=change['type']
        copyfilename=name.replace(localpath,dist)
        s=list(l.status(name.replace(localpath,'')))
        if type==1:
            if os.path.isfile(copyfilename) and os.path.exists(name):
                print(f"{name} 添加文件已存在，无法覆盖，建议手动处理")
            elif os.path.isfile(copyfilename):
                filedir=os.path.dirname(name)
                if not os.path.isdir(filedir):
                    os.makedirs(filedir)
                print(f"{name} 正在覆盖")
                shutil.copy(copyfilename,name)
        else:
            if len(s)>0 and s[0].name==name:
                print(f"{name} 已修改，无法覆盖，建议手动处理")
                break
            curfilerev=getFilerevision(l,name)
            if(rev>=curfilerev):
                print(f"{name} 正在覆盖")
                shutil.copy(copyfilename,name)
            else:
                print(f"{name} 已更新，无法覆盖")
                print("1. 还原原版本覆盖后更新 ")
                print("或者不选，直接回车结束")
                ret=input()
                try:
                    ret=int(ret)
                except:
                    ret=0

                if ret==1:
                    curfilerev=getFilerevision(l,name)
                    comargs=['-r',str(rev)]+[name]
                    l.run_command('update',comargs)
                    print(f"{name} 正在覆盖")
                    shutil.copy(copyfilename,name)
                    comargs=['-r',str(curfilerev)]+[name]
                    l.run_command('update',comargs)
                    curfilerev=getFilerevision(l,name)
    print("合并结束，按回车结束")
    input()