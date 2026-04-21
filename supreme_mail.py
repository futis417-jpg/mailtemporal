"""
██╗███████╗██╗  ██╗███████╗██╗  ██╗    ███████╗██╗   ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗
██║██╔════╝██║  ██║██╔════╝██║ ██╔╝    ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝
██║███████╗███████║███████╗█████╔╝     ███████╗██║   ██║██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗  
██║╚════██║██╔══██║╚════██║██╔═██╗     ╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝  
██║███████║██║  ██║███████║██║  ██╗    ███████║╚██████╔╝██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗
╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
================================================================================
SISTEMA: ISHAK SUPREME-MAIL V900 - THE APEX ENTERPRISE ARCHITECTURE
CEO Y DIRECTOR SUPREMO: Ishak (@izi_1244) - Sede Central: España.
DIRECTIVA DE SEGURIDAD [VEO3-ESPAÑOL]: BLINDADA EN EL REGISTRO KERNEL.
MOTOR DE ESCANEO PROFUNDO: EXTRACCIÓN DE ENLACES, IMÁGENES Y ADJUNTOS ACTIVADO.
================================================================================
"""

import os
import sys
import json
import uuid
import time
import asyncio
import logging
import datetime
import string
import random
import threading
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from functools import wraps

def bootstrap():
    try:
        import telegram
        import aiohttp
        import flask
        from bs4 import BeautifulSoup
    except ImportError:
        print("📦 [BOOTSTRAP V900] Inyectando librerías tácticas...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])

bootstrap()

import aiohttp
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    PreCheckoutQueryHandler, MessageHandler, ContextTypes, filters
)

class SupremeConfig:
    TOKEN = "8641633728:AAFz8fMKKZivoZ_x_Ad6Zia_IDYrEEqy174"
    ADMIN_ID = 8398522835
    PORT = int(os.getenv("PORT", 8080))
    VERSION = "900.5.0-SUPREME-STABLE"
    
    VAULT_DIR = "empire_vault"
    DB_PATH = os.path.join(VAULT_DIR, "supreme_db.json")

    PLANS = {
        "FREE": {"name": "🆓 CIUDADANO", "max_emails": 1, "auto_notify": False, "attachments": False, "api": False, "custom_alias": False, "export_txt": False},
        "PRO": {"name": "💎 ÉLITE PRO", "max_emails": 5, "auto_notify": True, "attachments": True, "api": False, "custom_alias": False, "export_txt": True},
        "TITAN": {"name": "🔥 TITAN GOD", "max_emails": 20, "auto_notify": True, "attachments": True, "api": True, "custom_alias": True, "export_txt": True}
    }

    STARS_PACKAGES = {
        "VIP_PRO_30D": {"name": "💎 PRO (30D)", "stars": 150, "plan": "PRO", "days": 30},
        "VIP_TITAN_30D": {"name": "🔥 TITAN (30D)", "stars": 350, "plan": "TITAN", "days": 30},
        "VIP_TITAN_LIFE": {"name": "👁️ TITAN VITALICIO", "stars": 1500, "plan": "TITAN", "days": 36500}
    }

os.makedirs(SupremeConfig.VAULT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s | SUPREME-CORE | %(message)s')
logger = logging.getLogger("ISHAK_V900")

class QuantumDatabase:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.data = {
            "users": {}, "coupons": {}, 
            "stats": {"emails_gen": 0, "stars_rev": 0, "pushed": 0, "api_calls": 0, "exports": 0}, 
            "system": {"maint_mode": False}
        }
        self.sync_load()

    def sync_load(self):
        if os.path.exists(SupremeConfig.DB_PATH):
            try:
                with open(SupremeConfig.DB_PATH, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    for k in self.data.keys():
                        if k in saved: self.data[k] = saved[k]
            except Exception as e: logger.error(f"DB Error: {e}")

    async def save(self):
        async with self.lock:
            def write_db():
                temp = f"{SupremeConfig.DB_PATH}.tmp"
                with open(temp, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
                os.replace(temp, SupremeConfig.DB_PATH)
            await asyncio.to_thread(write_db)

    async def get_user(self, user_obj):
        uid = str(user_obj.id)
        async with self.lock:
            if uid not in self.data["users"]:
                self.data["users"][uid] = {
                    "id": user_obj.id, "name": user_obj.first_name,
                    "plan": "TITAN" if user_obj.id == SupremeConfig.ADMIN_ID else "FREE",
                    "plan_expiry": None, "emails": [], "referrals": 0, "read_msg_ids": [],
                    "api_key": f"sk_v9_{uuid.uuid4().hex}" if user_obj.id == SupremeConfig.ADMIN_ID else None
                }
                await self._save_nolock()
            
            u = self.data["users"][uid]
            if u["plan_expiry"] and datetime.datetime.now() > parse(u["plan_expiry"]):
                u["plan"] = "FREE"
                u["plan_expiry"] = None
                await self._save_nolock()
            return u

    async def _save_nolock(self):
        def write_db():
            temp = f"{SupremeConfig.DB_PATH}.tmp"
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            os.replace(temp, SupremeConfig.DB_PATH)
        await asyncio.to_thread(write_db)

db = QuantumDatabase()

class MailEngine:
    BASE_URL = "https://www.1secmail.com/api/v1/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    @staticmethod
    def parse_email_html(html_content):
        """DEEP-SCAN ENGINE: Extrae enlaces e imágenes del HTML"""
        if not html_content: return "Sin contenido HTML.", [], []
        soup = BeautifulSoup(html_content, "html.parser")

        links = []
        for a in soup.find_all('a', href=True):
            text = a.text.strip() or "Enlace Directo"
            if len(links) < 8: # Limitar para no saturar Telegram
                links.append(f"🔗 [{text}]({a['href']})")

        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if src.startswith('http') and len(images) < 5:
                images.append(src)

        text = soup.get_text(separator="\n", strip=True)
        return text, links, images

    @classmethod
    async def get_domains(cls):
        fallbacks = [{"domain": "1secmail.com"}, {"domain": "1secmail.org"}, {"domain": "1secmail.net"}, {"domain": "kzccv.com"}, {"domain": "vjuum.com"}]
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}?action=getDomainList", headers=cls.HEADERS) as r:
                    if r.status == 200:
                        data = await r.json()
                        if data: return [{"domain": d} for d in data]
        except Exception: pass
        return fallbacks

    @classmethod
    async def create_account(cls, domain, custom_username=None):
        username = custom_username if custom_username else ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + "X!"
        
        return {
            "address": address, "password": password, 
            "token": f"{username}:{domain}", "domain": domain, 
            "id": str(uuid.uuid4())[:8], "login": username
        }

    @classmethod
    async def get_messages(cls, token):
        try:
            login, domain = token.split(":")
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}?action=getMessages&login={login}&domain={domain}", headers=cls.HEADERS) as r:
                    if r.status == 200:
                        msgs = await r.json()
                        return [{"id": str(m["id"]), "from": {"address": m["from"]}, "subject": m["subject"], "createdAt": m["date"]} for m in msgs]
        except Exception: pass
        return []

    @classmethod
    async def read_message(cls, token, msg_id):
        try:
            login, domain = token.split(":")
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}?action=readMessage&login={login}&domain={domain}&id={msg_id}", headers=cls.HEADERS) as r:
                    if r.status == 200:
                        m = await r.json()
                        atts = [{"filename": a["filename"]} for a in m.get("attachments", [])]
                        return {
                            "id": str(m["id"]), "from": {"address": m["from"]},
                            "subject": m["subject"], "createdAt": m["date"],
                            "text": m.get("textBody", ""), "html": m.get("htmlBody", ""),
                            "hasAttachments": len(atts) > 0, "attachments": atts
                        }
        except Exception: pass
        return None

    @classmethod
    async def download_attachment(cls, token, msg_id, filename):
        try:
            login, domain = token.split(":")
            async with aiohttp.ClientSession() as s:
                url = f"{cls.BASE_URL}?action=download&login={login}&domain={domain}&id={msg_id}&file={filename}"
                async with s.get(url, headers=cls.HEADERS) as r:
                    if r.status == 200:
                        path = os.path.join(SupremeConfig.VAULT_DIR, f"att_{uuid.uuid4().hex[:8]}_{filename}")
                        with open(path, 'wb') as f: f.write(await r.read())
                        return path
        except Exception: pass
        return None

# =================================================================
# [4] CRON & PUSH ENGINE
# =================================================================
async def cron_job(context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    try:
        now = datetime.datetime.now()
        for uid, u in list(db.data["users"].items()):
            if u.get("emails"):
                for acc in list(u["emails"]):
                    if acc.get("timer") and now > parse(acc["timer"]):
                        u["emails"].remove(acc)
                        try: await bot.send_message(chat_id=uid, text=f"🧨 **AUTO-DESTRUCCIÓN EJECUTADA**\nLa bóveda `{acc['address']}` ha sido purgada.", parse_mode="Markdown")
                        except Exception: pass

            if SupremeConfig.PLANS[u["plan"]]["auto_notify"] and u.get("emails"):
                for acc in u["emails"]:
                    msgs = await MailEngine.get_messages(acc["token"])
                    if msgs:
                        for m in msgs:
                            if m["id"] not in u.get("read_msg_ids", []):
                                db.data["users"][uid].setdefault("read_msg_ids", []).append(m["id"])
                                db.data["stats"]["pushed"] += 1
                                
                                full_m = await MailEngine.read_message(acc["token"], m["id"])
                                if not full_m: continue
                                text = full_m.get("text", "") or MailEngine.clean_html(full_m.get("html", ""))[0]
                                
                                alert = (f"🔔 **NUEVO PAQUETE INTERCEPTADO**\n"
                                         f"─────────────────\n"
                                         f"📥 **Bóveda:** `{acc['address']}`\n"
                                         f"👤 **Origen:** `{m['from']['address']}`\n"
                                         f"📝 **Asunto:** `{m['subject'].replace('`', '')}`\n"
                                         f"─────────────────\n"
                                         f"
