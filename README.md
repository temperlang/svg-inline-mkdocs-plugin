# mkdocs-plugin-inline-select-svg

A [MkDocs plugin] that inlines SVG images matching a pattern into the output without inlining Materials theme icons.

This operates post HTML generation looking for `img` elements like

```html
<img src="foo.inline.svg" ...>
```

When the *src* is a path-local URL with a path component that ends
with `.svg` and it matches the configured pattern then the file is
read from the local file system and inlined in place.

Alt text is ignored in favour of any SVG `<title>` element.

## Usage

Enable the plugin in your mkdocs.yml:

```yaml
plugins:
    - search
    - inline-select-svg
      pattern: "[.]inline[.]svg$"
```

[MkDocs plugin]: https://www.mkdocs.org/dev-guide/plugins/
