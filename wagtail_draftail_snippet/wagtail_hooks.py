from django.urls import include, path
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.core import hooks

from . import urls
from .richtext import (
    ContentstateSnippetLinkConversionRule,
    ContentstateSnippetEmbedConversionRule,
    SnippetLinkHandler,
    SnippetEmbedHandler,
)


@hooks.register("register_rich_text_features")
def register_snippet_link_feature(features):
    feature_name = "snippet-link"
    type_ = "SNIPPET"

    features.register_link_type(SnippetLinkHandler)

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {"type": type_, "icon": "snippet", "description": gettext("Snippet Link")},
            js=[
                "wagtailsnippets/js/snippet-chooser-modal.js",
                "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js",
                "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js",
            ],
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetLinkConversionRule
    )


@hooks.register("register_rich_text_features")
def register_snippet_embed_feature(features):
    feature_name = "snippet-embed"
    type_ = "SNIPPET-EMBED"

    features.register_embed_type(SnippetEmbedHandler)

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {"type": type_, "icon": "code", "description": gettext("Snippet Embed")},
            js=[
                "wagtailsnippets/js/snippet-chooser-modal.js",
                "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js",
                "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js",
            ],
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetEmbedConversionRule
    )


@hooks.register("insert_editor_js")
def editor_js():

    html = f"""
            <script>
                window.chooserUrls.snippetChooser = '{reverse('wagtaildraftailsnippet:choose_generic')}';
                window.chooserUrls.snippetLinkModelChooser = '{reverse("wagtaildraftailsnippet:choose-snippet-link-model")}';
                window.chooserUrls.snippetEmbedModelChooser = '{reverse("wagtaildraftailsnippet:choose-snippet-embed-model")}';
            </script>    
            """

    return format_html(html)


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [path("snippets/", include(urls, namespace="wagtaildraftailsnippet"))]
