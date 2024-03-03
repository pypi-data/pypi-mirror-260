import re

# use re.MULTILINE flag (equals inline modifier (?m)) to make ^ and $ match
# and start/end of each line instead of just start/end of whole string
# https://docs.python.org/3/library/re.html#re.MULTILINE


def format_cell_delimiters(text: str) -> str:
    """Ensure single space between hash and double-percent.

    --- before ---
    #   %%
    #%%
    --- after ---
    # %%
    # %%
    """
    return re.sub(r"(?m)^#\s*%%", r"# %%", text)


def format_comments_after_cell_delimiters(text: str) -> str:
    """Ensure single space between cell delimiter and possible comment on same line.

    --- before ---
    # %%some comment
    # %%     another comment
    --- after ---
    # %% some comment
    # %% another comment
    """
    # [^\S\n\r] = not non-whitespace and not new line or carriage return
    return re.sub(r"(?m)^# %%[^\S\n\r]*(\S)", r"# %% \g<1>", text)


def remove_empty_cells(text: str) -> str:
    """Remove empty cells.

    --- before ---
    # %% some comment

    # %%
    --- after ---
    # %% some comment
    """
    text = re.sub(r"(?m)^# %%(?:\s+# %%)+", r"# %%", text)
    return re.sub(r"(?m)^# %%([^\n]*)(?:\s+# %%$)+", r"# %%\g<1>", text)


def remove_empty_lines_starting_cell(text: str) -> str:
    """Remove empty lines from start of cell.

    --- before ---
    # %% comment

    first_code = 'here'
    --- after ---
    # %% comment
    first_code = 'here'
    """
    # (?:\n\s*){2,} = non-capturing group for two or more new lines containing
    # only optional white space
    return re.sub(r"(?m)^(# %%[^\n]*)(?:\n\s*){2,}", r"\g<1>\n", text)


def ensure_two_blank_lines_preceding_cell(text: str) -> str:
    """Ensure every cell delimiters has two preceding blank lines.
    Adds/deletes lines if there are less/more.

    --- before ---
    # %%
    some_code = 'here'
    # %%
    --- after ---
    # %%
    some_code = 'here'


    # %%
    """
    return re.sub(r"(?m)\n+^# %%", r"\n\n\n# %%", text)


def delete_last_cell_if_empty(text: str) -> str:
    """Delete last cell in file if it contains no code and no comment.

    --- before ---
    # %%
    some_code = 'here'

    # %%

    --- after ---
    # %%
    some_code = 'here'

    """
    # \Z matches only at end of string
    return re.sub(r"(?m)\s+^# %%\s*\Z", r"\n", text)


def single_blank_line_after_doc_string(text: str) -> str:
    """Ensure single blank line between cell delimiter and preceding module doc string.

    Added to avoid clash with ruff format. Started enforcing single blank line in 0.3.0.

    --- before ---
    '''module doc string.'''


    # %%
    some_code = 'here'

    --- after ---
    '''module doc string.'''

    # %%
    some_code = 'here'
    """
    return re.sub(r'(?m)(["\']{3})\n+(# %%)', r"\1\n\n\2", text)
