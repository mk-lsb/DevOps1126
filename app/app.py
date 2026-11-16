"""DevOps研修 デモ用の小さなWebアプリ

いま自分が「どの環境で」「どの設定で」動いているかを返すだけのアプリです。

- APP_VERSION … イメージを作るときに焼き込む値（どの環境でも同じ）
- APP_ENV / DB_HOST / DB_PASSWORD … 起動するときに外から渡す値（環境ごとに違う）

ライブラリは使わず、Python標準の http.server だけで動きます。
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def render(env=None):
    """画面に出す文字列を作る。テストしやすいように、環境変数を引数で渡せるようにしてある"""
    env = os.environ if env is None else env
    password = "設定あり" if env.get("DB_PASSWORD") else "設定なし"  # 値そのものは絶対に出さない
    lines = [
        f"環境       : {env.get('APP_ENV', 'local')}",
        f"DB接続先   : {env.get('DB_HOST', 'localhost')}",
        f"パスワード : {password}",
        f"ビルド     : {env.get('APP_VERSION', 'local')}",
    ]
    return "\n".join(lines) + "\n"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = "ok\n"
        elif self.path == "/":
            body = render()
        else:
            self.send_response(404)
            self.end_headers()
            return
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"listening on 0.0.0.0:{port}", flush=True)  # ログは標準出力へ（12-Factor「11. ログ」）
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
