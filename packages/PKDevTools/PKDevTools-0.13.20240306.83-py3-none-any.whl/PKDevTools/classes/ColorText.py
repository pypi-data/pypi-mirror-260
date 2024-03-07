"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
import tabulate as tb
from tabulate import tabulate, Line,DataRow

# Decoration Class
class colorText:
    HEAD = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDR = "\033[4m"
    WHITE = "\033[97m"

    No_Pad_GridFormat = "minpadding"

    def miniTabulator():
        tb._table_formats[colorText.No_Pad_GridFormat] = tb.TableFormat(
                lineabove=Line("+", "-", "+", "+"),
                linebelowheader=Line("+", "=", "+", "+"),
                linebetweenrows=Line("+", "-", "+", "+"),
                linebelow=Line("+", "-", "+", "+"),
                headerrow=DataRow("|", "|", "|"),
                datarow=DataRow("|", "|", "|"),
                padding=0,
                with_header_hide=None,
            )
        tb.multiline_formats[colorText.No_Pad_GridFormat] = colorText.No_Pad_GridFormat
        tb.tabulate_formats = list(sorted(tb._table_formats.keys()))
        return tb