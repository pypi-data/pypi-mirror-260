from typing import Any
from typing import Iterable
from typing import List
from typing import Tuple


def append(hub, c1: List[str], c2) -> List[str]:
    """
    Append two comments, no matter their type
    """
    if not c2:
        return
    if not isinstance(c1, list):
        raise TypeError(f"First comment must be a list")

    if isinstance(c2, (str, bytes)) or not isinstance(c2, Iterable):
        c2 = [c2]

    c1.extend(c2)


def flatten(hub, comment: Iterable[Any]) -> List[Any]:
    """
    Take a comment that may be a list of lists and flatten it
    """
    flat_list = []
    for item in comment:
        if item is None or (not item and isinstance(item, Iterable)):
            continue
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes, dict)):
            flattened = hub.tool.idem.comment.flatten(item)
            flat_list.extend(flattened)
        else:
            flat_list.append(item)

    return flat_list


def normalize(hub, comment: Any) -> List[str]:
    """
    Take an object of any type and turn it into a list
    """
    if comment is None or (not comment and isinstance(comment, Iterable)):
        comment = []
    elif isinstance(comment, Tuple):
        comment = list(comment)
    elif isinstance(comment, (str, bytes, dict)) or not isinstance(comment, Iterable):
        comment = [comment]

    return hub.tool.idem.comment.flatten(comment)
