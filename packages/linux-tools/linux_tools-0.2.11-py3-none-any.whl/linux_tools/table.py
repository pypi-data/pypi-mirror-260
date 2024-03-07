# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2023-2024 Robin Jarry

import io
import typing as T


ALIGN_LEFT = "<"
ALIGN_RIGHT = ">"


class Column:
    def __init__(self, name: str, align: str = "", convert: callable = str):
        self.name = name
        self.alignment = align
        self.convert = convert
        self.width = 0

    def align(self, cell) -> str:
        fmt = f"{{:{self.alignment}{self.width}}}"
        return fmt.format(cell)


class Table:
    def __init__(self, separator: str = "  "):
        self.separator = separator
        self.columns = []
        self.rows = []

    def add_column(self, name: str, align: str = "", convert: callable = str):
        self.columns.append(Column(name, align, convert))

    def add_row(self, cells: T.Iterable[T.Any]):
        row = []
        for col, cell in zip(self.columns, cells):
            cell = col.convert(cell)
            if len(cell) > col.width:
                col.width = len(cell)
            row.append(cell)
        self.rows.append(row)

    def print(self, fileobj: io.StringIO, with_headers: bool = True):
        if with_headers:
            for col in self.columns:
                if len(col.name) > col.width:
                    col.width = len(col.name)
        if self.columns[-1].align == ALIGN_LEFT:
            self.columns[-1].width = 0
        if with_headers:
            names = [c.name for c in self.columns]
            headers = [c.align(n) for c, n in zip(self.columns, names)]
            headers[-1] = headers[-1].rstrip()
            fileobj.write(self.separator.join(headers) + "\n")
        for row in self.rows:
            cells = [c.align(r) for c, r in zip(self.columns, row)]
            cells[-1] = cells[-1].rstrip()
            fileobj.write(self.separator.join(cells) + "\n")
