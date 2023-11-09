# Mkdocs Plugin to inline SVGs

A [MkDocs plugin] that inlines SVG images matching a pattern into the output without inlining Materials theme icons.

This differs from previously developed plugins in several ways:

- it does not use a regex to find images in Markdown.  It parses the
  generated HTML, and
- it can be configured to only inline SVGs with paths matching a
  pattern, and
- it parses the SVG and removes SVG elements that are marked
  `.do-not-inline`.

----

This plugin operates post HTML generation looking for `img` elements like

```html
<img src="foo.svg" ...>
```

When the *src* is a path-local URL with a path component that ends
with `.svg` and it matches the configured pattern then the file is
read from the local file system and inlined in place.

Alt text is ignored in favour of any SVG `<title>` element.

If the SVG contains any elements marked with `class="do-not-inline"`,
they will not be included in the inlined content.
This is useful when your SVG images contain `<style>` elements that
you do not want to bleed into the containing scope, and your Mkdocs
configuration includes extra CSS stylesheets that suffice.

## Usage

To download and install this module, run:

```sh
pip install mkdocs-inline-select-svg-plugin
```

Enable the plugin in your *mkdocs.yml* by adding `inline-select-svg` as a list item under the *plugins* section.  Since that section will almost certainly include *search* you might end up with something like this:

```yaml
plugins:
    - search
    - inline-select-svg
```

If you want to filter which SVGs to inline, by path, you can specify a regular expression using the *pattern* config option thus:

```yaml
plugins:
    - search
    - inline-select-svg:
        pattern: "[.]inline[.]svg$"
```

With that configuration, `<img src="../foo.inline.svg">` would be
inlined but `<img src="../foo.svg">` would not.

[MkDocs plugin]: https://www.mkdocs.org/dev-guide/plugins/
