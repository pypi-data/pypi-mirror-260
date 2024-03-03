"""Common Utils
"""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

import pytz
from texttable import Texttable


def format_result(
    dataset: str,
    model: str,
    source: str = None,
    sort_kw: bool = True,
    timezone="Asia/Shanghai",
    **kwargs,
):
    if sort_kw:
        kwargs = dict(sorted(kwargs.items()))

    if source is not None:
        kwargs.update({"src": source})

    kwargs.update({
        "ds": dataset,
        "model": model,
        "time": get_str_time(timezone),
    })
    return kwargs


def get_str_time(timezone="Asia/Shanghai"):
    """Return localtime in the format of %Y-%m-%d-%H:%M:%S."""

    # Set the timezone to timezone
    pytz_timezone = pytz.timezone(timezone)

    # Get the current time in UTC
    utc_now = datetime.utcnow()

    # Convert UTC time to timezone time
    pytz_now = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz_timezone)

    return pytz_now.strftime("%Y-%m-%d-%H:%M:%S")


def format_value(value) -> Any:
    """Return number as string with comma split.

    Args:
        value (int): number.

    Returns:
        str: string of the number with comma split.
    """
    if f"{value}".isdecimal():
        return f"{value:,}"
    return value


def tab_printer(
    args: Dict,
    thead: List[str] = None,
    cols_align: List[str] = None,
    cols_valign: List[str] = None,
    cols_dtype: List[str] = None,
    sort: bool = True,
) -> None:
    """Function to print the logs in a nice tabular format.


    Args:
        args (Dict): value dict.
        thead (List[str], optional): table head. Defaults to None.
        cols_align (List[str], optional): horizontal alignment of the columns. Defaults to None.
        cols_valign (List[str], optional): vertical alignment of the columns. Defaults to None.
        cols_dtype (List[str], optional): value types of the columns. Defaults to None.
        sort (bool, optional): whether to sort the keys. Defaults to True.

    Returns:
        str: table string to print.
    """
    args = vars(args) if hasattr(args, "__dict__") else args
    keys = sorted(args.keys()) if sort else args.keys()
    table = Texttable()
    table.set_precision(5)
    params = [[] if thead is None else thead]
    params.extend(
        [
            [
                k.replace("_", " "),
                f"{args[k]}" if isinstance(args[k], bool) else format_value(args[k]),
            ] for k in keys
        ]
    )
    if cols_align is not None:
        table.set_cols_align(cols_align)
    if cols_valign is not None:
        table.set_cols_valign(cols_valign)
    if cols_dtype is not None:
        table.set_cols_dtype(cols_dtype)
    table.add_rows(params)

    print(table.draw())

    return table.draw()
