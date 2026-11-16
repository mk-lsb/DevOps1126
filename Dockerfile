# ベースイメージはバージョンを固定する（latest にしない）
FROM python:3.12-slim

# ビルドするときに焼き込む値：どのコミットから作ったイメージか
# CI では --build-arg APP_VERSION=コミットID を渡す
ARG APP_VERSION=local
ENV APP_VERSION=${APP_VERSION} \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY app/ /app/

# 管理者権限で動かさない
USER nobody

EXPOSE 8000
CMD ["python", "app.py"]

# 環境ごとに違う値（APP_ENV, DB_HOST, DB_PASSWORD）はここに書かない。
# 起動するときに環境変数で渡す（12-Factor「3. 設定」）
