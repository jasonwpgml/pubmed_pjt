import csv
from pathlib import Path

# 파일 경로 설정 및 변수 설정
base_path = Path(__file__).parent
data_path = base_path / "data/summary_cancer_immunotherapy.csv"
source_dict = {}

# 파일 읽기
with open(data_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    # pmid만 담아서 리스트 만들기
    for dict in reader:
        source = dict["source"]
        if source in source_dict.keys():
            source_dict[source] +=1
        else:
            source_dict[source] = 1

# # 잘 읽혔는지 확인
# print(source_dict)

# 키 값 가장 많은 저널 찾기
count_most = 0
source_most = ""
for s, c in source_dict.items():
    if c > count_most:
        count_most=c
        source_most=s

# 출력부
print(f"가장 많이 등장한 저널명: {source_most}")
print(f"논문 수: {count_most}개")
