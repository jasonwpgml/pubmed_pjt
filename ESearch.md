# ESearch

## 기본 URL

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```

---

## 기능

ESearch는 다음과 같은 기능을 제공한다.

* 텍스트 검색어와 일치하는 UID 목록을 제공한다.
* 검색 결과를 History Server에 저장한다.
* History Server에 저장된 데이터셋에서 모든 UID를 다운로드한다.
* History Server에 저장된 UID 데이터셋을 결합하거나 제한한다.
* UID 집합을 정렬한다.

API 사용자는 NCBI의 일부 제품에서 웹 인터페이스 검색을 통해 생성되는 기능이 ESearch에서는 제공되지 않을 수 있다는 점을 알아야 한다.

예를 들어 PubMed 웹 인터페이스인 `pubmed.ncbi.nlm.nih.gov`에는 인용문 매칭과 철자 교정 도구가 있지만, 이 기능들은 웹 인터페이스에서만 사용할 수 있다.

API에서 이와 비슷한 기능을 사용하려면 아래의 `ECitMatch`와 `ESpell`을 참고해야 한다.

---

# 필수 파라미터

## db

검색할 데이터베이스를 지정한다.

값은 유효한 Entrez 데이터베이스 이름이어야 한다.

기본값은 `pubmed`이다.

---

## term

Entrez 텍스트 검색어를 지정한다.

모든 특수문자는 URL 인코딩되어야 한다.

공백은 `+` 기호로 대체할 수 있다.

검색어가 매우 긴 경우, 즉 수백 자 이상인 경우에는 HTTP POST 호출을 사용하는 것을 고려해야 한다.

검색 필드 설명과 태그에 대한 정보는 PubMed 또는 Entrez 도움말을 참고하면 된다.

검색 필드와 태그는 데이터베이스마다 다르다.

예시:

```text
esearch.fcgi?db=pubmed&term=asthma
```

PubMed는 또한 “근접 검색”을 제공한다.

근접 검색은 여러 단어가 `[Title]` 또는 `[Title/Abstract]` 필드 안에서, 지정된 단어 수 이내에 어떤 순서로든 나타나는 경우를 검색하는 기능이다.

예시:

```text
esearch.fcgi?db=pubmed&term=”asthma treatment”[Title:~3]
```

이 예시는 제목 필드 안에서 `asthma`와 `treatment`가 서로 3단어 이내에 가까이 등장하는 논문을 찾는 검색이다.

---

# 선택 파라미터 – History Server

## usehistory

`usehistory`를 `y`로 설정하면, ESearch는 검색 결과로 나온 UID들을 History Server에 저장한다.

이렇게 저장된 UID들은 이후 다른 E-utility 호출에서 바로 사용할 수 있다.

또한 `term` 안에 포함된 `query_key` 값을 ESearch가 해석하게 하거나, `WebEnv`를 입력값으로 받게 하려면 `usehistory`를 반드시 `y`로 설정해야 한다.

---

## WebEnv

이전 ESearch, EPost, ELink 호출에서 반환된 웹 환경 문자열이다.

`WebEnv`가 제공되면 ESearch는 검색 결과를 기존 WebEnv에 저장한다.

즉, 기존 환경에 새 검색 결과를 추가하는 방식이다.

또한 `WebEnv`를 제공하면 `term`에서 query key를 사용할 수 있으므로, 이전 검색 집합들을 결합하거나 제한할 수 있다.

위에서 설명한 것처럼, `WebEnv`를 사용하려면 `usehistory`를 반드시 `y`로 설정해야 한다.

예시:

```text
esearch.fcgi?db=pubmed&term=asthma&WebEnv=<webenv string>&usehistory=y
```

---

## query_key

이전 ESearch, EPost, ELink 호출에서 반환된 정수형 query key이다.

`query_key`가 제공되면, ESearch는 `query_key`가 가리키는 기존 검색 결과 집합과 `term`으로 검색한 새 검색 결과 집합의 교집합을 찾는다.

즉, 두 검색 결과를 `AND`로 결합하는 것이다.

`query_key`가 작동하려면 기존 `WebEnv` 문자열이 함께 지정되어야 하며, `usehistory`도 `y`로 설정되어야 한다.

query key 값은 `term` 안에서도 제공할 수 있다.

이때 query key 앞에는 `#`을 붙여야 한다.

URL에서는 `#`이 `%23`으로 인코딩된다.

ESearch에는 `query_key` 파라미터를 하나만 제공할 수 있지만, `term` 안에서는 여러 개의 query key를 조합할 수 있다.

또한 `term` 안에 query key를 넣으면 `AND`뿐 아니라 `OR`, `NOT`으로도 결합할 수 있다.

다음 두 URL은 기능적으로 동일하다.

```text
esearch.fcgi?db=pubmed&term=asthma&query_key=1&WebEnv=<webenv string>&usehistory=y
```

```text
esearch.fcgi?db=pubmed&term=%231+AND+asthma&WebEnv=<webenv string>&usehistory=y
```

---

# 선택 파라미터 – 검색 결과 가져오기

## retstart

검색 결과 집합에서 XML 출력에 표시할 첫 번째 UID의 순번을 지정한다.

기본값은 `0`이며, 이는 전체 결과 집합의 첫 번째 레코드를 의미한다.

이 파라미터는 `retmax`와 함께 사용하여 검색 결과 중 원하는 일부 UID만 다운로드할 때 사용할 수 있다.

---

## retmax

검색 결과 집합에서 XML 출력에 표시할 UID의 총 개수를 지정한다.

기본값은 `20`이다.

즉, 기본적으로 ESearch는 검색된 UID 중 처음 20개만 XML 출력에 포함한다.

만약 `usehistory`가 `y`로 설정되어 있다면, 나머지 UID들은 History Server에 저장된다.

그렇지 않으면 나머지 UID들은 출력되지 않고 사라진다.

`retmax` 값을 늘리면 XML 출력에 더 많은 UID를 포함할 수 있다.

단, 최대 10,000개까지 가능하다.

PubMed나 PMC가 아닌 데이터베이스에서 10,000개 이상의 UID를 가져오려면, `retstart` 값을 증가시키면서 여러 번 ESearch 요청을 보내야 한다.

하지만 PubMed와 PMC의 경우, ESearch는 검색어와 일치하는 결과 중 처음 10,000개까지만 가져올 수 있다.

10,000개 이상의 PubMed 레코드를 얻으려면 EDirect를 사용하는 것을 고려해야 한다.

EDirect에는 PubMed 검색 결과를 자동으로 배치 처리하여 임의의 개수만큼 가져올 수 있는 추가 로직이 포함되어 있다.

또 다른 방법은 검색어에 날짜 제한 같은 조건을 추가하여 원하는 결과 집합을 10,000개 이하의 여러 묶음으로 나누는 것이다.

---

## rettype

검색 결과 반환 타입을 지정한다.

ESearch에서 허용되는 값은 두 가지이다.

* `uilist`: 기본값이며, 표준 XML 출력을 표시한다.
* `count`: `<Count>` 태그만 표시한다.

즉, `count`를 사용하면 실제 PMID 목록이 아니라 검색 결과 개수만 받을 수 있다.

---

## retmode

반환되는 출력 형식을 결정한다.

ESearch의 기본값은 XML 출력인 `xml`이다.

하지만 `json`도 지원하므로, JSON 형식으로 결과를 받을 수 있다.

---

## sort

ESearch 출력에서 UID를 정렬하는 방법을 지정한다.

사용 가능한 값은 데이터베이스, 즉 `db`에 따라 다르다.

각 Entrez 검색 결과 페이지의 Display Settings 메뉴에서 확인할 수 있다.

`usehistory`가 `y`로 설정되어 있으면, UID들은 지정된 정렬 순서대로 History Server에 저장된다.

그리고 이후 ESummary나 EFetch에서 같은 순서로 가져올 수 있다.

예를 들어 Gene 데이터베이스에서는 `relevance`, `name` 같은 값이 있다.

사용자는 데이터베이스마다 기본 정렬값이 다르다는 점을 알아야 한다.

또한 특정 데이터베이스에서 ESearch가 사용하는 기본 정렬값이 NCBI 웹 검색 페이지에서 사용하는 기본 정렬값과 다를 수 있다.

PubMed에서 사용할 수 있는 `sort` 값은 다음과 같다.

* `pub_date`: 출판일 기준 내림차순 정렬
* `Author`: 첫 번째 저자 기준 오름차순 정렬
* `JournalName`: 저널 이름 기준 오름차순 정렬
* `relevance`: 기본 정렬 순서이며, PubMed 웹에서의 “Best Match”에 해당한다.

---

## field

검색 필드를 지정한다.

이 파라미터를 사용하면 전체 검색어가 지정된 Entrez 필드로 제한된다.

다음 두 URL은 동일하다.

```text
esearch.fcgi?db=pubmed&term=asthma&field=title
```

```text
esearch.fcgi?db=pubmed&term=asthma[title]
```

즉, `field=title`을 쓰는 것과 검색어에 `[title]` 태그를 붙이는 것은 같은 의미다.

---

## idtype

반환할 식별자의 종류를 지정한다.

이 파라미터는 주로 서열 데이터베이스인 `nuccore`, `popset`, `protein`에서 사용된다.

기본적으로 ESearch는 GI 번호를 반환한다.

만약 `idtype`을 `acc`로 설정하면, GI 번호 대신 `accession.version` 식별자를 반환한다.

PubMed만 사용할 때는 보통 신경 쓰지 않아도 되는 파라미터다.

---

# 선택 파라미터 – 날짜

## datetype

검색을 제한할 때 사용할 날짜 유형을 지정한다.

허용되는 값은 Entrez 데이터베이스마다 다르지만, 일반적으로 다음 값들이 사용된다.

* `mdat`: 수정일
* `pdat`: 출판일
* `edat`: Entrez 등록일

일반적으로 하나의 Entrez 데이터베이스에는 허용되는 `datetype` 값이 두 개 정도 있다.

---

## reldate

`reldate`에 정수 `n`을 설정하면, 지정한 `datetype` 기준으로 최근 `n`일 이내의 항목만 검색한다.

예를 들어 `reldate=60`이면 최근 60일 이내의 결과만 가져온다.

---

## mindate, maxdate

`datetype`으로 지정한 날짜 기준으로 검색 결과를 날짜 범위에 따라 제한한다.

임의의 날짜 범위를 지정하려면 `mindate`와 `maxdate`를 함께 사용해야 한다.

일반적인 날짜 형식은 다음과 같다.

```text
YYYY/MM/DD
```

다음 형식도 허용된다.

```text
YYYY
YYYY/MM
```

---

# 예시

## 예시 1

PubMed에서 `cancer`라는 검색어로 검색한다.

Entrez 등록일 기준 최근 60일 이내의 초록을 대상으로 한다.

처음 100개의 PMID와 검색어 변환 정보를 가져온다.

검색 결과를 History Server에 저장하고, `WebEnv`와 `query_key`를 반환한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&reldate=60&datetype=edat&retmax=100&usehistory=y
```

---

## 예시 2

PubMed에서 저널 PNAS, Volume 97에 해당하는 논문을 검색한다.

검색 결과 목록에서 7번째 PMID부터 시작하여 6개의 PMID를 가져온다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=PNAS[ta]+AND+97[vi]&retstart=6&retmax=6&tool=biomed3
```

여기서:

* `PNAS[ta]`: 저널 약어가 PNAS인 논문
* `97[vi]`: Volume이 97인 논문
* `retstart=6`: 0부터 세기 때문에 7번째 결과부터 시작
* `retmax=6`: 6개 결과 반환

---

## 예시 3

NLM Catalog에서 `obstetrics`라는 검색어와 일치하는 저널을 검색한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nlmcatalog&term=obstetrics+AND+ncbijournals[filter]
```

---

## 예시 4

PubMed Central에서 `stem cells`라는 검색어를 포함하고, 무료 전문이 제공되는 논문을 검색한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=stem+cells+AND+free+fulltext[filter]
```

---

## 예시 5

Nucleotide 데이터베이스에서 모든 tRNA를 검색한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term=biomol+trna[prop]
```

---

## 예시 6

Protein 데이터베이스에서 분자량 범위가 70,000에서 90,000 사이인 단백질을 검색한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=70000:90000[molecular+weight]
```

# Advanced Search

## 고급 검색에서 할 수 있는 것

Advanced Search 페이지에 포함된 도구들은 사용자가 다음과 같은 작업을 할 수 있도록 도와준다.

* 특정 필드에서 용어 검색하기
* 검색어를 조합하여 크고 복잡한 검색식 만들기
* PubMed가 각 검색어를 어떻게 해석했는지 확인하기
* 서로 다른 검색어의 검색 결과 수 비교하기

---

## 주요 기능

Advanced Search에는 다음과 같은 기능이 포함되어 있다.

* 특정 필드에서 검색하기
* 용어 색인 둘러보기
* 검색 기록 확인하기
* 검색 결과 수 미리보기
* History를 사용하여 검색 조합하기
* Search Details 확인하기

---

# 특정 필드에서 검색하기

Advanced Search Builder를 사용하면 저자나 저널 같은 특정 필드에서 용어를 검색할 수 있다.

일부 필드에서는 입력하는 동안 자동완성 기능이 제안을 제공한다.

## 사용 방법

1. `"All Fields"` 드롭다운 메뉴에서 검색하려는 필드를 선택한다.

2. Builder에서 용어를 추가하여 query box에 검색식을 만든다.

3. 기본 Boolean 연산자는 `AND`이다.
   필요한 경우 드롭다운 메뉴에서 `OR` 또는 `NOT`을 선택할 수 있다.

4. query box에 용어 추가를 마쳤다면 `Search`를 클릭하여 검색을 실행한다.
   또는 `Add to History`를 클릭하여 검색 기록에 추가할 수 있다.

특정 필드를 검색하면서 Automatic Term Mapping을 우회하고 싶다면, 검색어에 검색 필드 태그를 직접 붙이면 된다.

예를 들면 다음과 같은 방식이다.

```text
cancer[Title]
Smith J[Author]
Nature[Journal]
```

---

# 용어 색인 둘러보기

Advanced Search Builder에는 `Show Index` 기능이 포함되어 있다.

이 기능은 선택한 PubMed 검색 필드에 등장하는 용어들을 알파벳 순서로 보여준다.

전체 필드에서 둘러볼 수도 있고, `MeSH Terms` 같은 특정 필드 안에서만 둘러볼 수도 있다.

---

## 사용 방법

1. `Advanced`를 클릭하여 Advanced Search 페이지로 이동한다.

2. Builder에서 `All Fields` 메뉴를 사용하여 검색 필드를 선택한다.

   참고: `Show Index`는 모든 검색 필드에서 사용할 수 있는 것은 아니다.
   이 기능과 호환되는 필드에서만 `Show Index` 링크가 표시된다.

3. 검색창에 용어를 입력한 뒤 `Show Index`를 클릭한다.

4. 색인은 검색어 목록을 알파벳 순서로 보여준다.

5. 각 검색어 옆에는 대략적인 인용 문헌 수가 표시된다.
   실제 인용 문헌 수는 검색을 실행했을 때 반환된다.

6. 검색에 포함하고 싶은 용어를 찾을 때까지 스크롤한다.

7. 원하는 용어를 선택하면 해당 용어가 검색창에 추가된다.

8. 목록에서 여러 용어를 선택하여 검색창에 추가할 수도 있다.

9. Builder에서 용어를 query box에 추가하여 검색식을 구성한다.

10. 검색식 구성을 마쳤다면 `Search`를 클릭하여 검색을 실행한다.
    또는 `Add to History`를 클릭하여 검색 기록에 추가할 수 있다.

---

# 색인 사용 시 참고 사항

PubMed는 모든 Boolean 연산자를 왼쪽에서 오른쪽 순서로 처리한다.

Builder는 색인에서 여러 용어를 선택하면 자동으로 `OR`로 연결하고, 괄호도 추가한다.

슬래시는 공백 뒤에 표시된다.

예를 들어 MeSH Term과 Subheading인 `zika virus/analysis`는 `zika virus infection/virology` 뒤에 표시된다.

MeSH 용어 뒤에 슬래시를 입력하면, 색인에서 해당 MeSH/Subheading 조합의 개수 표시로 바로 이동할 수 있다.

`Show Index`는 날짜 필드에서는 사용할 수 없다.
