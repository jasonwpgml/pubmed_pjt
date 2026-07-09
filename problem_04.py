import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# 기본 URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# 검색할 DB위치와 검색용어(term)설정
TOPIC = "CRISPR	gene therapy"
DATES = [2021, 2022, 2023, 2024, 2025]
api_key = str(os.getenv("PUBMED_API_KEY"))
db_for_search = "pubmed"
retmode = "json"   # 이거 해야 json 으로 줌
rettype = "count"  # 갯수만 출력


# 변수설정
date_most = None
count_most = 0

# 연도별 검색
for date in DATES:
    # 검색어(연도 포함)
    term_for_search = f"{TOPIC} AND {date}[pdat]"

    # 파라미터로 검색 - requests 모듈 문법임!!!
    parameters = {
        "db": db_for_search,
        "api_key": api_key,
        "term": term_for_search,
        "retmode": retmode,
        "rettype": rettype,
    }

    # 응답받기
    response = requests.get(BASE_URL, parameters)

    # 데이터화
    data = response.json()
    esresult = data["esearchresult"]
    count = int(esresult["count"])

    # # 잘 나오는지 확인
    # print(f"{date}연도의 검색 결과 : {count}개")

    # 가장 많은 것 뽑기
    if count > count_most :
        count_most = count
        date_most = date

# 데이터 출력
print(f"검색 결과가 가장 많은 연도: {date_most}")
print(f"논문 수: {count_most}개")

