################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio

import os
import re

import wget
from io import BytesIO
from os import execvp
from sys import executable
from pytgcalls import PyTgCalls
from pyrogram import *
from pyrogram.enums import *
from pyrogram.handlers import *
from pyrogram.types import *
from pyrogram.errors import *
from config import *
from .database import udB
from .class_log import LOGGER

class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0

LOG_CHATS_ = LOG_CHATS()
    
class Userbot(Client):
    __module__ = "pyrogram.client"
    _prefix = {}
    _translate = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_id = api_id
        self.api_hash = api_hash
        self.device_model = "Mix-Userbot"
        self.ipv6 = False
        self.session_string = None
        self.no_updates = False
        self.call_py = PyTgCalls(self)

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])
        
    def user_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, c, m):
            if m.text:
                text = m.text.strip().encode("utf-8").decode("utf-8")
                username = c.me.username or ""
                prefixes = await self.get_prefix(c.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix) :]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        m.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)
        
    async def get_user_dialog(self, query):
        chats = []
        chat_types = {
            "group": [ChatType.GROUP, ChatType.SUPERGROUP],
            "users": [ChatType.PRIVATE],
            "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
            "ch": [ChatType.CHANNEL],
            "allread": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL, ChatType.PRIVATE]
        }
 
        async for dialog in self.get_dialogs():
            if dialog.chat.type in chat_types[query]:
                chats.append(dialog.chat.id)
        return chats
        
    def get_m(self, m):
        msg = (
            m.reply_to_message
            if m.reply_to_message
            else ""
            if len(m.command) < 2
            else " ".join(m.command[1:])
        )
        return msg
        
    def get_text(self, m):
        if m.reply_to_message:
            if len(m.command) < 2:
                text = m.reply_to_message.text or m.reply_to_message.caption
            else:
                text = (
                    (m.reply_to_message.text or m.reply_to_message.caption)
                    + "\n\n"
                    + m.text.split(None, 1)[1]
                )
        else:
            if len(m.command) < 2:
                text = ""
            else:
                text = m.text.split(None, 1)[1]
        return text
        
    async def bash(self, cmd):
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        err = stderr.decode().strip()
        out = stdout.decode().strip()
        return out, err
        
    async def run_cmd(self, cmd):
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )
        
    async def aexec(self, code, c, m):
        exec(
            "async def __aexec(c, m): "
            + "".join(f"\n {l_}" for l_ in code.split("\n"))
        )
        return await locals()["__aexec"](c, m)


    async def shell_exec(self, code, treat=True):
        process = await asyncio.create_subprocess_shell(
            code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )

        stdout = (await process.communicate())[0]
        if treat:
            stdout = stdout.decode().strip()
        return stdout, process

        
    async def dl_pic(self, a):
        path = await self.download_media(a)
        with open(path, "rb") as f:
            content = f.read()
        os.remove(path)
        getpp = BytesIO(content)
        return getpp
        
    def get_arg(self, m):
        if m.reply_to_message and len(m.command) < 2:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
            return msg
        elif len(m.command) > 1:
            return " ".join(m.command[1:])
        else:
            return ""
        
    async def extract_userid(self, m, t):
        def is_int(t):
            try:
                int(t)
            except ValueError:
                return False
            return True

        text = t.strip()

        if is_int(text):
            return int(text)

        entities = m.entities
        app = m._client
        entity = entities[1 if m.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            return (await self.get_users(text)).id
        if entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
        return None
        
    async def extract_user_and_reason(self, m, s=False):
        args = m.text.strip().split()
        text = m.text
        rg = None
        reason = None
        if m.reply_to_message:
            reply = m.reply_to_message
            if not reply.from_user:
                if (
                    reply.sender_chat
                    and reply.sender_chat != m.chat.id
                    and s
                ):
                    id_ = reply.sender_chat.id
                else:
                    return None, None
            else:
                id_ = reply.from_user.id

            if len(args) < 2:
                reason = None
            else:
                reason = text.split(None, 1)[1]
            return id_, reason

        if len(args) == 2:
            rg = text.split(None, 1)[1]
            return await self.extract_userid(m, rg), None

        if len(args) > 2:
            rg, reason = text.split(None, 2)[1:]
            return await self.extract_userid(m, rg), reason

        return rg, reason

    async def extract_user(self, m):
        return (await self.extract_user_and_reason(m))[0]
        
    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator
    
    async def forward_group(self, m):
        ll = await self.get_grup()
        db =  udB.get_logger(self.me.id)
        if not db:
            return
        user = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"
        lenk = m.link
        teks = f"""
📨 <b>TAGS MESSAGE</b>
• <b>Logs:</b> <code>{self.me.first_name}</code>
• <b>Group:</b> <code>{m.chat.title}</code>
• <b>Dari :</b> <code>{user}</code>
• <b>Pesan:</b> <code>{m.text}</code>

• <b>Tautan Grup:</b> [Disini]({lenk})
"""
        try:
            await self.send_message(
              db,
              teks,
              disable_web_page_preview=True,
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await self.send_message(
                db,
                teks,
                disable_web_page_preview=True,
            )
            
    async def forward_private(self, m):
        db =  udB.get_logger(self.me.id)
        if not db:
          return
        if m.chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != m.chat.id:
                LOG_CHATS_.RECENT_USER = m.chat.id
            try:
                async for x in self.search_messages(m.chat.id, limit=1):
                    await x.forward(db)
                LOG_CHATS_.COUNT += 1
            except BaseException:
                pass
        
    async def restart(self):
        execvp(executable, [executable, "-m", "Mix"])
        
    async def restart2(self):
        await self.bash("run.sh")
        
    def pytgc_dec(self):
        def decorator(func):
            try:
                if func.__name__ != "stream_end":
                    self.call_py.on_kicked()(func)
                    self.call_py.on_closed_voice_chat()(func)
                    self.call_py.on_left()(func)
                else:
                    self.call_py.on_stream_end()(func)
            except:
                pass
            return func

        return decorator

    async def start(self):
        try:
            await super().start()
            await self.call_py.start()
            handler = udB.get_pref(self.me.id)
            if handler:
                self._prefix[self.me.id] = handler
            else:
                self._prefix[self.me.id] = ["."]
            self._translate[self.me.id] = {"negara": "id"}
            LOGGER.info(
                f"Starting Userbot {self.me.id}|{self.me.mention}")
        except SessionExpired:
            LOGGER.info("Session Expired . Create New Session")
            sys.exit(1)
        except ApiIdInvalid:
            LOGGER.info("Api ID Not Valid.")
            sys.exit(1)
        
 
class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(name="bot", **kwargs)
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        LOGGER.info(f"Starting Assistant {self.me.id}|{self.me.mention}")