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

station = pd.read_excel("2호선 역 목록.xlsx")
# 역 이름에 # 붙여서 리스트로 저장
station = list(station['총'])
stations = [x for x in station if str(x) != 'nan']
stations

#포스팅 분리
for i in stations:
    try:
        doc = open(i + '.csv', 'r')
        data = doc.read()
        doc.close()
        phrase = data.split('\n')
    except:
        doc = open(i + '.csv', 'r', encoding='utf8')
        data = doc.read()
        doc.close()
        phrase = data.split('\n')

    #포스팅에서 한글 외 문자 제거
    import re
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    #형태소 문장 단위 추출
    dic_Twitter = []
    for i in range(len(phrase)):
        p = hangul.sub(' ', phrase[i])
        s = Twitter().pos(p, stem=True, norm=True)
        dic_Twitter.append(s)

    #총 형태소
    name = doc.name
    hts = []
    for a in range(len(dic_Twitter)):
        s1 = dic_Twitter[a]
        for b in range(len(s1)):
            s2 = s1[b]
            if len(s2[0]) >1 and s2[0] not in ["스타","그램",name[:-4],name[:-5],"이다","있다","없다","같다","아니다","그렇다","이렇다","많다","어떻다",
                                               "스럽다","저렇다", '인스타그램', '맞팔', '선팔', '이벤트', '응모']:
                hts.append(s2)

    #품사-단어 사전만들기
    hts2 = {}
    for x in hts:
        if x[1] not in hts2:
            hts2[x[1]] = []
        hts2[x[1]].append(x[0])

    for x in tw_tag:
        try:
            a=len(hts2[x])
        except:
            continue

    #품사별 단어 빈도 테이블 만들기
    x=pd.DataFrame({'Noun':hts2['Noun']})['Noun'].value_counts().reset_index()
    x.to_excel('ps_ass.xlsx')
    new_tw_tag = ['Noun','Adjective','Adverb','Exclamation']
    for i in new_tw_tag[1:]:
        try:
            x = pd.concat([x, pd.DataFrame({i: hts2[i]})[i].value_counts().reset_index()], axis=1)
        except:
            continue
    x.to_excel('ps_'+name[:-4]+'.xlsx')
print(i+" 완료")
