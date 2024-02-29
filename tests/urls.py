from django.conf.urls import include, url
from wagtail import __version__
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

WAGTAIL_MAJOR_VERSION = int(__version__.split(".", 1)[0])

if WAGTAIL_MAJOR_VERSION >= 3:
    from wagtail import urls as wagtail_urls
else:
    from wagtail.core import urls as wagtail_urls


urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"", include(wagtail_urls)),
]
