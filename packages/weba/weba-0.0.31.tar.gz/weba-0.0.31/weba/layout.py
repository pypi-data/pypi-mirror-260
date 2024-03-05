import json
import pathlib
from typing import TYPE_CHECKING, Any, NotRequired, Unpack

from weba import HTML, HTMLKwargs, env, ui

if TYPE_CHECKING:
    from .component import Component, Tag


def load_manifest(name: str) -> dict[str, Any]:
    if not env.is_prd:
        return {}

    manifest = pathlib.Path(f"dist/manifest-{name}.json").read_text()

    return json.loads(manifest)


class LayoutKwargs(HTMLKwargs):
    header: NotRequired["Component"]
    main: NotRequired["Component"]
    footer: NotRequired["Component"]


class Layout(HTML):
    src = """--html
        <!doctype html>
        <html lang="en-US">

        <head>
            <title>Weba</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>

        <body>
            <header/>
            <main />
            <footer />
        </body>

        </html>
    """

    header: "Tag"
    main: "Tag"
    footer: "Tag"

    manifest: dict[str, Any] = load_manifest("main")

    title = "Weba"

    lang = "en-US"

    def __init__(self, *_args: Any, **kwargs: Unpack[LayoutKwargs]):
        self.lang = kwargs.get("lang", self.__class__.lang)
        self.title = kwargs.get("title", self.__class__.title)

    def render(self):
        super().render()

        if env.is_prd:
            self.remove_script_tags()
            self.remove_link_tags()

            # loop over key value pairs in manifest and append to head
            for _, info in self.manifest.items():
                js_file = info["file"]
                css_files = info.get("css", [])

                self.body.append(ui.script(src=js_file, type="module"))

                for css_file in css_files:
                    self.head.append(ui.link(href=css_file, rel="stylesheet", type="text/css"))

                # NOTE: Until we have proper critical css detection this will slow down the page load using hx-boost
                # for css_file in css_files:
                #     css = pathlib.Path(f"dist/{css_file}").read_text()
                #     self.head.append(ui.style(css))
        else:
            for script in self.select("script"):
                script["src"] = f"{env.script_dev_url_prefix}/{script['src']}"

    def remove_script_tags(self):
        for script in self.select("script"):
            script.decompose()

    def remove_link_tags(self):
        for link in self.select("link"):
            link.decompose()

    def add(self, page: "Component"):
        header = page.find("header", recursive=False)
        footer = page.find("footer", recursive=False)
        main = page.find("main", recursive=False) or page

        if header:
            self.add_content(self.header, "header", header.extract())

        if footer:
            self.add_content(self.footer, "footer", footer.extract())

        self.add_content(self.main, "main", main)

    def add_content(self, tag: "Tag", tag_name: str, content: "Tag"):
        if content.name == tag_name:
            classes = tag["class"]
            attrs = tag.attrs or {}

            self.replace_content(tag, content, classes, attrs)
        else:
            tag.append(content)

    def replace_content(self, tag: "Tag", content: "Tag", classes: Any, attrs: dict[str, Any]):
        classes = content["class"] if content.has_attr("class") else []

        if classes:
            for class_ in classes:
                if class_ not in classes:
                    classes.append(class_)

        child_main_attrs = content.attrs

        tag.replace_with(content)
        tag.attrs = attrs
        tag.attrs.update(child_main_attrs)
        tag["class"] = classes
