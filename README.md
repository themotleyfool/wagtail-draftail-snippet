# wagtail-draftail-snippet

Wagtail has support for adding numerous types of links to `RichText` content, but there is not a way to tie a link to an arbitrary `snippet` model currently. `wagtail-draftail-snippet` provides a way to create either an `a href` element for a specific `snippet` model based on a template that can be provided, or a completely free-form piece of HTML for a snippet.

The project provides the following draftail (Wagtail Richtext editor) features:

1. `snippet-link`: Allows to create a link using the snippet chooser modal. The link is rendered using the template `{app_name}/{model_name}_snippet_link.html`.
1. `snippet-embed`: Allows to embed a block using the snippet chooser modal. The block is embedded using the template `{app_name}/{model_name}_snippet_embed.html`.

Unsure whether you want to use a snippet link or embed? Embeds have complete flexibility, but 1) break the flow of text in the Draftail richtext editor and 2) can't be used to link arbitrary text. If you want to render a link to a snippet model inside of body copy, then you probably want to use the snippet link. For anything else, the embed can be used.

![Demo of wagtail-draftail-snippet plugin](draftail-snippet-demo.gif)

## Install

1. `pip install wagtail-draftail-snippet`
1. Add `wagtail_draftail_snippet` to `INSTALLED_APPS` in Django settings
1. Add `"snippet-link"` and `"snippet-embed"` to the `features` keyword list argument when instantiating a `RichTextBlock`, e.g. `paragraph = RichTextBlock(features=["bold", "italic", "h1", "h2", "h3", "snippet-link", "snippet-embed"])`
1. Create a frontend template to determine how the snippet model will be rendered. Frontend templates are required for a snippet to be selected and are discovered when they match a path like `{app_name}/{model_name}_snippet_link.html` and `{app_name}/{model_name}_snippet_embed.html`. For example, if you have an `Affiliate` snippet model in `affiliates/models.py`, then a file in `affiliates/templates/affiliates/affiliate_snippet_link.html` and `affiliates/templates/affiliates/affiliate_snippet_embed.html` would be required.

## Example use-case

Wagtail is used for a content site that will display articles that have affiliate links embedded inside the content. Affiliate links have a snippet data model to store information with a URL, start, and end dates; the urls need to be rendered in such a way that JavaScript can attach an event listener to their clicks for analytics.

When the content gets rendered, it uses the specific affiliate model to get the URL stored in the snippet model. If the affiliate's URL ever changes, the snippet can be changed in the Wagtail admin, and the all of the content will use the correct link when rendered.

An example frontend template in `affiliates/templates/affiliates/affiliate_snippet_link.html` could be the following.

```
<a href="{{ object.url }}" data-vars-action="content-cta" data-vars-label="{{ object.slug }}" rel="sponsored">
```

## Requirements

The package requires Wagtail 2.5 or above.

## Build the library

1. `poetry build`

## Push a new version release to PyPI

Travis-CI will build the library and deploy it to PyPI on every commit to `master` that is tagged with a version.

## Run tests

1. `poetry install`
1. `poetry run pytest`

## Contributors

- [Parbhat Puri](https://github.com/Parbhat)
- [Adam Hill](https://github.com/adamghill/)
- [Brady Moe](https://github.com/bmoe872/)

## License

[BSD](https://github.com/themotleyfool/wagtail-draftail-snippet/blob/master/LICENSE)
