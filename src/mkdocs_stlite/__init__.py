import logging
import tomllib
from dataclasses import dataclass
from typing import TypedDict

from bs4 import BeautifulSoup
from jinja2 import Template
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

logger = logging.getLogger(__name__)
template = Template("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/browser@0.76.0/build/style.css">
<style>
.stlite-block {
  .stApp, .stApp .stAppHeader, .stApp .stAppViewContainer {
    position: relative;
  }
}
</style>
<script type="module" defer>
import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.76.0/build/stlite.js";
{% for block in blocks %}
mount(
  {
    {%- if block.front_matter.requirements -%}
    requirements: [{% for r in block.front_matter.requirements %}"{{ r }}",{% endfor %}],
    {%- endif -%}
    entrypoint: "{{ block.files.items()|first|first }}",
    files: {
        {% for filename, source in block.files.items() %}
        "{{ filename }}": `
{{ source }}
        `,
        {% endfor %}
    }
  },
  document.getElementById("{{ block.id }}"),
)
{% endfor %}
</script>
""")


class FrontMatter(TypedDict):
    requirements: list[str]


@dataclass
class StliteBlock:
    files: dict[str, str]
    id: str = "root"
    front_matter: FrontMatter | None = None

    @classmethod
    def parse(cls, source: str, filename: str = "app.py"):
        if not source.startswith("---\n"):
            return cls(files={filename: source})
        parts = source.split("---\n")
        front_matter: FrontMatter = tomllib.loads(parts[1])
        return cls(files={filename: parts[2]}, front_matter=front_matter)


class StlitePlugin(BasePlugin):
    def on_post_page(
        self, output: str, /, *, page: Page, config: MkDocsConfig
    ) -> str | None:
        soup = BeautifulSoup(
            output, "html.parser", preserve_whitespace_tags={"pre", "code"}
        )
        blocks: list[StliteBlock] = []
        for elm in soup.find_all("pre"):
            if (
                not elm.code
                or "class" not in elm.code.attrs
                or "language-stlite" not in elm.code["class"]
            ):
                continue
            # Convert
            try:
                block = StliteBlock.parse(elm.code.text)
                elm.name = "div"
                elm.clear()
                elm["id"] = block.id
                elm["class"] = "stlite-block"
                blocks.append(block)
            except ValueError as err:
                logger.error(err)
                return soup.prettify(formatter="html5")
        if blocks:
            soup.head.append(
                BeautifulSoup(template.render(blocks=blocks), "html.parser")
            )
        return soup.prettify(formatter="html5")
