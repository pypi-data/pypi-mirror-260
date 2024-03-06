import re
import string

from openpyxl_style_writer import CustomStyle

from .driver import ExcelDriver


def set_custom_style(style_name: str, style: CustomStyle):
    ExcelDriver.set_custom_style(style_name, style)


def separate_alpha_numeric(input_string: str):
    alpha_part = re.findall(r'[a-zA-Z]+', input_string)
    num_part = re.findall(r'[0-9]+', input_string)
    return alpha_part[0], num_part[0]


def _is_valid_column(column: str) -> bool:
    column = column.upper()
    index = 0
    for c in column:
        index = index * 26 + (ord(c) - ord('A')) + 1
    return 1 <= index <= 16384


def column_to_index(column: str) -> int:
    if not isinstance(column, str):
        raise TypeError(f'Invalid type ({type(column)}). Column should be a string.')
    if len(column) > 3:
        raise ValueError(f"Invalid column ({column}). Maximum Column is 'XFD'.")
    if not all(c in string.ascii_uppercase for c in column):
        raise ValueError(f'Invalid column ({column}). Column should be in uppercase.')
    if not _is_valid_column(column):
        raise ValueError(f"Invalid column ({column}). Maximum Column is 'XFD'.")
    column = column.upper()
    index = 0
    for c in column:
        index = index * 26 + (ord(c) - ord('A')) + 1
    return index


def index_to_column(index: int) -> str:
    if not isinstance(index, int):
        raise TypeError(f'Invalid type ({type(index)}). Index should be a string.')
    if index < 1 or index > 16384:
        raise ValueError(f'Invalid index ({index}). Index should less and equal to 16384.')
    name = ''
    while index > 0:
        index, r = divmod(index - 1, 26)
        name = chr(r + ord('A')) + name
    return name
