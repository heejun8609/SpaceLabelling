import pandas as pd
import numpy as np
from konlpy.tag import Twitter, Komoran, Kkma, Hannanum
from konlpy.utils import pprint
import time as time
from collections import Counter

#'2호선 역 목록' 파일에 있는 역 목록 소환.
station_list = pd.read_excel('2호선 역 목록.xlsx')
autostation = []
for station in station_list['2호선 역 목록'][0:50]:
    autostation.append(station)
print(autostation)

#역 자동화 시작 (한 역이 끝나면 자동으로 역목록에 있는 다음역으로 넘어가서 process 반복. 아래 참조)
stlist =[]
for station in autostation:
    try:
        doc = open(station+'.csv','r')
        data = doc.read()
        doc.close()
    except:
        doc = open(station + '.csv', 'r', encoding="utf-8")
        data = doc.read()
        doc.close()
    phrase = data.split('\n')

    #포스팅에서 한글 외 문자 제거
    import re
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    #형태소 추출
    dic_Twitter = []
    dic_Twitter2 = []
    for i in range(len(phrase)):
        p = hangul.sub(' ', phrase[i])
        s = Twitter().pos(p,norm=True, stem=True)
        dic_Twitter.append(s)
        dic_Twitter2.append(" ".join([k[0] for k in s]))
    print("==완료==")
    dic_Twitter2

    #총 형태소/ data cleansing
    name = doc.name
    hts = []
    for a in range(len(dic_Twitter)):
        s1 = dic_Twitter[a]
        for b in range(len(s1)):
            s2 = s1[b]
            if len(s2[0]) >1 and s2[0] not in ["스타","그램",name[:-4],name[:-5],"이다","있다","없다","같다","아니다","그렇다","이렇다","많다","어떻다",
                                               "스럽다","저렇다"]:
                hts.append(s2)
    hts
    #형용사만 추출
    ad = []
    for a, b in hts:
        if b == "Adjective":
            ad.append((b,a))
    print(ad)
    print("==완료==")

    #형용사 나오는 순서보기
    adc = Counter(ad)
    adc2 = [[b,a] for a, b in adc.items()]
    adc2.sort()
    adc2.reverse()
    adc2

    #top20 형용사만 보기 (예시용)
    adc3 = adc2[:20]
    adc3

    #top형용사만 들어있는 데이터를 추출
    new_ad = []
    for x in ad:
        new_ad.append(x[1])
    new_ad

    #역별 Top15 형용사들의 Top명사들 도출.
    for top in range(15):
        new_phrase_list = []
        for item in dic_Twitter2:
            if adc2[top][1][1] in item:
                p = hangul.sub(' ', item)
                new_phrase_list.append(p)
        print(new_phrase_list)
        len(new_phrase_list)
        dic_Twitter = []
        for i in range(len(new_phrase_list)):
            print(i)
            s = Twitter().pos(new_phrase_list[i],norm=True, stem=True)
            dic_Twitter.append(s)
        print("==완료==")
        print (dic_Twitter)
        #총 형태소/data cleansing
        name = doc.name
        hts = []
        for a in range(len(dic_Twitter)):
            s1 = dic_Twitter[a]
            for b in range(len(s1)):
                s2 = s1[b]
                if len(s2[0]) >1 and s2[0] not in ["스타","그램",name[:-4],name[:-5],"이다","있다","없다","같다","아니다","그렇다","이렇다","많다","어떻다",
                                                   "스럽다","저렇다", "에서", "너무", "까지","오늘","일리","진짜","여기","역시","가능"]:
                    hts.append(s2)

        # Top명사도출
        noun = []
        for a, b in hts:
            if b == "Noun":
                noun.append((b,a))
        print(noun)
        print("==완료==")
        nounc = Counter(noun)
        nounc2 = [[b, a] for a, b in nounc.items()]
        nounc2
        nounc2.sort()
        nounc2.reverse()
        #top 20 명사 도출
        nounc3 = nounc2[:20]
        nounc3

        tag = pd.read_excel("pstag.xlsx")
        twitter_tag = list(tag['Twitter'])
        tw_tag=[x for x in twitter_tag if str(x) != 'nan' ]
        tw_tag=tw_tag[2:]
        tw_tag

        #품사-단어 사전만들기
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

        #Top형용사별 Top명사 Table을 엑셀파일로 저장 (파일이름은 Noun+역이름+형용사). **결과적으로 한 역당 15개의 명사파일 생성.
        x=pd.DataFrame({'Noun':hts2['Noun']})['Noun'].value_counts().reset_index()
        x.to_excel("Noun"+name[:-4]+adc2[top][1][1]+'.xlsx')

    stlist.append(x)
#역 자동화 끝. 한 역이 끝나면 자동으로 역목록에 있는 다음역으로 넘어가서 이 전체 process를 반복한다. 결과적으로 50개의 역 x 15개의 명사파일 = 총 750파일이 저장된다.

#**이렇게 저장된 750개의 파일을 각각 다른 역 폴더에 분류하고 싶으면 '폴더자동화' 코딩을 참조.