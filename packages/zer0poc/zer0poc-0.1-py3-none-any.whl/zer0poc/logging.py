class Logger:
    """
    A class for logging messages with different prefixes and colors.

    Attributes:
        SUCCESS_PREFIX (str): The prefix for success messages.
        SUCCESS_TEXT_COLOR (str): The color for success messages.

        INFO_PREFIX (str): The prefix for info messages.
        INFO_TEXT_COLOR (str): The color for info messages.

        FAILURE_PREFIX (str): The prefix for failure messages.
        FAILURE_TEXT_COLOR (str): The color for failure messages.

        RESET_COLOR (str): The color reset code.

        indent_unit (str): The string used for indentation.

    Methods:
        info(message, indent=1, end='\n'): Prints an info message with the specified indentation.
        success(message, indent=1, end='\n'): Prints a success message with the specified indentation.
        fail(message, indent=1, end='\n', exit_flag=False): Prints a failure message with the specified indentation.
    """

    def __init__(self, indent_length: int = 4) -> None:
        """
        Initializes a new instance of the Logger class.

        Args:
            indent_length (int): The length of each indentation unit.
        """
        
        self.SUCCESS_PREFIX = "\033[92m[*]\033[0m"
        self.SUCCESS_TEXT_COLOR = "\033[94m"

        self.INFO_PREFIX = "\033[33m[info]\033[0m"
        self.INFO_TEXT_COLOR = "\033[93m"

        self.FAILURE_PREFIX = "\033[90m[!]\033[0m"
        self.FAILURE_TEXT_COLOR = "\033[91m"

        self.RESET_COLOR = "\033[0m"

        self.indent_unit = " " * indent_length

    def info(self, message, indent: int = 1, end='\n'):
        """
        Prints an info message with the specified indentation.

        Args:
            message (str): The message to be printed.
            indent (int): The number of indentation units.
            end (str): The string appended after the message. Defaults to '\n'.
        """
        print(
            self.indent_unit * indent + f"{self.INFO_PREFIX} {self.INFO_TEXT_COLOR}{message}{self.RESET_COLOR}",
            end=end,
        )

    def success(self, message, indent: int = 1, end='\n'):
        """
        Prints a success message with the specified indentation.

        Args:
            message (str): The message to be printed.
            indent (int): The number of indentation units.
            end (str): The string appended after the message. Defaults to '\n'.
        """
        print(
            self.indent_unit * indent + f"{self.SUCCESS_PREFIX} {self.SUCCESS_TEXT_COLOR}{message}{self.RESET_COLOR}",
            end=end,
        )

    def fail(self, message, indent: int = 1, end='\n', exit_flag: bool = False):
        """
        Prints a failure message with the specified indentation.

        Args:
            message (str): The message to be printed.
            indent (int): The number of indentation units.
            end (str): The string appended after the message. Defaults to '\n'.
            exit_flag (bool): Whether to exit the program after printing the message. Defaults to False.
        """
        print(
            self.indent_unit * indent + f"{self.FAILURE_PREFIX} {self.FAILURE_TEXT_COLOR}{message}{self.RESET_COLOR}",
            end=end,
        )
        
        if exit_flag: 
            exit(0)