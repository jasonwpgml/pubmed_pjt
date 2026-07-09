import csv
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup as bs

load_dotenv()

## text 파일 읽기
# 파일 경로 설정
base_path = Path(__file__).parent
text_path = base_path / "outputs/pmids_cancer_immunotherapy.txt"
csv_path = base_path / "outputs/abstracts_cancer_immunotherapy.csv"

text_list = []
with open(text_path, "r", encoding="utf-8") as text_file:
    for id in text_file:
        text_list.append(text_file.readline().strip())

# print(text_list)

## 검색하기
# 기본 URL 
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# 기본 변수 설정
api_key = str(os.getenv("PUBMED_API_KEY"))


# 파라미터 설정
parameters = {
    "db": "pubmed",
    "api_key": api_key,
    "id": text_list,
    "retmode": "xml",
    "rettype": "abstract",
}

response = requests.get(BASE_URL, parameters)
soup = bs(response.text, "lxml-xml")

result_list = []

articles = soup.find_all("PubmedArticle")

for article in articles:
    # PMID 추출
    pmid_tag = article.find("PMID")
    pmid = pmid_tag.get_text(strip=True)

    # Article Title 태그에서 텍스트 추출
    title_tag = article.find("ArticleTitle")
    title = title_tag.get_text(" ", strip=True)

    # Abstract Text 텍스트 추출
    abstract_tags = article.find_all("AbstractText")

    abstract_parts = []

    for tag in abstract_tags:
        label = tag.get("Label")
        text = tag.get_text(" ", strip=True)

        if label:
            abstract_parts.append(f"{label}: {text}")
        else:
            abstract_parts.append(text)

    abstract = " ".join(abstract_parts)

    result_list.append({
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
    })


with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["pmid", "title", "abstract"])
    writer.writeheader()
    writer.writerows(result_list)
    print("저장 완료!")