from typing import Optional
from .markdown import parse_markdown, unparse_html

class Parser:
    def __init__(self):
        # Initializes the Parser; can be extended to include more parsers or configuration.
        pass

    def parse(self, text: str, mode: Optional[str] = "markdown"):
        """
        Parses text from Markdown to HTML or other formats depending on the mode.

        :param text: The input text to be parsed.
        :param mode: The parsing mode (e.g., "markdown" to HTML). Default is "markdown".
        :return: The parsed text.
        """
        text = text.strip()

        if mode == "markdown":
            return parse_markdown(text)
        elif mode is None or mode == "disabled":
            # Return text as is if parsing is disabled or not specified
            return text
        else:
            raise ValueError(f"Unsupported parse mode: {mode}")

    def unparse(self, text: str, mode: Optional[str] = "html"):
        """
        Converts text from HTML back to Markdown or other formats depending on the mode.

        :param text: The input HTML text to be unparsed.
        :param mode: The unparse mode (e.g., "html" to Markdown). Default is "html".
        :return: The unparsed text.
        """
        if mode == "html":
            return unparse_html(text)
        elif mode is None or mode == "disabled":
            # Return text as is if unparsing is disabled or not specified
            return text
        else:
            raise ValueError(f"Unsupported unparse mode: {mode}")
