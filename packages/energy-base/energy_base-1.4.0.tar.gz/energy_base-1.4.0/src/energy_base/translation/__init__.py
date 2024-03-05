from typing import Callable, Any

from energy_base.translation.utils import translate

trans = translate
t = translate
_: Callable[[str], str] = translate

__all__ = [
    'translate'
    'trans',
    't',
    '_'
]
