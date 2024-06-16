from os import environ
from datetime import datetime
from edinet import Edinet


# APIキーを環境変数"API_KEY"から持ってくる
API_KEY = environ["API_KEY"]

edi = Edinet(API_KEY)

#ドキュメント一覧を取得
document_list = edi.get_document_list(datetime.today(), type_=2)

#seccodeをキーとした辞書の作成
documents_class_by_seccode: dict[str, list[tuple[str, str, str]]] = {}
