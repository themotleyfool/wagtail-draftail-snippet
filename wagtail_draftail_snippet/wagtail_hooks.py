from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks

from . import urls
from .richtext import ContentstateSnippetLinkConversionRule, SnippetLinkHandler


@hooks.register("register_rich_text_features")
def register_snippet_feature(features):
    feature_name = "snippet"
    type_ = "SNIPPET"

    features.register_link_type(SnippetLinkHandler)

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {"type": type_, "icon": "snippet", "description": ugettext("Snippet")},
            js=[
                "wagtailsnippets/js/snippet-chooser-modal.js",
                "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js",
                "wagtail_draftail_snippet/js/wagtail_draftail_snippet.js",
            ],
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetLinkConversionRule
    )


@hooks.register("insert_editor_js")
def editor_js():
    return format_html(
        """
            <script>window.chooserUrls.snippetModelChooser = '{0}';</script>
        """,
        reverse("wagtaildraftailsnippet:choose_snippet_model"),
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [url(r"^snippets/", include(urls, namespace="wagtaildraftailsnippet"))]
