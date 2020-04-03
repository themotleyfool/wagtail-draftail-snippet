from django.apps import apps
from django.template.loader import render_to_string

from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.contentstate_models import Entity
from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler, AtomicBlockEntityElementHandler
from wagtail.core.rich_text import EmbedHandler, LinkHandler

from .utils import get_snippet_link_frontend_template, get_snippet_embed_frontend_template


# Snippet Link

# Front-end conversion
class SnippetLinkHandler(LinkHandler):
    identifier = "snippet"

    @classmethod
    def get_instance(cls, attrs):
        model = apps.get_model(attrs["data-app-name"], attrs["data-model-name"])
        return model.objects.get(id=attrs["id"])

    @classmethod
    def get_template(cls, attrs):
        return get_snippet_link_frontend_template(
            attrs["data-app-name"], attrs["data-model-name"]
        )

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            snippet_obj = cls.get_instance(attrs)
            template = cls.get_template(attrs)
            return render_to_string(template, {"object": snippet_obj})
        except Exception:
            return "<a>"


# draft.js / contentstate conversion
def snippet_link_entity(props):
    """
    Helper to construct elements of the form
    <a id="1" linktype="snippet">snippet link</a>
    when converting from contentstate data
    """

    # props["children"] defaults to the string representation of the model if it's missing
    selected_text = props["children"]

    elem = DOM.create_element(
        "a",
        {
            "linktype": "snippet",
            "id": props.get("id"),
            "data-string": props.get("string"),
            "data-edit-link": props.get("edit_link"),
            "data-app-name": props.get("app_name"),
            "data-model-name": props.get("model_name"),
        },
        selected_text,
    )

    return elem


class SnippetLinkElementHandler(LinkElementHandler):
    """
    Rule for populating the attributes of a snippet link when converting from database representation
    to contentstate
    """

    def get_attribute_data(self, attrs):
        return {
            "id": attrs.get("id"),
            "string": attrs.get("data-string"),
            "edit_link": attrs.get("data-edit-link"),
            "app_name": attrs.get("data-app-name"),
            "model_name": attrs.get("data-model-name"),
        }


ContentstateSnippetLinkConversionRule = {
    "from_database_format": {
        'a[linktype="snippet"]': SnippetLinkElementHandler("SNIPPET")
    },
    "to_database_format": {"entity_decorators": {"SNIPPET": snippet_link_entity}},
}


# Snippet Embed

# Front-end conversion
class SnippetEmbedHandler(EmbedHandler):
    identifier = "snippet"

    @classmethod
    def get_instance(cls, attrs):
        model = apps.get_model(attrs["data-app-name"], attrs["data-model-name"])
        return model.objects.get(id=attrs["id"])

    @classmethod
    def get_template(cls, attrs):
        return get_snippet_embed_frontend_template(
            attrs["data-app-name"], attrs["data-model-name"]
        )

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            snippet_obj = cls.get_instance(attrs)
            template = cls.get_template(attrs)
            return render_to_string(template, {"object": snippet_obj})
        except Exception:
            return ""


# draft.js / contentstate conversion
def snippet_embed_entity(props):
    """
    Helper to construct elements of the form
    <embed embedtype="snippet" id="1"/> when converting from contentstate data
    """

    elem = DOM.create_element(
        "embed",
        {
            "embedtype": "snippet",
            "id": props.get("id"),
            "data-string": props.get("string"),
            "data-edit-link": props.get("edit_link"),
            "data-app-name": props.get("app_name"),
            "data-model-name": props.get("model_name"),
        }
    )

    return elem


class SnippetEmbedElementHandler(AtomicBlockEntityElementHandler):
    """
    Rule for building a snippet entity when converting from database representation
    to contentstate
    """

    def create_entity(self, name, attrs, state, contentstate):
        return Entity('SNIPPET-EMBED', 'IMMUTABLE', {
            "id": attrs.get("id"),
            "string": attrs.get("data-string"),
            "edit_link": attrs.get("data-edit-link"),
            "app_name": attrs.get("data-app-name"),
            "model_name": attrs.get("data-model-name"),
        })


ContentstateSnippetEmbedConversionRule = {
    "from_database_format": {
        'embed[embedtype="snippet"]': SnippetEmbedElementHandler()
    },
    "to_database_format": {"entity_decorators": {"SNIPPET-EMBED": snippet_embed_entity}},
}
