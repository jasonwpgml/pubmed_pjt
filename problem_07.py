from pathlib import Path
import csv

# 파일경로 및 변수 설정
path_csv = Path(__file__).parent / "outputs/abstracts_cancer_immunotherapy.csv"

KEY_WORDS = ("immunotherapy", "tumor", "survival", "response", "clinical trial")
keywords_dict = {
    "immunotherapy": 0,
    "tumor": 0, 
    "survival": 0, 
    "response": 0, 
    "clinical trial": 0, 
}

keyword_most = ""
count_has_mostkeyword = 0
# 파일 열기
with open(path_csv, "r", encoding="utf-8") as file :
    reader = csv.DictReader(file)

    # 딕셔너리 추출
    for dict in reader:
        artitle = dict["title"]
        abstext = dict["abstract"]

        # 키워드마다 돌면서 딕셔너리 안에 몇개씩 있는지 count 하기
        for word in KEY_WORDS:
            keywords_dict[word] += artitle.count(word) + abstext.count(word)

    # 최댓값인 key값 찾기
    for k, v in keywords_dict.items():
        if v == max(keywords_dict.values()):
            keyword_most = k

    # 해당 키워드가 포함된 논문의 수를 출력
    for dict in reader:
        artitle = dict["title"]
        abstext = dict["abstract"]

        if artitle.find(keyword_most) or abstext.find(keyword_most):
            count_has_mostkeyword += 1
    
print(f"가장 많이 등장한 키워드: {keyword_most}")
print(f"등장 논문 수: {count_has_mostkeyword}개")
