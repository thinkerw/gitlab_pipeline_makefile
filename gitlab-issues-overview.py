# -*- coding: utf-8 -*-
__Author__ = "Thinker Wu"
__Date__ = '2021/08/03 16:36'

"""
gitlab经常使用的api
DOC_URL: http://python-gitlab.readthedocs.io/en/stable/
LOCAL_PATH: C:\Python36\Lib\site-packages\gitlab
from gitlab.v4.objects.groups import GroupSubgroup
增加commit times、Summary 2021-8-19
"""
import gitlab
import urllib3
from jsonpath import jsonpath
import pandas as pd
from tabulate import tabulate
import json
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

# gitlab group
groups = gl.groups.list(visibility='public',search='SBG2',sort='desc')

# get group project issues all closed opened
gr = "\"Group\":["
pr = "\"Project\":["
al = "\"All\":["
op = "\"opened\":["
cl = "\"closed\":["
lo = "\"Last Week Open\":["
lc = "\"Last Week Closed\":["
ct = "\"Commit times\":["

# 用于统计Summary
s_al = 0
s_op = 0
s_cl = 0
s_lo = 0
s_lc = 0
s_ct = 0

# 当前日期
deline = (datetime.datetime.now()).strftime("%Y-%m-%d")
commitDate = (datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%Y-%m-%d")

for g in groups:
    print("Group name:" + g.name)
    # print(g.issues.list())
    # print(g.issues_statistics.get())
    # get group issues all closed opened
    print(g)
    
    all = jsonpath(g.issues_statistics.get().statistics,'$..all')
    closed = jsonpath(g.issues_statistics.get().statistics,'$..closed')
    opened = jsonpath(g.issues_statistics.get().statistics,'$..opened')
    
    print("--issues all:" + str(all[0])) 
    print("--issues closed:" + str(closed[0]))
    print("--issues opened:" + str(opened[0]))
    
    # 获取group对应的issues 统计上周的new issues
    issues = g.issues.list(state='opened')
    print(issues)
    # 如果当前时间减去issue的创建时间<=7，则统计进new issues
    var1 = 0
    for ii in issues:
        d1 = pd.to_datetime(deline, utc=True)
        d2 = pd.to_datetime(ii.created_at, utc=True)   # 第二个日期
        if (d1 - d2).days <= 7:       # 具体的天数    
            var1 = var1 + 1
            print(var1)                 
            print(ii)
    
    # 获取group对应的issues 统计上周的closed issues
    issues = g.issues.list(state='closed')
    print(issues)
    # 如果当前时间减去issue的创建时间<=7，则统计进new issues
    var2 = 0
    for ii in issues:
        d1 = pd.to_datetime(deline, utc=True)
        d2 = pd.to_datetime(ii.closed_at, utc=True)   # 第二个日期
        if (d1 - d2).days <= 7:       # 具体的天数    
            var2 = var2 + 1  
            print(var2)               
            print(ii)
    
    # 添加每一个group
    gr = gr + "\"" + g.name + "\"" + ","
    # 每一个group都要加一个空的project,因为有group的时候没project，如 "Group": [cloudplatform,'','']  "Project": ['',Chanty_Operation, faq] 
    pr = pr + "\"\","
    # 添加每一个group对应的all closed opened
    al = al + str(all[0]) + ","
    op = op + str(opened[0]) + ","
    cl = cl + str(closed[0]) + "," 
    lo = lo + str(var1) + "," 
    lc = lc + str(var2) + ","
    ct = ct + "\"\","
    
    # 累计Summary的数据
    s_al = s_al + all[0]
    s_op = s_op + opened[0]
    s_cl = s_cl + closed[0]
    s_lo = s_lo + var1
    s_lc = s_lc + var2
    
    stat = g.issues_statistics.get()
    for p in g.projects.list(visibility='public'):
        print("----Project name:" + p.name)
        
        # print(p.id)
        # print(p)
        project = gl.projects.get(p.id, visibility='public',lazy=True)

        statistics = project.issues_statistics.get()
        
        # get project issues all closed opened
        all = jsonpath(project.issues_statistics.get().statistics,'$..all')
        closed = jsonpath(project.issues_statistics.get().statistics,'$..closed')
        opened = jsonpath(project.issues_statistics.get().statistics,'$..opened')
        
        print("------issues all:" + str(all[0])) 
        print("------issues closed:" + str(closed[0]))
        print("------issues opened:" + str(opened[0]))
        
        # 获取group对应的issues 统计上周的new issues
        issues = project.issues.list(state='opened')
        print(issues)
        # 如果当前时间减去issue的创建时间<=7，则统计进new issues
        var1 = 0
        for ii in issues:
            d1 = pd.to_datetime(deline, utc=True)
            d2 = pd.to_datetime(ii.created_at, utc=True)   # 第二个日期
            if (d1 - d2).days <= 7:       # 具体的天数    
                var1 = var1 + 1
                print(var1)                 
                print(ii)
        
        # 获取group对应的issues 统计上周的closed issues
        issues = project.issues.list(state='closed')
        print(issues)
        # 如果当前时间减去issue的创建时间<=7，则统计进new issues
        var2 = 0
        for ii in issues:
            d1 = pd.to_datetime(deline, utc=True)
            d2 = pd.to_datetime(ii.closed_at, utc=True)   # 第二个日期
            if (d1 - d2).days <= 7:       # 具体的天数    
                var2 = var2 + 1  
                print(var2)           
                print(ii)

        # 每个project从committed_date开始的commit times
        # print("commitDate:" + str(commitDate))
        commits = project.commits.list(all=True,since=commitDate)
        var3 = 0
        for co in commits:
            var3 = var3 + 1
        
        # 累计Summary的数据
        s_ct = s_ct + var3 
           
        # print(statistics)
        # 每一个project都要加一个空的group,因为有project的时候没group，如 "Group": ['']  "Project": ['baikai'] 
        gr = gr + "\"\","
        # 每一个group都要加一个空的project,因为有group的时候没project，如 "Group": [cloudplatform,'','']  "Project": ['',Chanty_Operation, faq] 
        pr = pr + "\"" + p.name + "\"" + ","
        # 添加每一个group对应的all closed opened
        al = al + str(all[0]) + ","
        op = op + str(opened[0]) + ","
        cl = cl + str(closed[0]) + "," 
        lo = lo + str(var1) + "," 
        lc = lc + str(var2) + ","
        ct = ct + str(var3) + ","    
        
# summary line 汇总
gr = gr + "\"Summary\"" + ","
pr = pr + "\"\","
al = al + str(s_al) + ","
op = op + str(s_op) + ","
cl = cl + str(s_cl) + "," 
lo = lo + str(s_lo) + "," 
lc = lc + str(s_lc) + ","
ct = ct + str(s_ct) + ","   

gr = gr[:-1] + "]"
pr = pr[:-1] + "]"
al = al[:-1] + "]"
op = op[:-1] + "]"
cl = cl[:-1] + "]" 
lo = lo[:-1] + "]" 
lc = lc[:-1] + "]"
ct = ct[:-1] + "]"
    
# 字典格式的JSON                                                                                              
data = "{" + gr + "," + pr + "," + al + "," + op + "," + cl + "," + lo + "," + lc + "," + ct + "}"  
dd = json.loads(data)

df = pd.DataFrame(dd)

print(df.to_markdown(index=False))

# print(tabulate(df, tablefmt="pipe", headers="keys"))


