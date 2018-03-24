import pandas as pd
import numpy as np
from konlpy.tag import Twitter
from konlpy.utils import pprint
import time as time
from openpyxl import Workbook
from openpyxl.styles import Font, Side, Border

#품사목록 불러오기
tag = pd.read_excel("pstag.xlsx")
twitter_tag = list(tag['Twitter'])
tw_tag=[x for x in twitter_tag if str(x) != 'nan' ]
tw_tag=tw_tag[2:]


#포스팅 분리
doc = open('삼성역.csv')
data = doc.read()
doc.close()
phrase = data.split('\n')

#포스팅에서 한글 외 문자 제거
import re
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')


#형태소 문장 단위 추출
dic_Twitter = []
for i in range(len(phrase)):
    print(i)
    p = hangul.sub(' ', phrase[i])
    s = Twitter().pos(p, stem=True, norm=True)  ##norm, stem 옵션 추가
    dic_Twitter.append(s)
print(dic_Twitter)


#총 형태소
hts = []
for a in range(len(dic_Twitter)):
    print(a)
    s1 = dic_Twitter[a]
    for b in range(len(s1)):
        s2 = s1[b]
        hts.append(s2)
print(hts)

# 빈도 테이블 작성
hts2 = {}
for x in hts:
    if x[1] not in hts2:
        hts2[x[1]] = []
    hts2[x[1]].append(x[0])

for x in tw_tag:
    try:
        a=len(hts2[x])
        print(x,a)
    except:
        continue

x=pd.DataFrame({'Noun':hts2['Noun']})['Noun'].value_counts().reset_index()
x.to_excel('삼성역.xlsx')

for i in tw_tag[1:]:
    try:
        x = pd.concat([x, pd.DataFrame({i: hts2[i]})[i].value_counts().reset_index()], axis=1)
    except:
        continue
x.to_excel('삼성역_DF.xlsx')

print("==완료==")


