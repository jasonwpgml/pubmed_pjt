import requests
import csv
from pathlib import Path

# 기본 URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# 검색할 DB 위치와 검색용어(term)설정
Topics = [
    "machine learning diabetes",
    "deep learning radiology",
    "Alzheimer biomarker",
    "COVID-19 vaccine",
    "cancer immunotherapy"
    ]

db_for_search = "?db=pubmed"
retmode = "&retmode=json"
rettype = "&rettype=count" # 안씀


# 저장할 빈 리스트 및 변수 작성
topic_counts = []
topic_most = ""
topic_least = ""
count_most = 0
count_least = 99999999999999

# 본격적인 저장 및 비교
for topic in Topics:
    # url 조합
    term_for_search = "&term=" + topic
    url_for_search = BASE_URL + db_for_search + term_for_search + retmode

    # 응답받기
    response = requests.get(url_for_search)

    # 데이터화
    data = response.json()
    data_esresult = data['esearchresult']
    count = int(data_esresult['count'])
    print(f"주제어 {topic} 의 검색 결과 수 : {count}")

    # 리스트에 담기
    topic_counts.append({ 
        "topic" : topic , 
        "count" : count 
        })
    
    # 크기 비교
    if count > count_most:
        count_most = count
        topic_most = topic

    if count < count_least:
        count_least = count
        topic_least = topic


# # 담긴 정보 확인
# print(count_most)
# print(topic_most)
# print(count_least)
# print(topic_least)
# print(topic_counts)

# 출력부
print(f"검색 결과가 가장 많은 주제어: {topic_most} , {count_most}개")
print(f"검색 결과가 가장 많은 주제어: {topic_least} , {count_least}개")

## csv 파일로 저장
# 경로 설정
folder_path = Path(__file__).parent
csv_path = folder_path / "outputs/topic_counts.csv"
# 저장
with open(csv_path, "w", encoding="utf-8",newline="") as file:
    keys = ["topic","count"]
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(topic_counts)
    print("저장이 완료되었습니다.")
