import requests
from pathlib import Path

# 기본 URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# 검색할 DB위치와 검색용어(term)설정
TOPIC = "cancer immunotherapy"
db_for_search = "?db=pubmed"
term_for_search = "&term=" + TOPIC
ret_num = 50    # 검색 할 PMID 갯수
retmax = "&retmax="+str(ret_num)    # PMID 수 제한
retmode = "&retmode=json"   # 이거 해야 json 으로 줌
rettype = "&rettype=count"  # 여기선 안씀

# url 조합
url_for_search = BASE_URL + db_for_search + term_for_search + retmax + retmode

# 응답받기
response = requests.get(url_for_search)

# 데이터화
data = response.json()

# # 잘 나오는지 확인
# print(data)

# 데이터 출력
data_esresult = data['esearchresult']
pmid_list = data_esresult['idlist']
count = len(pmid_list)
pmid_first = pmid_list[0]
pmid_last = pmid_list[-1]

print(f"저장된 PMID 수 : {count}")
print(f"첫 번째 PMID : {pmid_first}")
print(f"마지막 PMID : {pmid_last}")


# 파일 저장 주소 설정
path_folder = Path(__file__).parent
path_text = path_folder / "outputs/pmids_cancer_immunotherapy.txt"

# 파일 저장
with open(path_text, "w", encoding="utf-8") as file:
    for id in pmid_list:
        file.write(id+"\n")
    print("저장이 완료되었습니다.")