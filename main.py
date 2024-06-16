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

# 無効な文字を置き換える関数
def sanitize_filename(filename):
    import re
    return re.sub(r'[\/:*?"<>|]', '_', filename)

# ダウンロード先ディレクトリを設定
download_directory = "downloads"
os.makedirs(download_directory, exist_ok=True)

# PDFをダウンロードして保存する関数
def download_pdf(doc_id, file_name):
    try:
        content = edi.get_document(doc_id, type_=2)
        with open(file_name, "wb") as f:
            f.write(content)
        print(f"PDF downloaded and saved as {file_name}")
    except Exception as e:
        print(f"Failed to download PDF for document ID {doc_id}. Error: {e}")

# 銘柄コードから書類があるか確認する
while True:
    ticker = input("確認したい会社の銘柄コードを入力してください: ")
    SecCode = ticker + '0'
    if SecCode in documents_class_by_secCode:
        print("次の書類が確認できました。pdfをダウンロードします")
        for document in documents_class_by_secCode[SecCode]:
            print(document[0])
            doc_name = sanitize_filename(ticker + '_' + document[2] + '_' + document[0])
            file_name = os.path.join(download_directory, f"{doc_name}.pdf")
            download_pdf(document[1], file_name)
    else:
        print("指定された銘柄コードに対応する書類は見つかりませんでした。")
    
    another = input("他の銘柄コードを確認しますか？ y/n: ")
    if another.lower() != 'y':
        break
