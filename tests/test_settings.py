import os

from wagtail import __version__

WAGTAIL_MAJOR_VERSION = int(__version__.split(".", 1)[0])
WT_CORE_APP_PATH = "wagtail.core"
if WAGTAIL_MAJOR_VERSION >= 3:
    WT_CORE_APP_PATH = "wagtail"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (("test@example.com", "TEST-R"),)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "tests.db"}}

SECRET_KEY = "_uobce43e5osp8xgsffssffsds2_16%y$sf*5(12vfg25hpnxik_*"

INSTALLED_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    WT_CORE_APP_PATH,
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # App Under test
    "wagtail_draftail_snippet",
    # Test app
    "tests.testapp",
]


MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    WT_CORE_APP_PATH + ".middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = "tests.urls"

WAGTAIL_SITE_NAME = ("Test Site",)
SITE_ID = 1
