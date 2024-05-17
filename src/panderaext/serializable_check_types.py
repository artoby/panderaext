# pylint: disable=global-statement,global-variable-not-assigned,no-else-return

from functools import wraps
from typing import TYPE_CHECKING

import pandera as pa

# Pandera checks can be disabled as sometimes they drive to memory leaks. Observed the leak in Optuna pipeline
#   with pandera==0.9.0 (Python 3.7), pandera==0.10.1 (Python 3.8).
__PANDERA_CHECK_ENABLED: bool = True


def set_pandera_checks_enabled(enabled: bool) -> None:
    global __PANDERA_CHECK_ENABLED
    __PANDERA_CHECK_ENABLED = enabled


def pandera_check_types(func):
    """Makes pandera check_types serializable, otherwise notebooks won't be reproducible in Yandex DataSphere
    Fix idea: http://gael-varoquaux.info/programming/decoration-in-python-done-right-decorating-and-pickling.html
    """

    @wraps(func)
    def inner_func(*args, **kwargs):
        global __PANDERA_CHECK_ENABLED
        if __PANDERA_CHECK_ENABLED:
            wrapper = pa.check_types(func)
        else:
            wrapper = func
        return wrapper(*args, **kwargs)

    # In TYPE_CHECKING mode we return the source func for the annotations to properly be displayed in IDE.
    #   In realtime a type checked wrapper is returned
    if TYPE_CHECKING:
        return func
    else:
        return inner_func
