# E-Team_2026-Summer

「つどい」開発リポジトリ。

## セットアップ

初回・`git pull`後は毎回、以下を実行する。

```sh
# 1. 環境変数ファイルを作成(.envはgitignoreされているので各自作成が必要)
cp .env.example .env

# 2. Dockerビルド&起動
docker-compose up --build
```

起動できたら、ブラウザで以下を開いて確認する。

```
http://localhost:55000/signup
```

「Hello World / 新規登録画面(仮)」が表示されればDB・Flaskとも正常に動いている。

## 停止

```sh
docker-compose down
```

## トラブルシューティング

- `container name ... already in use` というエラーが出たら、同じ名前のコンテナが他で動いている。`docker ps -a` で確認し、不要なら `docker rm <コンテナID>` で削除する
