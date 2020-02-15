import pytest
from wagtail.core.models import Site

from tests.testapp import factories


@pytest.fixture
def site():
    site = Site.objects.get(is_default_site=True)
    return site


@pytest.fixture()
def advert():
    advert = factories.AdvertFactory(text="advert", url="https://www.example.com")
    advert.save()
    yield advert
