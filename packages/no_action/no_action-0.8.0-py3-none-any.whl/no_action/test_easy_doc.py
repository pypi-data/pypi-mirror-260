"""Testing file for EasyDoc class."""

from pytest import raises as p_raises
from .easy_doc import EasyDoc
from .exceptions import MissingDocstringException


class Dummy:
    """A docstring for the Dummy class.

    It is multiline, having one summary line at the top, and also having a docstring "body" that is
    separated from that summary line by a blank line of whitespace. The EasyDoc class should be able
    to clean and format this docstring into it's respective parts and make them easily accessable
    for classes that need docstring introspection.
    """


ed_dummy = EasyDoc(Dummy.__doc__)


def test_original_correct():
    """Test attribute 'original', correct case."""
    assert ed_dummy.original == Dummy.__doc__


def test_title_correct():
    """Test attribute 'title', correct case."""
    assert ed_dummy.title == "A docstring for the Dummy class."


def test_body_correct():
    """Test attribute 'body', correct case."""
    body = """
It is multiline, having one summary line at the top, and also having a docstring "body" that is
separated from that summary line by a blank line of whitespace. The EasyDoc class should be able
to clean and format this docstring into it's respective parts and make them easily accessable
for classes that need docstring introspection."""
    assert ed_dummy.body == body


def test_cleaned_original_correct():
    """Test attribute 'cleaned_original', correct case."""
    cleaned = """A docstring for the Dummy class.

It is multiline, having one summary line at the top, and also having a docstring "body" that is
separated from that summary line by a blank line of whitespace. The EasyDoc class should be able
to clean and format this docstring into it's respective parts and make them easily accessable
for classes that need docstring introspection."""
    assert ed_dummy.cleaned_original == cleaned


class DummyNoDoc:  # pylint: disable=missing-class-docstring
    def a(self):
        """Pass and do nothing."""


def test_initialization():
    """Test __init__ method throws a MissingDocstringException if the docstring is empty."""
    with p_raises(MissingDocstringException):
        EasyDoc(DummyNoDoc.__doc__)


class DummyAOnly:
    """a."""


ed_dummy_aonly = EasyDoc(DummyAOnly.__doc__)


def test_title_aonly():
    """Test attribute 'title', from a title-only docstring case."""
    assert ed_dummy_aonly.title == "a."


def test_body_aonly():
    """Test attribute 'body' from a title-only docstring case."""
    assert ed_dummy_aonly.body is None
