# EFetch

## 기본 URL

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

---

# 기능

EFetch는 다음과 같은 기능을 제공한다.

* 입력된 UID 목록에 해당하는 데이터 레코드를 지정된 형식으로 반환한다.
* Entrez History Server에 저장된 UID 집합에 해당하는 데이터 레코드를 지정된 형식으로 반환한다.

쉽게 말하면, **PMID 같은 ID를 넣으면 해당 논문의 초록, XML, MEDLINE 형식 데이터 등을 가져오는 기능**이다.

---

# 필수 파라미터

## db

레코드를 가져올 데이터베이스를 지정한다.

값은 유효한 Entrez 데이터베이스 이름이어야 한다.

기본값은 `pubmed`이다.

현재 EFetch는 모든 Entrez 데이터베이스를 지원하지는 않는다.

사용 가능한 데이터베이스 목록은 Chapter 2의 Table 1을 참고해야 한다.

---

# 필수 파라미터 — UID 목록을 입력으로 사용할 때

## id

UID 목록을 지정한다.

하나의 UID를 제공할 수도 있고, 쉼표로 구분된 UID 목록을 제공할 수도 있다.

모든 UID는 `db`에서 지정한 데이터베이스에 속한 것이어야 한다.

EFetch에 전달할 수 있는 UID 개수에 정해진 최대값은 없다.

하지만 약 200개 이상의 UID를 전달해야 한다면 HTTP POST 방식을 사용하는 것이 좋다.

서열 데이터베이스인 `nuccore`, `popset`, `protein`에서는 UID 목록에 GI 번호와 `accession.version` 식별자가 섞여 있을 수 있다.

예시:

```text
efetch.fcgi?db=pubmed&id=19393038,30242208,29453458
```

```text
efetch.fcgi?db=protein&id=15718680,NP_001098858.1,119703751
```

---

## 서열 데이터베이스에 대한 특별 참고 사항

NCBI는 점점 더 많은 새로운 서열 레코드에 대해 더 이상 GI 번호를 부여하지 않는다.

따라서 이러한 레코드들은 Entrez에 색인되지 않으며, ESearch나 ESummary로 가져올 수 없다.

또한 ELink를 통해 접근 가능한 Entrez 링크도 없다.

하지만 EFetch는 `id` 파라미터에 `accession.version` 식별자를 넣으면 이러한 레코드를 가져올 수 있다.

---

# 필수 파라미터 — Entrez History Server를 입력으로 사용할 때

## query_key

`query_key`는 정수값이다.

이 값은 주어진 Web Environment에 연결된 UID 목록 중 어떤 것을 EFetch의 입력으로 사용할지 지정한다.

`query_key`는 이전 ESearch, EPost, ELink 호출의 출력에서 얻을 수 있다.

`query_key` 파라미터는 반드시 `WebEnv`와 함께 사용해야 한다.

---

## WebEnv

`WebEnv`는 Web Environment를 의미한다.

이 파라미터는 EFetch의 입력으로 제공할 UID 목록이 들어 있는 Web Environment를 지정한다.

일반적으로 `WebEnv` 값은 이전 ESearch, EPost, ELink 호출의 출력에서 얻는다.

`WebEnv` 파라미터는 반드시 `query_key`와 함께 사용해야 한다.

예시:

```text
efetch.fcgi?db=protein&query_key=<key>&WebEnv=<webenv string>
```

---

# 선택 파라미터 — 데이터 가져오기

## retmode

`retmode`는 반환될 레코드의 데이터 형식을 지정한다.

예를 들어 일반 텍스트, HTML, XML 같은 형식을 지정할 수 있다.

각 데이터베이스에서 허용되는 값의 전체 목록은 Table 1을 참고해야 한다.

---

## rettype

`rettype`은 반환될 레코드의 보기 형식을 지정한다.

예를 들어 PubMed에서는 `Abstract`나 `MEDLINE` 형식을 지정할 수 있다.

Protein 데이터베이스에서는 `GenPept`나 `FASTA` 형식을 지정할 수 있다.

각 데이터베이스에서 허용되는 값의 전체 목록은 Table 1을 참고해야 한다.

---

## retstart

가져올 첫 번째 레코드의 순차적 인덱스를 지정한다.

기본값은 `0`이며, 이는 전체 입력 집합의 첫 번째 레코드를 의미한다.

이 파라미터는 `retmax`와 함께 사용하여 입력 집합에서 원하는 일부 레코드만 다운로드할 때 사용할 수 있다.

---

## retmax

입력 집합에서 가져올 레코드의 총 개수를 지정한다.

최대값은 10,000개이다.

큰 데이터 집합을 가져올 경우 `retmax` 값을 고정해두고 `retstart` 값을 반복적으로 증가시키면 전체 데이터를 일정한 크기의 배치로 나누어 다운로드할 수 있다.

---

# 선택 파라미터 — 서열 데이터베이스

## strand

가져올 DNA 가닥을 지정한다.

사용 가능한 값은 다음과 같다.

* `1`: plus strand
* `2`: minus strand

---

## seq_start

가져올 첫 번째 서열 염기를 지정한다.

값은 원하는 첫 번째 염기의 정수 좌표여야 한다.

`1`은 서열의 첫 번째 염기를 의미한다.

---

## seq_stop

가져올 마지막 서열 염기를 지정한다.

값은 원하는 마지막 염기의 정수 좌표여야 한다.

`1`은 서열의 첫 번째 염기를 의미한다.

---

## complexity

반환할 데이터 내용의 범위를 지정한다.

많은 서열 레코드는 더 큰 데이터 구조, 즉 “blob”의 일부로 저장되어 있다.

`complexity` 파라미터는 그 blob 중 어느 정도를 반환할지 결정한다.

예를 들어 mRNA는 해당 단백질 산물과 함께 저장될 수 있다.

사용 가능한 값은 다음과 같다.

| complexity 값 | 각 요청 GI에 대해 반환되는 데이터 |
| -----------: | -------------------- |
|          `0` | entire blob          |
|          `1` | bioseq               |
|          `2` | minimal bioseq-set   |
|          `3` | minimal nuc-prot     |
|          `4` | minimal pub-set      |

---

# 예시

## PubMed

### PMID 17284678과 9997을 텍스트 초록 형식으로 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=17284678,9997&retmode=text&rettype=abstract
```

---

### PMID를 XML 형식으로 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11748933,11700088&retmode=xml
```

---

## PubMed Central

### PubMed Central ID 212403의 XML 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=212403
```

---

## Nucleotide / Nuccore

### GI 21614549의 plus strand에서 처음 100개 염기를 FASTA 형식으로 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=21614549&strand=1&seq_start=1&seq_stop=100&rettype=fasta&retmode=text
```

---

### GI 21614549의 minus strand에서 처음 100개 염기를 FASTA 형식으로 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=21614549&strand=2&seq_start=1&seq_stop=100&rettype=fasta&retmode=text
```

---

### GI 21614549의 nuc-prot 객체 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=21614549&complexity=3
```

---

### GI 5의 전체 ASN.1 레코드 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=5
```

---

### GI 5의 FASTA 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=5&rettype=fasta
```

---

### GI 5의 GenBank flat file 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=5&rettype=gb
```

---

### GI 5의 GBSeqXML 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=5&rettype=gb&retmode=xml
```

---

### GI 5의 TinySeqXML 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=5&rettype=fasta&retmode=xml
```

---

## Popset

### Popset ID 12829836의 GenPept flat file 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=popset&id=12829836&rettype=gp
```

---

## Protein

### GI 8의 GenPept flat file 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=8&rettype=gp
```

---

### GI 8의 GBSeqXML 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=8&rettype=gp&retmode=xml
```

---

## Sequences

### transcript와 단백질 산물의 FASTA 가져오기

대상 GI는 `312836839`와 `34577063`이다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sequences&id=312836839,34577063&rettype=fasta&retmode=text
```

---

## Gene

### Gene ID 2의 전체 XML 레코드 가져오기

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=2&retmode=xml
```

---

# PubMed 기준 핵심 정리

PubMed에서 EFetch를 쓸 때 가장 자주 쓰는 형태는 다음과 같다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID&retmode=text&rettype=abstract
```

예를 들어 PMID가 `17284678`이면:

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=17284678&retmode=text&rettype=abstract
```

여러 PMID를 한 번에 가져올 때는 쉼표로 연결한다.

```text
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=17284678,9997&retmode=text&rettype=abstract
```

즉 PubMed 기준으로는 다음처럼 이해하면 된다.

```text
ESearch = 검색어로 PMID 찾기
ESummary = PMID로 제목, 저널, 날짜 같은 요약 정보 가져오기
EFetch = PMID로 초록, XML, MEDLINE 같은 실제 레코드 가져오기
```

