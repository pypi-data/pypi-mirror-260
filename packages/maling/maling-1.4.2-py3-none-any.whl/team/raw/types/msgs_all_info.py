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


class MsgsAllInfo(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~team.raw.base.MsgsAllInfo`.

    Details:
        - Layer: ``158``
        - ID: ``8CC0D131``

    Parameters:
        msg_ids (List of ``int`` ``64-bit``):
            N/A

        info (``str``):
            N/A

    """

    __slots__: List[str] = ["msg_ids", "info"]

    ID = 0x8cc0d131
    QUALNAME = "types.MsgsAllInfo"

    def __init__(self, *, msg_ids: List[int], info: str) -> None:
        self.msg_ids = msg_ids  # Vector<long>
        self.info = info  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MsgsAllInfo":
        # No flags
        
        msg_ids = TLObject.read(b, Long)
        
        info = String.read(b)
        
        return MsgsAllInfo(msg_ids=msg_ids, info=info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.msg_ids, Long))
        
        b.write(String(self.info))
        
        return b.getvalue()
