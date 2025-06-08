# myproject/myproject/ は、Djangoのプロジェクト設定ファイル一式が入っているディレクトリです。

# Procfile
# web:	Render（または Heroku）に「これはWebプロセスです」と伝える識別子
# gunicorn	Python用の本番向けWSGI HTTPサーバー（高速・軽量）
# myproject.wsgi	DjangoのWSGI起動ポイント。myproject/wsgi.py にある application を起動