# -*- coding: utf-8 -*-
import pprint
import svn.local
import os
import shutil
import time
from datetime import datetime
import json
def filter_status(localpath,status):
    includedirs=[]
    excludedirs=['data/','upload/','picserver','filter/','load.php',
    'cachecheck.php','config.php','admin/','nbproject','editlog/']
    if os.path.isdir(status.name):
        return False
    name=status.name.replace('\\','/')
    for indirs in includedirs:
        thedirs=os.path.join(localpath,indirs).replace('\\','/')
        if not name.startswith(thedirs):
            return False
    for exdirs in excludedirs:
        thedirs=os.path.join(localpath,exdirs).replace('\\','/')
        if name.startswith(thedirs):
            return False
    return True

def getFilerevision(localpath,l,filepath):
    relpath=filepath.replace(localpath,'')
    info=l.info(relpath)
    return info['commit_revision']

def revertFile(localpath,l,filepath):
    relpath=filepath.replace(localpath,'')
    cmd=[]
    cmd += [filepath]
    l.run_command('revert', cmd)