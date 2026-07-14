# tutorial/steps ブランチについて

RareTechのFlask/Docker学習用ステップと、参考サンプルSNSをまとめたブランチ。
**このブランチは`develop`/`main`にはマージしない**（学習用の参考資料置き場）。

## 起動方法(共通)

各フォルダに移動して、それぞれ個別に起動する。

```sh
cd <フォルダ名>
docker-compose up
```

`Ctrl+C`で停止、次のstepを見る前に`docker-compose down`しておくこと。

## 各stepの内容

| フォルダ | URL | ブラウザで見れる？ | 内容 |
|---|---|---|---|
| step145 | http://localhost:5104 | △(テキストAPI) | `/`, `/time`, `/date`など複数のテキストAPIエンドポイント。DBは使わない |
| step159 | http://localhost:5100 | ✕(テキストのみ) | Flask+MySQLの最小構成。`/`と`/db`がプレーンテキストを返すだけ |
| step160 | http://localhost:5101 | ✕(JSON API) | `/users`にPOST/GETでユーザーの作成・一覧ができるAPI化ステップ。curlかPostman推奨 |
| step161 | http://localhost:5102 | ○ | `/users/new`(登録フォーム)・`/users/list`(一覧)でHTML画面が初めて出てくるステップ |
| step162 | http://localhost:5103 | ○ | step161と同じHTML画面に、DB接続のエラーハンドリングを追加した堅牢化版 |
| sns-sample | http://localhost:55001 | ○ | ログイン/サインアップ・投稿一覧・投稿詳細まで揃った参考SNSアプリ。起動前に`cp .env.example .env`が必要 |

## 補足

- MySQLを使うstep(159〜162)は、ポート番号(Flask/MySQLとも)を全部ずらしてあるので、同時に複数起動しても衝突しない
- `sns-sample`は独立したgitリポジトリだったものをコード部分だけ取り込んだもの(`.git`・`.env`は除外済み)
