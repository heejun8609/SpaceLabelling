import os, sys
import pandas as pd
import shutil

#'역별기본빈도'이라는 이름의 폴더생성
os.mkdir('역별기본빈도')

#역목록불러오기
station_list = pd.read_excel('2호선 역 목록.xlsx')
autostation = []
for station in station_list['2호선 역 목록'][0:50]:
    autostation.append(station)
print(autostation)

#'역별기본빈도'폴더 안에 각 역 이름을 딴 폴더들을 생성
for file_name in autostation:
    s = '역별기본빈도/'
    if not os.path.exists(s + file_name):
        os.mkdir(s + file_name)

#'Noun'역이름''으로 시작하는 파일들을 합당하는 역이름폴더에 넣는다
    source = r'C:\Users\2-10\PycharmProjects\project'
    c= r'C:\Users\2-10\PycharmProjects\project\역별기본빈도\\'+file_name

    files = os.listdir(source)
    for f in files:
        if (f.startswith("Noun"+file_name)):
            shutil.move(f, c)

