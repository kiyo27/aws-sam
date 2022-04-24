# Lambda packaging and deploy

## 関数を zip にまとめる

zip を作成

```
python package.py
```

artifacts ディレクトリに関数ごとに zip が作成される

## Lambda にデプロイ

zip を lambda にアップロード

```
python deploy.py <function name>
```
