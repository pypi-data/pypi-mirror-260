#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from team.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from team.raw.core import TLObject
from team import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class WebViewResultUrl(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.WebViewResult`.

    Details:
        - Layer: ``158``
        - ID: ``C14557C``

    Parameters:
        query_id (``int`` ``64-bit``):
            N/A

        url (``str``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: team.raw.functions

        .. autosummary::
            :nosignatures:

            messages.RequestWebView
    """

    __slots__: List[str] = ["query_id", "url"]

    ID = 0xc14557c
    QUALNAME = "types.WebViewResultUrl"

    def __init__(self, *, query_id: int, url: str) -> None:
        self.query_id = query_id  # long
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebViewResultUrl":
        # No flags
        
        query_id = Long.read(b)
        
        url = String.read(b)
        
        return WebViewResultUrl(query_id=query_id, url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.query_id))
        
        b.write(String(self.url))
        
        return b.getvalue()
