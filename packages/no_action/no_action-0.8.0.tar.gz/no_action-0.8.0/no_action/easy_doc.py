"""Defines the EasyDoc class that will be used to parse the docstring of a Step.

EasyDoc parses and provides sane attributes for various parts of the docstring.
"""

from inspect import cleandoc
from typing import Optional
from loguru import logger

from .exceptions import MissingDocstringException


class EasyDoc:
    """EasyDoc parses and exposes parts of a docstring.

    Attributes:
        original:
            The original text passed in.
        cleaned_original:
            Original docstring that has the indentation removed.
        title:
            The first line of the docstring.
        body:
            The body of the docstring.

    """

    def __init__(self, doc: Optional[str]) -> None:
        """Initialize and ingest the original doc and call parsing functions.

        Args:
            doc: The docstring.

        Raises:
            MissingDocstringException

        """
        logger.info("Initialize the EasyDoc")
        try:
            assert doc is not None
            logger.debug(f"Passed docstring: {doc}")
            self.original: str = doc
            # Clean the whitespace
            self.cleaned_original: str = cleandoc(doc)

            self.title: Optional[str] = self.__parse_title()
            logger.info(f"title: {self.title}")

            self.body: Optional[str] = self.__parse_body()
            logger.info(f"body: {self.body}")
        except AssertionError as err:
            logger.error("The docstring is empty, cannot parse.")
            raise MissingDocstringException("Docstring is empty.") from err

    def __parse_title(self) -> Optional[str]:
        # Attempt to split out the first line only.
        splits: list[str] = self.cleaned_original.split(sep="\n", maxsplit=1)
        if len(splits) > 0:
            return splits[0]
        return None

    def __parse_body(self) -> Optional[str]:
        # Split out the body only.
        splits: list[str] = self.cleaned_original.split(sep="\n", maxsplit=1)
        if len(splits) > 1:
            del splits[0]
            return "\n".join(splits)
        return None
