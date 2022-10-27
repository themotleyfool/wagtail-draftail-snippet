# 0.4.2

Upgrade required version of Wagtail to >=2.15.x (feature implemented in 0.4.0)

# 0.4.1

Support Django 4.x and Wagtail 3.x

# 0.4.0

Fix issue when upgrading to Wagtail 2.14.x.

# 0.3.2

Fix issue when upgrading to Wagtail 2.11.x.

# 0.3.0

Adds the ability for snippets to be either a link (current functionality) or a block element.

## Breaking changes

- `snippet` Wagtail feature renamed to `snippet-link`
- template search looks for `{model}_snippet_link.html` instead of `{model}_snippet.html`

# 0.2.2

Update travis-ci configuration.

# 0.2.0

Add edit and remove tooltip in the editor to the linked snippet.

# 0.1.2

Initial release.
