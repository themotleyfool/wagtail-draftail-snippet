from django.conf.urls import url

from .views import choose_snippet_link_model, choose_snippet_embed_model


app_name = "wagtaildraftailsnippet"

urlpatterns = [
    url(r"^choose-link-model/$", choose_snippet_link_model, name="choose-snippet-link-model"),
    url(r"^choose-embed-model/$", choose_snippet_embed_model, name="choose-snippet-embed-model"),
]
