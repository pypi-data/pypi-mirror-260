################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from .class_log import LOGGER
from .database import udB, ndB
from Mix import user, bot
import wget
import asyncio
from pyrogram.types import ChatPrivileges


async def check_logger():
    LOGGER.info(f"Check Grup Log User...")
    if udB.get_logger(user.me.id) is not None:
        return
    LOGGER.info(f"Creating Grup Log...")
    nama = f"Mix-Userbot Logs"
    des = "Jangan Keluar Dari Grup Log Ini\n\nPowered by: @KynanSupport"
    log_pic = "https://telegra.ph//file/ee7fc86ab183a0ff90392.jpg"
    gc = await user.create_supergroup(nama, des)
    bhan = wget.download(f"{log_pic}")
    gmbr = {"video": bhan} if bhan.endswith(".mp4") else {"photo": bhan}
    kntl = gc.id
    await asyncio.sleep(1)
    await user.set_chat_photo(kntl, **gmbr)
    await asyncio.sleep(1)
    await user.promote_chat_member(
        kntl, 
        bot.me.username,
        privileges=ChatPrivileges(
            can_change_info=True,
            can_invite_users=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_chat=True,
            can_manage_video_chats=True))
    await asyncio.sleep(1)
    await user.send_message(
        kntl,
        f"<b>Group Log Berhasil Dibuat.</b>")
    udB.set_logger(user.me.id, kntl)
    ndB.set_key("TAG_LOG", kntl)
    
    LOGGER.info(f"Group Logger Enable...")
   