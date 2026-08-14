# MySQL8系のイメージを指定
FROM mysql:8.0

# MySQLのローカルの設定ファイルをコンテナにコピー
COPY Docker/MySQL/my.cnf /etc/mysql/conf.d/my.cnf
# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY Docker/MySQL/00_init.sql /docker-entrypoint-initdb.d/00_init.sql
# seedsディレクトリのファイルもエントリーポイントに含めるために同じディレクトリにコピー
COPY Docker/MySQL/seeds/ /docker-entrypoint-initdb.d/