import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# 기본 URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# 검색할 DB위치와 검색용어(term)설정
TOPIC = "CRISPR	gene therapy"
api_key = "api_key=" + str(os.getenv("PUBMED_API_KEY"))
db_for_search = "?db=pubmed"
term_for_search = "&term=" + TOPIC
ret_num = 50    # 검색 할 PMID 갯수
retmax = "&retmax="+str(ret_num)    # PMID 수 제한
retmode = "&retmode=json"   # 이거 해야 json 으로 줌
rettype = "&rettype=count"  # 여기선 안씀

# url 조합
url_for_search = BASE_URL + db_for_search + api_key + term_for_search + retmax + retmode

# 응답받기
response = requests.get(url_for_search)

# 데이터화
data = response.json()

# # 잘 나오는지 확인
# print(data)

# 데이터 출력