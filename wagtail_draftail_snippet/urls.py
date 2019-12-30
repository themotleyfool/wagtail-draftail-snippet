from django.conf.urls import url

from .views import choose_snippet_model


app_name = "wagtaildraftailsnippet"

urlpatterns = [
    url(r"^choose-model/$", choose_snippet_model, name="choose_snippet_model")
]
