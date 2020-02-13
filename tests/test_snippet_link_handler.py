import pytest

from tests.testapp import factories
from wagtail_draftail_snippet.richtext import SnippetLinkHandler


@pytest.mark.django_db
def test_snippet_link_handler():
    advert = factories.AdvertFactory(text='advert', url='https://www.example.com')
    advert.save()

    assert advert.text == 'advert'
    assert advert.url == 'https://www.example.com'

    # Empty link created in case of exception
    result = SnippetLinkHandler.expand_db_attributes({'id': 0})
    assert result == "<a>"

    # Test snippet template render correctly
    attrs = {'id': 1, 'data-app-name': 'testapp', 'data-model-name': 'Advert'}
    result = SnippetLinkHandler.expand_db_attributes(attrs)
    assert result == f'<a href="{ advert.url }/{ advert.id }">'
