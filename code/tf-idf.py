import pandas as pd
import matplotlib.pyplot as plt
from konlpy.tag import Twitter
import os
from gensim import corpora, models, similarities
import numpy as np

station = pd.read_excel("2호선 역 목록.xlsx")
# 역 이름에 # 붙여서 리스트로 저장
station = list(station['총'])
stations = [x for x in station if str(x) != 'nan']
stations

dic_station = []
station_emo = []

# 포스팅 분리
for station in stations:
    try:
        doc = open('crawl/'+station + '.csv', 'r')
        data = doc.read()
        doc.close()
        phrase = data.split('\n')
    except:
        doc = open('crawl/'+station  + '.csv', 'r', encoding='utf8')
        data = doc.read()
        doc.close()
        phrase = data.split('\n')
        continue

    # 포스팅에서 한글 외 문자 제거
    import re

    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    # 형태소 문장 단위 추출
    dic_Twitter = []
    for i in range(len(phrase)):
        p = hangul.sub(' ', phrase[i])
        s = Twitter().pos(p, stem=True, norm=True)
        dic_Twitter.append(s)

    # 총 형태소
    name = doc.name
    hts = []
    for a in range(len(dic_Twitter)):
        s1 = dic_Twitter[a]
        for b in range(len(s1)):
            s2 = s1[b]
            if len(s2[0]) >1 and s2[0] not in ["스타","그램",name[:-4],name[:-5],"이다","있다","없다","같다","아니다","그렇다","이렇다","많다","어떻다",
                                               "스럽다","저렇다", '인스타그램', '맞팔', '선팔', '이벤트', '응모']:
                hts.append(s2)

    # 형용사만 뽑기
    texts = []
    for z, x in hts:
        if x == 'Adjective':
            texts.append(z)

    # 형용사별 빈도수 5개 이상만 추가
    from collections import Counter
    k = Counter(texts)
    t = []
    for x, y in k.items():
        if y >= 5:
            for i in range(y):
                t.append(x)
    dic_station.append(corpora.Dictionary([t]))
    print(station+str(len(t)))
    # 역별 감정 추가
    station_emo.append(t)

print("1차 준비 완료")


# TF-IDF
count = 0
result = pd.DataFrame(np.zeros(400))
col_list = [0]
for station in stations:
    corpus = [dic_station[count].doc2bow(emo) for emo in station_emo]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # TF-IDF 가중치 정렬
    # 역 사전별 단어 뽑기
    character = {}
    for x in dic_station[count]:
        character[x] = dic_station[count][x]
    b = []
    for doc in corpus_tfidf:
        b.append([(x[1], x[0]) for x in doc])
    b = b[count]
    b.sort(reverse=True)

    weight = {}
    for x in b:
        if character[1] not in weight:
            weight[character[x[1]]] = []
            weight[character[x[1]]].append(x[0])

    kk = pd.DataFrame(weight).T
    kk = kk.sort_values(0, ascending=False).reset_index()
    kk.columns = [station, "weight"]
    col_list.extend(list(kk.columns))
    result = pd.concat([result, kk], axis=1)
    count += 1
result.drop(0, axis=1, inplace=True)
result.to_excel('역별 tf-idf.xlsx')
print("완료")
