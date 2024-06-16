使用方法

リポジトリをクローン:
```sh
git clone https://github.com/AyukiFukami/EDINETReportExtractor
cd edinet-document-downloader

```

このレポジトリを使用するには、edinet_wrap ライブラリが必要です。
まだインストールされていない場合は、以下のコマンドを実行してください。

```sh
pip install edinet_wrap
```

環境変数としてEDINET APIキーを設定します。
```sh
export API_KEY="your_edinet_api_key"
```
yyyy-mm-dd形式で日付を入力し、銘柄コードを入力することでその会社のEdinet上での書類を確認できます。
まだ機能は少なく、これから追加していく予定です。
