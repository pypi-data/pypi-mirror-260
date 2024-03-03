from typing import Callable


class CliFashion(object):

    def __init__(self):
        """Module initialization"""

    def error(self, text: str):
        """Prints an error statement."""

        line = "\033[31m[✕] " + text + "\033[m"
        line = "\n" + line

        print(line)

    def success(self, text: str):
        """Prints a success statement."""

        line = "\033[32m[✓] " + text + "\033[m"
        line = "\n" + line

        print(line)

    def warning(self, text: str):
        """Prints a warning statement."""

        line = "\033[33m[!] " + text + "\033[m"
        line = "\n" + line

        print(line)

    def text(self, text: str):
        """Prints a text statement."""

        line = text
        line = "\n" + line

        print(line)

    def debug(self, text: str):
        """Prints a notice statement."""

        line = "[#] " + text
        line = "\n" + line

        print(line)

    def notice(self, text: str):
        """Prints a notice statement."""

        line = "\033[34m[~] " + text + "\033[m"
        line = "\n" + line

        print(line)

    def ask(self, question: str, default, validator=Callable[[str], str]):
        """Asks to the user an input and validates the value with the given validator function."""

        line = "\n[?] " + question

        if default:
            line += " [" + str(default) + "]"

        line += ": "

        while True:
            value = str(input(line))

            try:
                validator(value)
                return value
            except ValueError as e:
                self.error(str(e))
