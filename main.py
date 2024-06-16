import os
import json
from datetime import datetime
from edinet import Edinet


def get_and_save_document_list(edi, date):
    """指定した日付のドキュメントリストを取得し、JSONファイルに保存する。"""
    document_list = edi.get_document_list(date, type_=2)
    documents_class_by_secCode = {}

    for document in document_list["results"]:
        if document["legalStatus"] != 0:
            if document["secCode"] not in documents_class_by_secCode:
                documents_class_by_secCode[document["secCode"]] = []
            documents_class_by_secCode[document["secCode"]].append((
                document["docDescription"],
                document["docID"],
                document["filerName"]
            ))

    with open("documents.json", "w", encoding="utf-8") as f:
        json.dump(documents_class_by_secCode, f, indent=4, ensure_ascii=False)
    return documents_class_by_secCode


def sanitize_filename(filename):
    """ファイル名に使用できない文字を置き換える。"""
    import re
    return re.sub(r'[\/:*?"<>|]', '_', filename)


def download_pdf(edi, doc_id, file_name):
    """指定したドキュメントIDのPDFをダウンロードして保存する。"""
    try:
        content = edi.get_document(doc_id, type_=2)
        with open(file_name, "wb") as f:
            f.write(content)
        print(f"PDF downloaded and saved as {file_name}")
    except Exception as e:
        print(f"Failed to download PDF for document ID {doc_id}. Error: {e}")


def main():
    # ダウンロード先ディレクトリを設定
    download_directory = "downloads"
    os.makedirs(download_directory, exist_ok=True)

    # ユーザーから日付を入力させる
    date_str = input("Please enter the date in YYYY-MM-DD format: ")

    # 日付を解析し、datetimeオブジェクトに変換する
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    # APIキーを環境変数"API_KEY"から持ってくる
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        print("API_KEY environment variable not set.")
        return
    
    edi = Edinet(API_KEY)

    # ドキュメント一覧を取得して保存
    documents_class_by_secCode = get_and_save_document_list(edi, date)

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
                download_pdf(edi, document[1], file_name)
        else:
            print("指定された銘柄コードに対応する書類は見つかりませんでした。")
        
        another = input("他の銘柄コードを確認しますか？ y/n: ")
        if another.lower() != 'y':
            break


if __name__ == "__main__":
    main()
