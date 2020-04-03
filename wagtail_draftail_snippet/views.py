from django.template.loader import TemplateDoesNotExist, get_template

from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.snippets.models import get_snippet_models

from .utils import get_snippet_link_frontend_template, get_snippet_embed_frontend_template


def choose_snippet_link_model(request):
    snippet_model_opts = []

    # Only display those snippet models which have snippet link frontend template
    for snippet_model in get_snippet_models():
        snippet_frontend_template = get_snippet_link_frontend_template(
            snippet_model._meta.app_label, snippet_model._meta.model_name
        )

        try:
            get_template(snippet_frontend_template)
            snippet_model_opts.append(snippet_model._meta)
        except TemplateDoesNotExist:
            pass

    return render_modal_workflow(
        request,
        "wagtail_draftail_snippet/choose_snippet_model.html",
        None,
        {"snippet_model_opts": snippet_model_opts},
        json_data={"step": "choose"},
    )


def choose_snippet_embed_model(request):
    snippet_model_opts = []

    # Only display those snippet models which have snippet embed frontend template
    for snippet_model in get_snippet_models():
        snippet_frontend_template = get_snippet_embed_frontend_template(
            snippet_model._meta.app_label, snippet_model._meta.model_name
        )

        try:
            get_template(snippet_frontend_template)
            snippet_model_opts.append(snippet_model._meta)
        except TemplateDoesNotExist:
            pass

    return render_modal_workflow(
        request,
        "wagtail_draftail_snippet/choose_snippet_model.html",
        None,
        {"snippet_model_opts": snippet_model_opts},
        json_data={"step": "choose"},
    )
