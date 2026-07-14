# Flask-API-Project
こちらのハンズオンでは、Pythonの軽量ウェブフレームワークであるFlaskを利用したAPIを作成します。

## 使用言語とバージョン

![](https://img.shields.io/badge/python-v3.7.3-blue?style=plastic)
![](https://img.shields.io/badge/flask-v2.2.2-blue?style=plastic)

## API

| エンドポイント | method | コマンド例                                                                                 |                             |
| -------------- | ------ | ------------------------------------------------------------------------------------------ | --------------------------- |
| /              | GET    | `curl localhost:5000`                                                                      | メッセージを返す |
| /time          | GET    | `curl localhost:5000/time`                                                                 | 現在時刻を返す              |
| /date          | GET    | `curl -X POST -d 'days=2022-10-03' http://localhost:5000/date`                             | 入力した日付から曜日を算出  |
| /aphorism      | GET    | `curl localhost:5000/aphorism`                                                             | 偉人の名言を返す            |
| /fortune       | GET    | `curl localhost:5000/fortune`                                                              | ポジティブおみくじ          |
| /message       | POST   | `curl -X POST -d 'name=kazu' http://localhost:5000/message`                                | 労いの言葉を返す            |
| /login         | POST   | `curl -X POST -d '{"username": "hoge", "password": "123456"}' http://localhost:5000/login` | ログイン機能のサンプル      |

## 環境構築
以下、macでの環境を想定しています。

### 1. virtualenv によるPython環境の構築
Python での仮想環境を構築するため、virtualenv をインストールする。

```bash
pip3 install virtualenv
```

以下のエラーが発生した場合、コマンドの先頭に`sudo`をつけて再度実行する。
```bash
Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Library/Python/3.7'Consider using the `--user` option or check the permissions. 
```  

```bash
sudo pip3 install virtualenv
```

次に、プロジェクトを作成したいディレクトリへ移動し、下記コマンドを実行する。 こちらのコマンドにより、移動したディレクトリに virtualenv の設定ファイルが作成される。
```bash
virtualenv env
```
次に、以下のコマンドで virtualenv を有効化する。  
```bash
source env/bin/activate
```

virtualenvでの環境構築が成功した場合、以下のように、プロンプトの前に()でvirtualenvコマンドを実行した時の名前が表示される。
```bash
(env)user@hoge|ディレクトリ
```

### 2. Flask のインストール
以下のコマンドで、Flask をインストールする。
```bash
pip3 install flask
```

### 3. app.py の作成
現在のディレクトリにファイル`app.py`を作成する。  
```bash
touch app.py
```  

作成した`app.py`ファイルに以下の内容を記述する。

```python
from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello World'


if __name__ == "__main__":
    app.run(debug=True)
```

## 4. サーバーの立ち上げ
`app.py`ファイルと同じディレクトリにて、以下のコマンドを実行し、APIサーバーを起動する。
`http://localhost:5000`にブラウザでアクセスし、`Hello World`が表示されると完了です。
```bash
flask run
```

