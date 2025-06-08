import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # .envファイルから環境変数を読み込む

# プロジェクトのルートディレクトリを定義
BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティキー（.envで管理、本番環境で必ず秘密にする）
SECRET_KEY = os.environ.get('SECRET_KEY')

# 開発環境(DEBUG="True")か本番環境(DEBUG="False")かを環境変数で切り替え（DEBUGの値は.envで管理）
DEBUG = os.getenv("DEBUG", "False") == "True"

# アクセスを許可するホスト（開発：ローカル、本番：外部からのアクセスを許可）
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] 
else:
    ALLOWED_HOSTS = ['*']

# アプリケーション定義（このプロジェクトに含まれるアプリ）
INSTALLED_APPS = [ #有効化されたアプリ一覧（member もここで登録）
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig', #mainアプリを参照
    'member.apps.MemberConfig', #memberアプリを参照
    'accounting.apps.AccountingConfig', #accountingアプリを参照
    'practice_management.apps.PracticeManagementConfig', #practice_managementアプリを参照
    'cloudinary', # Cloudinary（画像保存用）
    'cloudinary_storage',
]

# Cloudinaryを使ってメディアファイルを保存
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# リクエスト処理の中間処理（セキュリティ、CSRF、セッション、認証など）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静的ファイルを本番で効率的に配信
]

# ルートURLconfの指定（urls.py）
ROOT_URLCONF = 'myproject.urls' #メインURLファイル（urls.py）のパス

# テンプレートの設定（HTMLテンプレートの探索ディレクトリなど）
TEMPLATES = [ #テンプレートの設定（DIRSでテンプレートフォルダ指定）
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# WSGIアプリケーションのエントリポイント
WSGI_APPLICATION = 'myproject.wsgi.application'

# データベース設定（環境変数がある場合はPostgreSQL、ない場合はSQLite）
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# パスワードバリデーション（ログイン時のセキュリティ強化）
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 国際化設定（日本語、タイムゾーン）
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# 静的ファイル（CSS, JS など）の設定
STATIC_URL = '/static/' # URLルート
STATICFILES_DIRS = [BASE_DIR / "static"] # ソースとなる静的ファイルの場所
STATIC_ROOT = BASE_DIR / "staticfiles" # collectstaticで集約される場所
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# メディアファイル（アップロード画像など）の保存先
if DEBUG:
    MEDIA_ROOT = BASE_DIR / "media" # ローカル保存
else:
    MEDIA_ROOT = "/media/" # RenderのVolumeマウント先

# ログイン・ログアウト後のリダイレクト先
LOGIN_REDIRECT_URL = "/main/"
LOGOUT_REDIRECT_URL = "/login/"

# 主キーのデフォルト設定（IDカラムの型）
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")