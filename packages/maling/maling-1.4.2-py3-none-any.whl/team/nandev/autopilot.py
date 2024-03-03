################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Kalo Pake Ini Kode Minimal Cantumkan Credits . Gw Boleh Mikir Juga Anjing, Meski Liat Ultroid
"""
################################################################

import asyncio
from .class_log import LOGGER
from config import *
from Mix import user
from random import randint
from os import execvp
import os
from sys import executable
import wget
import random
import math
import os
import shutil
import socket

import time
import dotenv
import heroku3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def in_heroku():
    return "heroku" in socket.getfqdn()
    
def on_heroku():
    return "heroku" in socket.getfqdn()

HAPP = None

def heroku():
    global HAPP
    if on_heroku:
        if heroku_api and heroku_app_name:
            try:
                Heroku = heroku3.from_key(heroku_api)
                HAPP = Heroku.app(heroku_app_name)
                LOGGER.info(f"Heroku App Configured")
            except BaseException:
                LOGGER.warning(
                    f"Please make sure your Heroku API Key and Your App name are configured correctly in the heroku."
                )

async def autobot():
    
    dist = "bot_token"
    if bot_token:
        return
    LOGGER.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    gw = user.me
    name = gw.first_name + " Asisstant"
    if gw.username:
        username = gw.username + "_bot"
    else:
        username = "mix_" + (str(gw.id))[5:] + "_bot"
    bf = "@BotFather"
    await user.unblock_user(bf)
    await user.send_message(bf, "/start")
    await asyncio.sleep(1)
    await user.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, "Alright, a new bot.", limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone is None or "20 bots" in isdone:
        LOGGER.error(
            "Tolong buat Bot dari @BotFather dan tambahkan tokennya di BOT_TOKEN, sebagai env var dan mulai ulang saya."
        )
        import sys

        sys.exit(1)
    await user.send_message(bf, name)
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Good."):
        await user.send_message(bf, username)
    await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "mix_" + (str(gw.id))[6:] + str(ran) + "_bot"
        await user.send_message(bf, username)
        await asyncio.sleep(1)
    async for aa in user.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
         isdone = None
    token = None
    for k in isdone.split("HTTP API:"):
      token = k.split("\n")[1]
    if token:
        LOGGER.info(
            f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
        )
        await enable_inline(user, username)
        if heroku_api and heroku_app_name:
            heroku_config = heroku3.from_key(heroku_api).app(heroku_app_name).config()
            heroku_config[dist] = token
        else:
            path = dotenv.find_dotenv()
            dotenv.set_key(".env", dist, token)
        await asyncio.sleep(8)
        execvp(executable, [executable, "-m", "Mix"])
    else:
        LOGGER.info(
            "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
        )
        import sys
        sys.exit(1)
        
async def enable_inline(user, username):
    pp = random.choice(["https://telegra.ph//file/19b336da463a05d7d8f8c.jpg", "https://telegra.ph//file/2eaf853d09c319465a8f4.jpg", "https://telegra.ph//file/7d2e8f0ae636e2f6dc381.jpg"])
    bb = wget.download(pp)
    LOGGER.info(f"Menyesuaikan Bot Asisten di @BotFather")
    bf = "BotFather"
    await user.send_message(bf, "/setuserpic")
    await asyncio.sleep(1)
    await user.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await user.send_photo(bf, bb)
    await asyncio.sleep(1)
    await user.send_message(bf, "/setabouttext")
    await asyncio.sleep(1)
    await user.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await user.send_message(bf, f"Mix-Userbot Asisten My Owner : @{user.me.first_name}")
    await asyncio.sleep(2)
    await user.send_message(bf, "/setdescription")
    await asyncio.sleep(1)
    await user.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await user.send_message(bf, f"Powerful Mix-Userbot Assistant\nMy Owner : @{user.me.first_name}\n\nPowered By ~ @KynanSupport")
    await asyncio.sleep(2)
    await user.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await user.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await user.send_message(bf, "Search")
    LOGGER.info("Customisation Done")