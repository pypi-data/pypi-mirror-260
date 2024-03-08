from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.w3.org/1999/xlink"


class ActuateValue(Enum):
    ON_LOAD = "onLoad"
    ON_REQUEST = "onRequest"
    OTHER = "other"
    NONE = "none"


@dataclass
class Arcrole:
    class Meta:
        name = "arcrole"
        namespace = "http://www.w3.org/1999/xlink"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Href:
    class Meta:
        name = "href"
        namespace = "http://www.w3.org/1999/xlink"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Role:
    class Meta:
        name = "role"
        namespace = "http://www.w3.org/1999/xlink"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class ShowValue(Enum):
    NEW = "new"
    REPLACE = "replace"
    EMBED = "embed"
    OTHER = "other"
    NONE = "none"


@dataclass
class Title:
    class Meta:
        name = "title"
        namespace = "http://www.w3.org/1999/xlink"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Actuate:
    """The 'actuate' attribute is used to communicate the desired timing of
    traversal from the starting resource to the ending resource;

    it's value should be treated as follows:
    onLoad - traverse to the ending resource immediately on loading
    the starting resource
    onRequest - traverse from the starting resource to the ending
    resource only on a post-loading event triggered for
    this purpose
    other - behavior is unconstrained; examine other markup in link
    for hints
    none - behavior is unconstrained
    """

    class Meta:
        name = "actuate"
        namespace = "http://www.w3.org/1999/xlink"

    value: Optional[ActuateValue] = field(default=None)


@dataclass
class Show:
    """The 'show' attribute is used to communicate the desired presentation of the
    ending resource on traversal from the starting resource; it's.

    value should be treated as follows:
    new - load ending resource in a new window, frame, pane, or other
    presentation context
    replace - load the resource in the same window, frame, pane, or
    other presentation context
    embed - load ending resource in place of the presentation of the
    starting resource
    other - behavior is unconstrained; examine other markup in the
    link for hints
    none - behavior is unconstrained
    """

    class Meta:
        name = "show"
        namespace = "http://www.w3.org/1999/xlink"

    value: Optional[ShowValue] = field(default=None)
