import re
import os

import mkdocs
import mkdocs.config
import mkdocs.config.config_options
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote_plus, urljoin

class MkdocsInlineSelectSvgConfig(mkdocs.config.base.Config):
    """
    pattern: str: a regex used to filter the img src URL's path.
                  If it matches, then the image tag is inlined.
    """
    pattern = mkdocs.config.config_options.Type(str, default='[.]svg$')

class MkdocsInlineSelectSvgPlugin(mkdocs.plugins.BasePlugin[MkdocsInlineSelectSvgConfig]):
    """
    Replaces <img src="foo.svg"> with the inlined SVG content when
    the src URL matches the conditions from ../README.md.
    """

    def on_page_content(self, html, page, config, files, **kwargs):
        """
        Runs post translation of the Markdown into HTML to do
        the substitution.

        After the markdown has been translated to HTML, we have
        direct programmatic access to <img> elements.
        """
        from_md_path = page.file.src_path
        docs_dir  = config.docs_dir
        pattern = re.compile(self.config.pattern)
        site_url = config.site_url
        page_url = urlparse(page.url)
        site_url_path = urlparse(site_url).path

        # Parse the HTML
        soup = BeautifulSoup(html, features='html.parser')
        # Find all img elements
        imgs = soup.find_all('img')
        changed_soup = False
        for img in imgs:
            img_src = img['src']
            try:
                img_url = urlparse(img_src)
            except:
                continue
            if img_url.scheme or img_url.netloc or not img_url.path:
                # Skip over non local file paths
                continue
            if not img_url.path.endswith('.svg'):
                continue
            resolved_url_path = urljoin(page_url.path, img_url.path)
            if not pattern.search(resolved_url_path): continue
            mkdocs.utils.log.info(
                '%s: processing img src=%s',
                self.log_prefix(),
                img_src
            )

            # If img_url                   is '../foo+bar.svg'
            # and page.url                 is 'dir/page/'
            # and the mkdocs root          is 'C:\my\mkdocs\'
            # then the resolved img url    is 'dir/foo+bar.svg'
            # and that converted to a file is 'dir\foo bar.svg'
            # so the file to load          is 'C:\my\mkdocs\dir\foo bar.svg'
            fs_path_parts = [
                unquote_plus(x) for x in resolved_url_path.split('/')
            ]
            abs_fs_path = os.path.join(config.docs_dir, *fs_path_parts)
            try:
                svg_content = open(abs_fs_path, 'r').read()
                svg_soup = BeautifulSoup(svg_content, 'xml')
            except:
                svg_soup = None
                mkdocs.utils.log.error(
                    '%s: could not read SVG content from %s',
                    self.log_prefix(),
                    self.__abs_fs_path
                )
            if svg_soup is not None:
                # strip out elements related marked with class="do-not-inline"
                for to_remove in svg_soup.find_all('.do-not-inline'):
                    to_remove.replace_with()
                # TODO: rewrite any relative path URLs
                # and to scope nested `<style>` elements.
                img.replace_with(svg_soup)
                changed_soup = True

        if changed_soup:
            return str(soup)
        else:
            return html

    def log_prefix(self): return type(self).__name__
