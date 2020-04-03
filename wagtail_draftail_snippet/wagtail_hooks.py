from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.core import hooks

from . import urls
from .richtext import (
    ContentstateSnippetLinkConversionRule, ContentstateSnippetEmbedConversionRule,
    SnippetLinkHandler, SnippetEmbedHandler,
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
            {"type": type_, "icon": "snippet", "description": ugettext("Snippet Link")},
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
            {"type": type_, "icon": "code", "description": ugettext("Snippet Embed")},
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
    return format_html(
        """
            <script>
                window.chooserUrls.snippetLinkModelChooser = '{0}';
                window.chooserUrls.snippetEmbedModelChooser = '{1}';
            </script>
        """,
        reverse("wagtaildraftailsnippet:choose-snippet-link-model"),
        reverse("wagtaildraftailsnippet:choose-snippet-embed-model"),
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [url(r"^snippets/", include(urls, namespace="wagtaildraftailsnippet"))]
