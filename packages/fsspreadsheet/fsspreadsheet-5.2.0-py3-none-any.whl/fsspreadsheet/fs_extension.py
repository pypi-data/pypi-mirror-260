from __future__ import annotations
from typing import Any
from .FsSpreadsheet.fs_workbook import FsWorkbook
from .xlsx import Xlsx

def FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5(path: str) -> FsWorkbook:
    return Xlsx.from_xlsx_file(path)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxStream_Static_4D976C1A(stream: Any) -> FsWorkbook:
    return Xlsx.from_xlsx_stream(stream)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromBytes_Static_Z3F6BC7B1(bytes: bytearray) -> FsWorkbook:
    return Xlsx.from_bytes(bytes)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toFile_Static(path: str, wb: FsWorkbook) -> None:
    Xlsx.to_file(path, wb)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toBytes_Static_32154C9D(wb: FsWorkbook) -> bytearray:
    return Xlsx.to_bytes(wb)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToFile_Z721C83C5(this: FsWorkbook, path: str) -> None:
    FsSpreadsheet_FsWorkbook__FsWorkbook_toFile_Static(path, this)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToBytes(this: FsWorkbook) -> bytearray:
    return FsSpreadsheet_FsWorkbook__FsWorkbook_toBytes_Static_32154C9D(this)


__all__ = ["FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxStream_Static_4D976C1A", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromBytes_Static_Z3F6BC7B1", "FsSpreadsheet_FsWorkbook__FsWorkbook_toFile_Static", "FsSpreadsheet_FsWorkbook__FsWorkbook_toBytes_Static_32154C9D", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToFile_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToBytes"]

