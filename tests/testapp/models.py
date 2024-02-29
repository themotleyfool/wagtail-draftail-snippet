from django.db import models
from wagtail import __version__

WAGTAIL_MAJOR_VERSION = int(__version__.split(".", 1)[0])

if WAGTAIL_MAJOR_VERSION >= 3:
    from wagtail.admin.panels import FieldPanel
else:
    from wagtail.admin.edit_handlers import FieldPanel

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Advert(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel("url"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.text
