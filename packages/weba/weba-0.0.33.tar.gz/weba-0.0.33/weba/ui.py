from typing import TYPE_CHECKING, Any, Callable

from .component import Component, weba_html_context
from .tag.context_manager import TagContextManager

if TYPE_CHECKING:
    from bs4 import Tag


# Define a class that will act as a factory for creating UI elements
class UIFactory:
    def __getattr__(self, tag_name: str) -> Callable[..., TagContextManager]:
        def create_tag(*args: Any, **kwargs: Any) -> TagContextManager:
            html_context = weba_html_context.get(None)

            if html_context is None or not callable(html_context.new_tag):
                html_context = Component()
                weba_html_context.set(html_context)

            # Handle different variations of the class attribute
            class_variants = ["_class", "class_", "klass", "cls"]

            for variant in class_variants:
                if variant in kwargs:
                    # Move the value to the 'class' key
                    kwargs["class"] = kwargs.pop(variant)
                    break

            # if kwargs contains "hx_" convert it to hx-, so for example:
            # hx_oob_swap -> hx-oob-swap
            for key in list(kwargs.keys()):
                if key.startswith("hx_"):
                    value = kwargs.pop(key)
                    key = key.replace("_", "-")
                    kwargs[key] = value

            tag: Tag = html_context.new_tag(tag_name, **kwargs)  # type: ignore

            if args:
                tag.string = args[0]

            # Check if there is a current context and append the tag to it
            if html_context:  # type: ignore
                if html_context._context_stack:  # type: ignore
                    current_context = html_context._context_stack[-1]  # type: ignore
                    current_context.append(tag)
                if html_context._last_component is None:  # type:ignore
                    html_context._last_component = tag  # type:ignore

            return TagContextManager(tag, html_context)  # type: ignore

        return create_tag


ui = UIFactory()
