import contextvars
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Iterable,
    Pattern,
    TypeAlias,
    cast,
)

from bs4 import SoupStrainer
from bs4.element import Tag

if TYPE_CHECKING:
    from ..component import Component
    from .context_manager import TagContextManager

weba_html_context: contextvars.ContextVar[Any] = contextvars.ContextVar("current_weba_html_context")


Incomplete: TypeAlias = Any
_SimpleStrainable: TypeAlias = str | bool | None | bytes | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
_Strainable: TypeAlias = _SimpleStrainable | Iterable[_SimpleStrainable]
_SimpleNormalizedStrainable: TypeAlias = (
    str | bool | None | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
)
_NormalizedStrainable: TypeAlias = _SimpleNormalizedStrainable | Iterable[_SimpleNormalizedStrainable]

Render = None | Coroutine[Any, Any, None]


class TagMixins(Tag):
    _html: "Component"

    def select_one(self, selector: str, namespaces: Any = None, **kwargs: Any) -> "TagContextManager":
        """Perform a CSS selection operation on the current element.

        :param selector: A CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param kwargs: Keyword arguments to be passed into Soup Sieve's
           soupsieve.select() method.

        :return: A Tag.
        :rtype: bs4.element.Tag
        """
        if self._content is None:
            tag = super().select_one(selector, namespaces, **kwargs)
        else:
            tag = self._content.select_one(selector, namespaces, **kwargs)

        if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
            tag = self._tag_context_manager(tag)  # type: ignore

        return cast("TagContextManager", tag)

    def select(  # type: ignore TODO: fix instead of ignoring
        self,
        selector: str,
        namespaces: Incomplete | None = None,
        limit: int | None = None,
        *,
        flags: int = 0,
        custom: dict[str, str] | None = None,
    ) -> list["TagContextManager"]:
        """Perform a CSS selection operation on the current element.

        This uses the SoupSieve library.

        :param selector: A string containing a CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param limit: After finding this number of results, stop looking.

        :param kwargs: Keyword arguments to be passed into SoupSieve's
           soupsieve.select() method.

        :return: A ResultSet of Tags.
        :rtype: bs4.element.ResultSet
        """
        if self._content is None:
            tags = super().select(selector, namespaces, limit, flags=flags, custom=custom)
        else:
            tags = self._content.select(selector, namespaces, limit, flags=flags, custom=custom)

        context_tags: list["TagContextManager"] = []

        for tag in tags:
            if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
                tag = self._tag_context_manager(tag)  # type: ignore

            context_tags.append(cast("TagContextManager", tag))

        return context_tags

    def find_next_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = None,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> "TagContextManager":
        """Find the closest sibling to this PageElement that matches the
        given criteria and appears later in the document.

        All find_* methods take a common set of arguments. See the
        online documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
        if attrs is None:
            attrs = {}
        if self._content is None:
            tag = super().find_next_sibling(name, attrs, string, **kwargs)
        else:
            tag = self._content.find_next_sibling(name, attrs, string, **kwargs)

        if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
            tag = self._tag_context_manager(tag)  # type: ignore

        return cast("TagContextManager", tag)

    def find_previous_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = None,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> "TagContextManager":
        """Returns the closest sibling to this PageElement that matches the
        given criteria and appears earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
        if attrs is None:
            attrs = {}

        if self._content is None:
            tag = super().find_previous_sibling(name, attrs, string, **kwargs)
        else:
            tag = self._content.find_previous_sibling(name, attrs, string, **kwargs)

        if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
            tag = self._tag_context_manager(tag)  # type: ignore

        return cast("TagContextManager", tag)

    def find(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = None,
        recursive: bool = True,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> "TagContextManager":
        """Look in the children of this PageElement and find the first
        PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """

        if attrs is None:
            attrs = {}

        if self._content is None:
            tag = super().find(name, attrs, recursive, string, **kwargs)
        else:
            tag = self._content.find(name, attrs, recursive, string, **kwargs)

        if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
            tag = self._tag_context_manager(tag)  # type: ignore

        return cast("TagContextManager", tag)

    def find_all(  # type: ignore TODO: fix instead of ignoring
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = None,
        recursive: bool = True,
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> list["TagContextManager"]:
        """Look in the children of this PageElement and find all
        PageElements that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find_all() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
        if attrs is None:
            attrs = {}

        if self._content is None:
            tags = super().find_all(name, attrs, recursive, string, limit, **kwargs)
        else:
            tags = self._content.find_all(name, attrs, recursive, string, limit, **kwargs)  # type: ignore

        context_tags: list["TagContextManager"] = []

        for tag in tags:
            if tag.__class__.__name__ == "Tag" and callable(getattr(self, "_tag_context_manager", None)):
                tag = self._tag_context_manager(tag)  # type: ignore

            context_tags.append(cast("TagContextManager", tag))

        return context_tags
