import pytest


@pytest.fixture
def site():
    from wagtail.core.models import Site
    site = Site.objects.get(is_default_site=True)
    return site
