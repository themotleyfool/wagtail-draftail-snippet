import factory

from .models import Advert


class AdvertFactory(factory.Factory):
    class Meta:
        model = Advert

    url = "https://www.example.com"
    text = "Example"
