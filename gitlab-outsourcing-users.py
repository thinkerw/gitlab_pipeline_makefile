# -*- coding: utf-8 -*-
# 超过设置时间没活动的用户blocked处理，用来管理外包人员的账号
__Author__ = "Thinker Wu"
__Date__ = '2021/08/12 16:36'
 
"""
gitlab经常使用的api
DOC_URL: http://python-gitlab.readthedocs.io/en/stable/
LOCAL_PATH: C:\Python36\Lib\site-packages\gitlab
from gitlab.v4.objects.groups import GroupSubgroup
from _ast import If
from tkinter.constants import ACTIVE
"""
import gitlab
import urllib3
import datetime
 
urllib3.disable_warnings()

# 测试环境
# url = 'http://172.22.50.175/'
# token = 'p2LTzKVKdr1Y8uGUc95p'

# kubernetes环境
url = 'https://gitlab.dev.21vianet.com'
token = 'SzNSh4hxtLuqFWseDAXp'
 
# 登录
gl = gitlab.Gitlab(url, token)

# 需要修改加减的天数,如下代码为7
deline = (datetime.datetime.now()+datetime.timedelta(days=-14)).strftime("%Y-%m-%d")
print(deline)      

# 取出所有的用户,active and deactive
# users = gl.users.list(all=True)
users = gl.users.list(search='-os')

# 把活动用户名append到动态数组
activeList = []

# 获取设置的时间后的所有活动用户
activities = gl.user_activities.list(
    query_parameters={'from': deline},
    all=True, as_list=False)

for ac in activities:
    print("active:" + ac.username)
    activeList.append(ac.username) 
    
print ('activeList size: ', str(len(activeList)))

msg = "block user:["

for u in users:
    if u.username not in activeList:
        msg = msg + str(u.username) + ","
        # block user的状态
        u.block()
    else:
        print("Nothing user is being blocked.")


msg = msg[:-1] + "]"
print(msg)
