from functools import reduce
from ..plugin import get_contexts_from_modules
from .methods import default_methods
from .properties import default_properties


def get_all_context(**kwargs):
    array = [default_methods | default_properties, *get_contexts_from_modules(**kwargs)[::-1]]
    return reduce(lambda x, y: x | y, array, {})
