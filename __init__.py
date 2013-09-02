import functools
import os
import shutil
import signal
import time
import unittest
import warnings
from .dogtail_gui_helper import gnome_apps_helper as helpers  # noqa


# Create a dummy unittest class to have nice assertions
class dummy(unittest.TestCase):
    def runTest(self):  # pylint: disable=R0201
        assert True


def deprecated(replacement=None):
    """A decorator which can be used to mark functions as deprecated.
    replacement is a callable that will be called with the same args
    as the decorated function.

    >>> @deprecated()
    ... def foo(x):
    ...     return x
    ...
    >>> ret = foo(1)
    DeprecationWarning: foo is deprecated
    >>> ret
    1
    >>>
    >>>
    >>> def newfun(x):
    ...     return 0
    ...
    >>> @deprecated(newfun)
    ... def foo(x):
    ...     return x
    ...
    >>> ret = foo(1)
    DeprecationWarning: foo is deprecated; use newfun instead
    >>> ret
    0
    >>>

    Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
    License: MIT
    Originally from
    http://code.activestate.com/recipes/577819-deprecated-decorator/
    """
    def outer(oldfun):
        def inner(*args, **kwargs):
            msg = "%s is deprecated" % oldfun.__name__
            if replacement is not None:
                msg += "; use %s instead" % (replacement.__name__)
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            if replacement is not None:
                return replacement(*args, **kwargs)
            else:
                return oldfun(*args, **kwargs)
        return inner
    return outer


def wait_until(my_lambda, element, timeout=30, period=0.25):
    """
    This function keeps running lambda with specified params until the result is True
    or timeout is reached
    Sample usages:
     * wait_until(lambda x: x.name != 'Loading...', context.app.instance)
       Pause until window title is not 'Loading...'.
       Return False if window title is still 'Loading...'
       Throw an exception if window doesn't exist after default timeout

     * wait_until(lambda element, expected: x.text == expected, element, ('Expected text'))
       Wait until element text becomes the expected (passed to the lambda)

    """
    exception_thrown = None
    mustend = int(time.time()) + timeout
    while int(time.time()) < mustend:
        try:
            if my_lambda(element):
                return True
        except Exception as e:
            # If lambda has thrown the exception we'll re-raise it later
            # and forget about if lambda passes
            exception_thrown = e
        time.sleep(period)
    if exception_thrown:
        raise exception_thrown
    else:
        return False


def timeout(func, args=(), expected=True, equals=True, timeout=30, period=0.25):
    """
    This function waits until specified function returns required result

    Sample usage:
       * timeout(a.__getattribute__)
         returns True if a was set to True in 30 seconds
       * timeout(class.__getattribute__, "a")
         returns True if class.a was set to True
       * timeout(class.__getattribute__, "a", expected=1)
         returns True if class.a was set to 1
       * timeout(class.__getattribute__, "a", expected=1, equals=False)
         returns True if class.a was set to any value except False

       From evo code:
       * assert timeout(context.app.categories.__getattribute__, "dead"),\
             "New category dialog is still opened"
       * assert timeout(dupl_dialog.__getattribute__, "showing", expected=False),\
        "Duplicate Contact dialog was not closed"
       * assert timeout(dupl_dialog.__getattribute__, "showing", expected=False),\
        "Duplicate Contact dialog was not closed"
    """
    mustend = int(time.time()) + timeout
    while int(time.time()) < mustend:
        res = func.__call__(args)
        if equals:
            if res == expected:
                return True
        else:
            if res != expected:
                return True
        time.sleep(period)
    return False


class TimeoutError(Exception):
    pass


def limit_execution_time_to(seconds=10, error_message=os.strerror(os.errno.ETIME)):
    """
    Decorator to limit function execution to specified limit
    """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return functools.wraps(func)(wrapper)

    return decorator


class App(helpers.App):
    def __init__(self, *args, **kwargs):
        for one_dir in kwargs.pop('clean_dirs', []):
            shutil.rmtree(one_dir, ignore_errors=True)
        super(App, self).__init__(*args, **kwargs)
