from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListPlatesSort(Enums.KnownString):
    BARCODE = "barcode"
    NAME = "name"
    CREATEDAT = "createdAt"
    MODIFIEDAT = "modifiedAt"
    BARCODEASC = "barcode:asc"
    BARCODEDESC = "barcode:desc"
    NAMEASC = "name:asc"
    NAMEDESC = "name:desc"
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListPlatesSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListPlatesSort must be a string (encountered: {val})")
        newcls = Enum("ListPlatesSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListPlatesSort, getattr(newcls, "_UNKNOWN"))
