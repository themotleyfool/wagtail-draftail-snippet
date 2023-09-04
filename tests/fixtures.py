import pytest

from tests.testapp import factories
from wagtail import __version__


WAGTAIL_MAJOR_VERSION = int(__version__.split(".", 1)[0])

if WAGTAIL_MAJOR_VERSION >= 3:
    from wagtail.models import Site
else:
    from wagtail.core.models import Site


@pytest.fixture
def site():
    site = Site.objects.get(is_default_site=True)
    return site


@pytest.fixture()
def advert():
    advert = factories.AdvertFactory(text="advert", url="https://www.example.com")
    advert.save()
    yield advert
