import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


url_pages = "https://www.ptt.cc/bbs/Stock/index.html"

#收集時間 推噓 計數資料
date=[]
push=[]
count=0
pages = 300
for p in range(pages):
    r1 = requests.get(url_pages)
    source_page = BeautifulSoup(r1.text, "html.parser")
    #得到每篇文的資料迴圈
    sel = source_page.find_all("div","r-ent")
    #print(sel)
    for s in sel:
        #每篇文之日期
        dates = s.find_all("div","date")[0].text
        date.append(dates)
        #每篇文的推噓數量
        pushs = s.find_all("div","nrec")[0].text
        if pushs.find("X") == 0:
            push.append(0)
            count += 1
        elif pushs.find("爆") == 0:
            push.append(99)
            count += 1
        elif pushs == '':
            push.append(0)
            count += 1
        else:
            push.append(int(pushs))
            count += 1
        print(count)
    #print(push)
    #print(date)
    #得到上頁網址
    sel_prev = source_page.select("div.btn-group.btn-group-paging a")
    prev = "https://www.ptt.cc" + sel_prev[1]['href']
    url_pages = prev
#計算每天聲量資料

df=pd.DataFrame()
df['dates']=date
df['pushs']=push
df['total'] = df.groupby('dates').transform('sum')
#print(df)
sns.lineplot(data=df, x="dates", y="total")
plt.xticks(rotation=90)
plt.show()



