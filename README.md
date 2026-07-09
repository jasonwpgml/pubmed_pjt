# pubmed_pjt

pubmed api 에서 ESearch를 활용하여 논문 검색하는 프로젝트 입니다.

ESearch 활용법 등 필요한 사항들은 ChatGpt로 번역해서 ESearch.md 에 저장해놓았습니다.



# 문제 풀이 정리


## problem_01.py

ESearch 기본 URL에 `db`, `api_key`, `term`, `retmode`, `rettype` 등 필요한 값들을 붙여서 요청 URL을 만들고, `requests.get()`으로 응답을 받았습니다. 

응답은 json 형태로 바꾸면 나오는 딕셔너리에서 키 `esearchresult` 로 밸류를 가져왔습니다.

그 밸류도 딕셔너리라 필요한 키 `count`와 `pmid`를 사용해 전체 검색 결과 수와 PMID 목록을 가져왔습니다.



## problem_02.py

필요한 토픽을 리스트로 만들어서 각각 PubMed 검색 결과 수를 비교했습니다.

반복문으로 토픽을 하나씩 꺼내고, `rettype=count`를 사용해서 각 주제어의 논문 수만 가져오도록 했습니다. 가져온 count 값은 숫자로 바꾼 뒤 `topic_counts` 리스트에 저장했습니다.

반복문 안에서 가장 큰 값과 가장 작은 값을 계속 비교해서 검색 결과가 가장 많은 주제어와 가장 적은 주제어를 찾았습니다. 

마지막에는 전체 주제어별 검색 결과 수를 `outputs/topic_counts.csv` 파일로 저장했습니다.



## problem_03.py

`cancer immunotherapy` 검색어로 PubMed에서 PMID 50개를 가져왔습니다.

`retmax=50` 값을 넣어서 가져올 PMID 개수를 제한했고, json 응답에서 `idlist`를 꺼내 PMID 목록을 만들었습니다. 저장된 PMID 수, 첫 번째 PMID, 마지막 PMID를 출력해서 제대로 가져왔는지 확인했습니다.

PMID 목록은 한 줄에 하나씩 들어가도록 `outputs/pmids_cancer_immunotherapy.txt` 파일에 저장했습니다.



## problem_04.py

`CRISPR gene therapy` 검색어를 2021년부터 2025년까지 연도별로 검색해서 논문 수가 가장 많은 연도를 찾았습니다.

연도 리스트를 만들고, 반복문에서 검색어에 `AND {연도}[pdat]` 조건을 붙였습니다. 이 문제에서는 URL을 직접 문자열로 붙이지 않고, `parameters` 딕셔너리를 만들어서 `requests.get(BASE_URL, parameters)` 형태로 요청했습니다.

각 연도의 검색 결과 수를 가져와서 기존 최댓값과 비교했고, 가장 큰 count를 가진 연도와 논문 수를 마지막에 출력했습니다.



## problem_05.py

`data/summary_cancer_immunotherapy.csv` 파일을 읽어서 가장 많이 등장한 저널명을 찾았습니다.

`csv.DictReader`로 csv 파일을 읽고, 각 행에서 `source` 값을 가져왔습니다. `source_dict` 딕셔너리에 저널명이 이미 있으면 개수를 1 증가시키고, 처음 나오는 저널이면 1로 새로 넣었습니다.

마지막에는 딕셔너리의 key, value를 반복하면서 count가 가장 큰 저널명을 찾고, 가장 많이 등장한 저널명과 논문 수를 출력했습니다.



## problem_06.py

`beautifulsoup4` 와 `lxml` 을 사용하여 초록(Abstract) 텍스트를 파싱하였습니다.

일단 `PubmedArticle` 태그를 전부 불러와서 `PMID`, `ArticleTitle`, `AbstractText`를 추출하였습니다.
`AbstractText` 의 경우에는 없는 경우와, label이 붙어있는 경우를 구분하여 나눠서 텍스트들을 추출한 후 나중에 되합치는 방법으로 만들었습니다.