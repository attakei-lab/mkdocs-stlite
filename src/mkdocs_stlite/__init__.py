from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


class StlitePlugin(BasePlugin):
    def on_post_page(
        self, output: str, /, *, page: Page, config: MkDocsConfig
    ) -> str | None:
        return output

