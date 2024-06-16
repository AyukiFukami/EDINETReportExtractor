import os
import json
from datetime import datetime
from edinet import Edinet

# ユーザーから日付を入力させる
date_str = input("Please enter the date in YYYY-MM-DD format: ")

# 日付を解析し、datetimeオブジェクトに変換する
try:
    date = datetime.strptime(date_str, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD format.")
    exit(1)

# APIキーを環境変数"API_KEY"から持ってくる
API_KEY = os.environ["API_KEY"]

edi = Edinet(API_KEY)

# ドキュメント一覧を取得
document_list = edi.get_document_list(date, type_=2)

# seccodeをキーとした辞書の作成
# key = SecCode, value = (docDescription, docID, filerName)
documents_class_by_secCode: dict[str, list[tuple[str, str, str]]] = {}

for document in document_list["results"]:
    # legalStatusが0の場合は閲覧期間満了
    if document["legalStatus"] != 0:
        # 辞書の要素に今まで出たことがないSecCodeだった場合、key, valueを作成
        if not documents_class_by_secCode.get(document["secCode"]):
            documents_class_by_secCode[document["secCode"]] = []
        documents_class_by_secCode[document["secCode"]].append((
            document["docDescription"],
            document["docID"],
            document["filerName"]
        ))

# 保存する
with open("documents.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(documents_class_by_secCode, indent=4, ensure_ascii=False))
