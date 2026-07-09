import requests
import json
from pathlib import Path

# 기본 URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# DB 와 검색용어(term)설정
db_for_search = "pubmed"
term_for_search = "artificial+intelligence+cancer"
retmode = "&retmode=json"
rettype = "&rettype=count" # 안씀

# url 조합
url_for_search = BASE_URL + "?db=" + db_for_search + "&term=" + term_for_search + retmode

# 응답받기
response = requests.get(url_for_search)

# 
data = response.json()

# # 잘 나오는지 확인
# print(data)

# 데이터 출력
data_esresult = data['esearchresult']
count = data_esresult['count']
pmid_list = data_esresult['idlist'][:5]

print(f"전체 검색 결과 수 : {count}")
print(f"가져온 PMID 5개 : {pmid_list}")

# 파일 기본 주소 설정

path_folder = Path(__file__).parent
path_json = path_folder / "outputs/raw_esearch_ai_cancer.json"

with open(path_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    print("outputs 폴더에 저장 완료되었습니다")