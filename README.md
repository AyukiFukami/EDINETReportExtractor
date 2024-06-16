使用方法

リポジトリをクローン:
```sh
git clone https://github.com/AyukiFukami/EDINETReportExtractor
cd edinet-document-downloader

```

このレポジトリを使うには、edinet_wrap ライブラリがインストールされている必要があります。
インストールされていない場合は、インストールしてください。

```sh
pip install edinet_wrap
```

環境変数としてEDINET APIキーを設定します。
```sh
export API_KEY="your_edinet_api_key"
```
yyyy-mm-dd形式で日付を入力し、銘柄コードを入力することでその会社のEdinet上での書類を確認できます。
まだ実用的な機能は少なく、これから追加していく予定です。
