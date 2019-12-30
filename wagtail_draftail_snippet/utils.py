from wagtail.core.utils import camelcase_to_underscore


def get_snippet_frontend_template(app_name, model_name):
    return "%s/%s_snippet.html" % (app_name, camelcase_to_underscore(model_name))
