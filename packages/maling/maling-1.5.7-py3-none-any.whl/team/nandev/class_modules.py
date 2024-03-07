################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from pyrogram import __version__ as pyrover
from importlib import import_module
from sys import version as pyver
from math import ceil
from pytgcalls.__version__ import __version__ as pytgver
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors import ChannelInvalid
from Mix import user, bot
from modular import import_modular


from .class_log import LOGGER
from .database import udB

CMD_HELP = {}

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({})".format(
                        prefix, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__modles__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__modles__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    line = 3
    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )
        
 

    max_num_pages = ceil(len(pairs) / line)
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⪻",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "ⓧ",
                    callback_data="cls_hlp",
                ),
                EqInlineKeyboardButton(
                    "⪼",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs
    
    
    
async def refresh_modules():
    LOGGER.info(f"Importing All Modules...")
    modxx = import_modular()
    emut = await user.get_prefix(user.me.id)
    xx = " ".join(emut)
    for modx in modxx:
        imported_module = import_module(f"modular.{modx}")
        if hasattr(imported_module, "__modles__") and imported_module.__modles__:
            imported_module.__modles__ = imported_module.__modles__
            if hasattr(imported_module, "__help__") and imported_module.__help__:
                CMD_HELP[
                    imported_module.__modles__.replace(" ", "_").lower()
                ] = imported_module
    try:
        await bot.send_message(
            udB.get_logger(user.me.id),
            f"""
<b>Userbot Successfully Deploy !!</b>

<b>Modules : {len(CMD_HELP)}</b>
<b>Python : {pyver.split()[0]}</b>
<b>Pyrogram : {pyrover}</b>
<b>Pytgcalls : {pytgver}</b>
<b>Prefixes : {xx}</b>
""")
    except ChannelInvalid:
        udB.rem_logger(user.me.id)
        await user.restart()