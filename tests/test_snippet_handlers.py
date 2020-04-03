import pytest
from wagtail_draftail_snippet.richtext import SnippetLinkHandler, SnippetEmbedHandler


class TestSnippetLinkHandler:
    @pytest.mark.django_db
    def test_advert_setup_correctly(self, advert):
        assert advert.text == "advert"
        assert advert.url == "https://www.example.com"

    @pytest.mark.django_db
    def test_snippet_create_empty_link_on_error(self, advert):
        """
        Empty link created in case of exception
        """

        result = SnippetLinkHandler.expand_db_attributes({"id": 0})
        assert result == "<a>"

    @pytest.mark.django_db
    def test_snippet_link_handler_renders(self, advert):
        """
        Test snippet template renders correctly
        """

        attrs = {"id": 1, "data-app-name": "testapp", "data-model-name": "Advert"}
        result = SnippetLinkHandler.expand_db_attributes(attrs)
        assert result == f'<a href="{advert.url}/{advert.id}">'


class TestSnippetEmbedHandler:
    @pytest.mark.django_db
    def test_advert_setup_correctly(self, advert):
        assert advert.text == "advert"
        assert advert.url == "https://www.example.com"

    @pytest.mark.django_db
    def test_snippet_create_empty_block_on_error(self, advert):
        """
        Empty block created in case of exception
        """

        result = SnippetEmbedHandler.expand_db_attributes({"id": 0})
        assert result == ""

    @pytest.mark.django_db
    def test_snippet_embed_handler_renders(self, advert):
        """
        Test snippet template renders correctly
        """

        attrs = {"id": 1, "data-app-name": "testapp", "data-model-name": "Advert"}
        result = SnippetEmbedHandler.expand_db_attributes(attrs)
        assert result == f'<div>{advert.text}</div>'
