# wagtail-draftail-snippet

Wagtail has support for adding numerous types of links to `RichTextBlock` content, but there is not a way to tie a link to an arbitrary `snippet` model currently. `wagtail-draftail-snippet` provides a way to add a new button to the Draftail rich text editor, which creates an `a href` element for a specific `snippet` model based on a template that can be provided.


## Install

1. Add `wagtail_draftail_snippet` to `INSTALLED_APPS` in Django settings
1. Add `"snippet"` to the `features` keyword list argument when instantiating a `RichTextBlock`, e.g. `paragraph = RichTextBlock(features=["bold", "italic", "h1", "h2", "h3", "snippet"])`
1. Create a frontend template to determine how the snippet model will be rendered. Frontend templates are required for a snippet to  be selected and are discovered when they match a path like `{app_name}/{model_name}_snippet.html`. For example, if you have an `Affiliate` snippet model in `affiliates/models.py`, then a file in `affiliates/templates/affiliates/affiliate_snippet.html` would be required.


## Example use-case

Wagtail is used for a content site that will display articles that have affiliate links embedded inside the content. Affiliate links have a snippet data model to store information with a URL, start, and end dates; the urls need to be rendered in such a way that JavaScript can attach an event listener to their clicks for analytics.

When the content gets rendered, it uses the specific affiliate model to get the URL stored in the snippet model. If the affiliate's URL ever changes, the snippet can be changed in the Wagtail admin, and the all of the content will use the correct link when rendered.

An example frontend template in `affiliates/templates/affiliates/affiliate_snippet.html` could be the following.
```
<a href="{{ object.url }}" data-vars-action="content-cta" data-vars-label="{{ object.slug }}" rel="sponsored">
```


## Build the library

1. `poetry build`


## Contributors

- [Parbhat Puri](https://github.com/Parbhat)
- [Adam Hill](https://github.com/adamghill/)


## License

[BSD](https://github.com/themotleyfool/wagtail-draftail-snippet/blob/master/LICENSE)
