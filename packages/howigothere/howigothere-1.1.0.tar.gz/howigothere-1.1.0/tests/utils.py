"""
Testing utilities.
"""

import unittest
from typing import Optional

from howigothere import howigothere


try:
    import colorama  # noqa: W0601
except ImportError:
    pass
else:
    raise RuntimeError(
        "tests must be run in an environment that doesn't provide colorama.\n"
        "Try using a virtual environment:\n"
        "    python -m venv venv && . venv/bin/activate && pip install -r"
        " requirements_dev.txt && ./run_tests.sh && deactivate",
    )


class TestsBase(unittest.TestCase):
    """
    The base unit tests class, used as a foundation for all other unit tests.
    """

    def setUp(self):
        """
        For future uses (common resets between runs).
        """
        pass

    def tearDown(self):
        """
        For future uses (common resets between runs).
        """
        pass


class SomeClass:

    @staticmethod
    def some_method(
        start_from_dir: Optional[str | tuple[str, ...]],
        *,
        show_args: bool = False,
    ):
        def some_inner_function(show_args: bool) -> str:
            return howigothere(
                no_color=True,
                start_from_dir=start_from_dir,
                show_args=show_args,
            )
        return some_inner_function(show_args)


class _MockColoramaConstant:

    def __getattr__(self, name: str) -> str:
        return "foo"


class MockColorama:

    Back = _MockColoramaConstant()
    Fore = _MockColoramaConstant()
    Style = _MockColoramaConstant()
