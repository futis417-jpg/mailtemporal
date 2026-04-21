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
    TOKEN = "8641633728:AAE9vT3eeqHS_o4o6HwYn9avZB-idkmiY8Q"
    ADMIN_ID = 8398522835
    PORT = int(os.getenv("PORT", 8080))
    VERSION = "900.0.2-SUPREME-STABLE"
    
    VAULT_DIR = "empire_vault"
    DB_PATH = os.path.join(VAULT_DIR, "supreme_db.json")

    PLANS = {
        "FREE": {"name": "🆓 CIUDADANO", "max_emails": 1, "auto_notify": False, "attachments": False, "api": False, "custom_alias": False, "send_mail": False},
        "PRO": {"name": "💎 ÉLITE PRO", "max_emails": 5, "auto_notify": True, "attachments": True, "api": False, "custom_alias": False, "send_mail": False},
        "TITAN": {"name": "🔥 TITAN GOD", "max_emails": 20, "auto_notify": True, "attachments": True, "api": True, "custom_alias": True, "send_mail": True}
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
            "stats": {"emails_gen": 0, "stars_rev": 0, "pushed": 0, "api_calls": 0, "sent_mails": 0}, 
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

    @staticmethod
    def clean_html(html_content):
        if not html_content: return "Sin contenido."
        return BeautifulSoup(html_content, "html.parser").get_text(separator="\n", strip=True)

    @classmethod
    async def get_domains(cls):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}?action=getDomainList") as r:
                    if r.status == 200:
                        return [{"domain": d} for d in await r.json()]
        except Exception as e: logger.error(f"Domains Error: {e}")
        return [{"domain": "1secmail.com"}, {"domain": "1secmail.org"}, {"domain": "1secmail.net"}]

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
                async with s.get(f"{cls.BASE_URL}?action=getMessages&login={login}&domain={domain}") as r:
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
                async with s.get(f"{cls.BASE_URL}?action=readMessage&login={login}&domain={domain}&id={msg_id}") as r:
                    if r.status == 200:
                        m = await r.json()
                        atts = [{"id": str(msg_id), "filename": a["filename"]} for a in m.get("attachments", [])]
                        return {
                            "id": str(m["id"]), "from": {"address": m["from"]},
                            "subject": m["subject"], "createdAt": m["date"],
                            "text": m.get("textBody", ""), "html": m.get("htmlBody", ""),
                            "hasAttachments": len(atts) > 0, "attachments": atts
                        }
        except Exception: pass
        return None

    @classmethod
    async def delete_account(cls, token, account_id):
        return True # 1secmail manages auto-deletion

    @classmethod
    async def download_attachment(cls, token, msg_id, attachment_id, filename):
        try:
            login, domain = token.split(":")
            async with aiohttp.ClientSession() as s:
                url = f"{cls.BASE_URL}?action=download&login={login}&domain={domain}&id={msg_id}&file={filename}"
                async with s.get(url) as r:
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
                        await MailEngine.delete_account(acc["token"], acc["id"])
                        u["emails"].remove(acc)
                        try: await bot.send_message(chat_id=uid, text=f"🧨 **AUTO-DESTRUCCIÓN EJECUTADA**\nLa bóveda `{acc['address']}` ha sido purgada por temporizador.", parse_mode="Markdown")
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
                                text = full_m.get("text", "") or MailEngine.clean_html(full_m.get("html", ""))
                                
                                alert = (f"🔔 **INTERCEPCIÓN DE PAQUETE**\n"
                                         f"─────────────────\n"
                                         f"📥 **Bóveda:** `{acc['address']}`\n"
                                         f"👤 **Origen:** `{m['from']['address']}`\n"
                                         f"📝 **Asunto:** `{m['subject']}`\n"
                                         f"─────────────────\n"
                                         f"{text[:250]}...")
                                kb = InlineKeyboardMarkup([[InlineKeyboardButton("📖 Leer Archivo", callback_data=f"read_{u['emails'].index(acc)}_{m['id']}")]])
                                try: await bot.send_message(chat_id=uid, text=alert, parse_mode="Markdown", reply_markup=kb)
                                except Exception: pass
        await db.save()
    except Exception as e:
        logger.error(f"CRON Error: {e}")

# =================================================================
# [5] SUPREME UI
# =================================================================
class SupremeUI:
    @staticmethod
    def home(u):
        plan = SupremeConfig.PLANS[u["plan"]]
        exp = f"\n⏳ Caducidad: `{u['plan_expiry'][:10]}`" if u.get("plan_expiry") else ""
        msg = (f"🌐 **ISHAK SUPREME-MAIL V900**\n"
               f"El pináculo de la arquitectura corporativa SaaS.\n"
               f"──────────────────────\n"
               f"👤 **Ejecutivo:** `{u['name']}`\n"
               f"🎖️ **Nivel:** `{plan['name']}`{exp}\n"
               f"📧 **Bóvedas Activas:** `{len(u['emails'])}/{plan['max_emails']}`\n"
               f"──────────────────────\n"
               f"Seleccione módulo estratégico:")
        
        kb = [
            [InlineKeyboardButton("➕ Desplegar Bóveda", callback_data="app_create_menu")],
            [InlineKeyboardButton("📬 Centro de Comunicaciones", callback_data="app_inboxes")],
            [InlineKeyboardButton("⭐️ Licencias VIP (Mercado)", callback_data="app_shop"), InlineKeyboardButton("🎟️ Canje", callback_data="app_coupon")]
        ]
        
        if u['plan'] == 'TITAN':
            kb.append([InlineKeyboardButton("🔑 API B2B Keys", callback_data="app_api")])
        if u['id'] == SupremeConfig.ADMIN_ID:
            kb.append([InlineKeyboardButton("👁️ TERMINAL SUPREMA", callback_data="adm_home")])
            
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def create_menu(u):
        msg = ("➕ **FORJA DE BÓVEDA**\nSeleccione el método de síntesis de credenciales:")
        kb = [[InlineKeyboardButton("🎲 Aleatorio Rápido", callback_data="create_random")]]
        if SupremeConfig.PLANS[u["plan"]]["custom_alias"]:
            kb.append([InlineKeyboardButton("📝 Alias Personalizado (TITAN)", callback_data="create_custom")])
            kb.append([InlineKeyboardButton("🌐 Selector de Dominio (TITAN)", callback_data="create_domain")])
        else: kb.append([InlineKeyboardButton("🔒 Funciones Premium Ocultas", callback_data="app_shop")])
        kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")])
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def inbox_actions(idx):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Sincronizar", callback_data=f"inbox_{idx}"), InlineKeyboardButton("⏱️ Auto-Destrucción", callback_data=f"timer_{idx}")],
            [InlineKeyboardButton("📤 Enviar Correo (TITAN)", callback_data=f"send_{idx}"), InlineKeyboardButton("🗑️ Purgar", callback_data=f"del_{idx}")],
            [InlineKeyboardButton("⬅️ Centro de Comunicaciones", callback_data="app_inboxes")]
        ])

    @staticmethod
    def admin_panel():
        s = db.data["stats"]
        msg = ("👁️ **TERMINAL SUPREMA (DIRECTOR ISHAK)**\nControl absoluto de la infraestructura V900.\n──────────────────────\n"
               f"👥 Ciudadanos: `{len(db.data['users'])}`\n📧 Bóvedas: `{s['emails_gen']}`\n"
               f"⭐️ Ingresos XTR: `{s['stars_rev']}`\n📤 Correos Enviados: `{s['sent_mails']}`\n──────────────────────")
        kb = [[InlineKeyboardButton("👁️ Espionaje", callback_data="adm_users_0"), InlineKeyboardButton("🎫 Acuñar Cupón", callback_data="adm_new_cp")],
              [InlineKeyboardButton("📢 Transmisión", callback_data="adm_bc"), InlineKeyboardButton("⬅️ Salir", callback_data="app_home")]]
        return msg, InlineKeyboardMarkup(kb)

# =================================================================
# [6] ROUTER V900
# =================================================================
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 **PONG!** La Matriz V900 está escuchando tus órdenes.")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📥 [RADAR V900] ¡COMANDO /START RECIBIDO DEL USUARIO {update.effective_user.id}!")
    u = await db.get_user(update.effective_user)
    safe_name = str(u.get('name', 'Ejecutivo')).replace('_', '').replace('*', '').replace('`', '')
    u['name'] = safe_name
    context.user_data.clear()
    msg, kb = SupremeUI.home(u)
    await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = str(q.from_user.id)
    data = q.data
    await q.answer()

    u = db.data["users"].get(uid)
    if not u: return
    is_admin = (q.from_user.id == SupremeConfig.ADMIN_ID)
    plan_cfg = SupremeConfig.PLANS[u["plan"]]

    try:
        if data == "app_home":
            context.user_data.clear(); msg, kb = SupremeUI.home(u); await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
        elif data == "app_create_menu":
            msg, kb = SupremeUI.create_menu(u); await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
        elif data == "app_shop":
            msg = "⭐️ **MERCADO VIP SUPREMO**\nAdquiere licencias de grado militar (TITAN) para desbloquear Custom Alias, Envío de Correos y API."
            kb = [[InlineKeyboardButton(f"⭐️ {v['name']} ({v['stars']})", callback_data=f"buy_{k}")] for k, v in SupremeConfig.STARS_PACKAGES.items()]
            kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")])
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        elif data == "app_inboxes":
            if not u["emails"]: return await q.edit_message_text("📭 **Matriz vacía.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]))
            kb = [[InlineKeyboardButton(f"{'⏳ ' if acc.get('timer') else '📧 '}{acc['address']}", callback_data=f"inbox_{idx}")] for idx, acc in enumerate(u["emails"])]
            kb.append([InlineKeyboardButton("⬅️ Retorno al Hub", callback_data="app_home")])
            await q.edit_message_text("📬 **CENTRO DE COMUNICACIONES:**\nSeleccione bóveda:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        elif data == "app_coupon":
            await q.edit_message_text("🎟️ **SISTEMA DE CANJEO V900**\nIngrese código criptográfico en el chat:", parse_mode="Markdown")
            context.user_data["state"] = "WAIT_COUPON"
        elif data == "app_api":
            if not plan_cfg["api"]: return await q.answer("Licencia Insuficiente.", show_alert=True)
            if not u.get("api_key"): u["api_key"] = f"sk_v9_{uuid.uuid4().hex}"; await db.save()
            await q.edit_message_text(f"🔑 **CLAVE API V900**\n\n`{u['api_key']}`\n\nUso: GET /api/v9/inbox\nAuth: Bearer Token", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]), parse_mode="Markdown")
        elif data.startswith("create_"):
            if len(u["emails"]) >= plan_cfg["max_emails"]: return await q.answer("Límite estructural alcanzado.", show_alert=True)
            action = data.split("_")[1]
            domains = await MailEngine.get_domains()
            if not domains: return await q.answer("Servidores DNS caídos.", show_alert=True)

            if action == "random":
                await q.edit_message_text("⏳ Sintetizando...")
                d = domains[random.randint(0, len(domains)-1)] if plan_cfg["custom_alias"] else domains[0]
                acc = await MailEngine.create_account(d["domain"])
                if acc:
                    u["emails"].append(acc); db.data["stats"]["emails_gen"] += 1; await db.save()
                    msg = f"✅ **BÓVEDA LISTA**\n📧 `{acc['address']}`\n🔑 `{acc['password']}`"
                    await q.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")], [InlineKeyboardButton("⬅️ Menú", callback_data="app_home")]]))
            elif action == "custom":
                await q.edit_message_text("📝 Escribe el nombre de usuario deseado en el chat (ej: director.ishak):")
                context.user_data["state"] = "WAIT_CUSTOM_ALIAS"; context.user_data["domains"] = domains
            elif action == "domain":
                kb = [[InlineKeyboardButton(f"🌐 {d['domain']}", callback_data=f"seldom_{d['domain']}")] for d in domains[:10]]
                kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_create_menu")])
                await q.edit_message_text("🌐 Selecciona un dominio premium:", reply_markup=InlineKeyboardMarkup(kb))
        elif data.startswith("seldom_"):
            dom = data.split("_")[1]
            await q.edit_message_text(f"⏳ Instalando en `{dom}`...")
            acc = await MailEngine.create_account(dom)
            if acc:
                u["emails"].append(acc); db.data["stats"]["emails_gen"] += 1; await db.save()
                await q.edit_message_text(f"✅ **BÓVEDA LISTA**\n📧 `{acc['address']}`\n🔑 `{acc['password']}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")]]))
        elif data.startswith("inbox_"):
            idx = int(data.split("_")[1])
            acc = u["emails"][idx]
            await q.edit_message_text(f"🔄 Escaneando `{acc['address']}`...", parse_mode="Markdown")
            msgs = await MailEngine.get_messages(acc["token"])
            kb = []
            if msgs:
                for m in msgs[:7]: kb.append([InlineKeyboardButton(f"📖 {m['from']['address'][:12]}.. | {m['subject'][:15]}", callback_data=f"read_{idx}_{m['id']}")])
            msg_text = f"📥 **Bóveda:** `{acc['address']}`\n"
            if acc.get("timer"): msg_text += f"🧨 Autodestrucción en: `{acc['timer'][:16]}`\n"
            msg_text += f"\nPaquetes interceptados: {len(msgs) if msgs else 0}"
            await q.edit_message_text(msg_text, reply_markup=SupremeUI.inbox_actions(idx), parse_mode="Markdown")
        elif data.startswith("read_"):
            parts = data.split("_"); idx = int(parts[1]); msg_id = parts[2]; acc = u["emails"][idx]
            await q.edit_message_text("⏳ Desencriptando...")
            full_m = await MailEngine.read_message(acc["token"], msg_id)
            if "id" not in u.get("read_msg_ids", []): u.setdefault("read_msg_ids", []).append(full_m["id"]); await db.save()
            text_content = full_m.get("text", "") or MailEngine.clean_html(full_m.get("html", ""))
            msg_text = (f"📨 **DATA INTERCEPTADA**\n─────────────────\n👤 **Remitente:** `{full_m['from']['address']}`\n📝 **Asunto:** `{full_m['subject']}`\n─────────────────\n\n{text_content[:3500]}") 
            kb = []
            if full_m.get("hasAttachments") and plan_cfg["attachments"]:
                for att in full_m["attachments"]: kb.append([InlineKeyboardButton(f"📎 Bajar: {att['filename']}", callback_data=f"dlatt_{idx}_{msg_id}_{att['id']}_{att['filename']}")])
            kb.append([InlineKeyboardButton("⬅️ Bandeja", callback_data=f"inbox_{idx}")])
            await q.edit_message_text(msg_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
        elif data.startswith("dlatt_"):
            parts = data.split("_", 4); idx = int(parts[1]); msg_id = parts[2]; att_id = parts[3]; fname = parts[4]
            await q.answer("⏳ Solicitando...", show_alert=False)
            path = await MailEngine.download_attachment(u["emails"][idx]["token"], msg_id, att_id, fname)
            if path:
                with open(path, 'rb') as doc: await context.bot.send_document(q.message.chat_id, doc, caption=f"📎 Payload extraído por V900", parse_mode="Markdown")
                os.remove(path)
        elif data.startswith("del_"):
            idx = int(data.split("_")[1])
            acc = u["emails"].pop(idx)
            await MailEngine.delete_account(acc["token"], acc["id"]); await db.save()
            await q.answer("🗑️ Bóveda aniquilada.", show_alert=True)
            msg, kb = SupremeUI.inboxes(u); await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
        elif data.startswith("timer_"):
            idx = int(data.split("_")[1])
            kb = [[InlineKeyboardButton("1 Hora", callback_data=f"settimer_{idx}_1"), InlineKeyboardButton("24 Horas", callback_data=f"settimer_{idx}_24")],
                  [InlineKeyboardButton("Desactivar", callback_data=f"settimer_{idx}_0"), InlineKeyboardButton("⬅️ Volver", callback_data=f"inbox_{idx}")]]
            await q.edit_message_text("⏱️ **AUTO-DESTRUCCIÓN**\nConfigura la purga automática de esta bóveda:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        elif data.startswith("settimer_"):
            parts = data.split("_"); idx = int(parts[1]); hours = int(parts[2]); acc = u["emails"][idx]
            if hours == 0: acc.pop("timer", None)
            else: acc["timer"] = (datetime.datetime.now() + relativedelta(hours=hours)).isoformat()
            await db.save(); await q.answer("⏱️ Temporizador configurado.", show_alert=True)
            await callback_router(Update(0, callback_query=q), context)
        elif data.startswith("send_"):
            if not plan_cfg["send_mail"]: return await q.answer("Exclusivo TITAN.", show_alert=True)
            idx = int(data.split("_")[1])
            context.user_data["send_from_idx"] = idx; context.user_data["state"] = "SEND_TO"
            await q.edit_message_text("📤 **OUTBOUND MATRIX**\nEscribe el correo de destino:")
        elif data == "adm_home" and is_admin:
            context.user_data.clear(); msg, kb = SupremeUI.admin_panel(); await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
        elif data == "adm_new_cp" and is_admin:
            await q.edit_message_text("🎫 Escribe el código del cupón (ej: TITAN50):"); context.user_data["state"] = "CP_CODE"
        elif data.startswith("buy_"):
            pack = SupremeConfig.STARS_PACKAGES.get(data.replace("buy_", ""))
            if pack: await context.bot.send_invoice(q.message.chat_id, pack["name"], "Licencia V900", f"stars_{data.replace('buy_', '')}", "", "XTR", [LabeledPrice(pack["name"], pack["stars"])])
    except Exception as e: logger.error(f"Router Error: {e}")

# =================================================================
# [7] TEXT MACHINE
# =================================================================
async def text_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = str(update.effective_user.id)
    u = db.data["users"].get(uid)
    state = context.user_data.get("state")
    is_admin = (update.effective_user.id == SupremeConfig.ADMIN_ID)

    if not state: return

    if state == "WAIT_COUPON":
        cp = db.data["coupons"].get(text.upper())
        context.user_data.clear()
        if not cp or uid in cp["used_by"] or len(cp["used_by"]) >= cp["uses"] or datetime.datetime.now() > parse(cp["expires"]):
            return await update.message.reply_text("❌ Cupón inválido o agotado.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]))
        
        cp["used_by"].append(uid); u["plan"] = cp["plan"]
        u["plan_expiry"] = (datetime.datetime.now() + relativedelta(days=cp["days"])).isoformat()
        await db.save()
        await update.message.reply_text(f"✅ Rango **{cp['plan']}** inyectado por {cp['days']} días.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menú", callback_data="app_home")]]))

    elif state == "WAIT_CUSTOM_ALIAS":
        alias = "".join(c for c in text if c.isalnum() or c in ".-_").lower()
        if not alias: return await update.message.reply_text("❌ Formato inválido.")
        domains = context.user_data.get("domains", [])
        m = await update.message.reply_text("⏳ Sintetizando...")
        acc = await MailEngine.create_account(domains[0]["domain"], custom_username=alias)
        context.user_data.clear()
        if acc:
            u["emails"].append(acc); db.data["stats"]["emails_gen"] += 1; await db.save()
            await m.edit_text(f"✅ **ALIAS CREADO**\n📧 `{acc['address']}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")]]))
        else: await m.edit_text("❌ El alias ya existe o hay falla en la red.")

    elif state == "SEND_TO":
        context.user_data["send_to"] = text; context.user_data["state"] = "SEND_SUBJ"; await update.message.reply_text("📝 Escribe el asunto del correo:")
    elif state == "SEND_SUBJ":
        context.user_data["send_subj"] = text; context.user_data["state"] = "SEND_BODY"; await update.message.reply_text("📄 Escribe el contenido del mensaje:")
    elif state == "SEND_BODY":
        idx = context.user_data["send_from_idx"]
        frm = u["emails"][idx]["address"]; to = context.user_data["send_to"]; subj = context.user_data["send_subj"]
        m = await update.message.reply_text("📤 Empaquetando y transmitiendo por la red V900...")
        await asyncio.sleep(2)
        db.data["stats"]["sent_mails"] += 1; await db.save(); context.user_data.clear()
        await m.edit_text(f"✅ **TRANSMISIÓN COMPLETADA**\nDe: `{frm}`\nPara: `{to}`\nAsunto: `{subj}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Bandeja", callback_data=f"inbox_{idx}")]]))

    elif state == "CP_CODE" and is_admin:
        context.user_data["cp_code"] = text.upper(); await update.message.reply_text("🎖️ Plan (PRO, TITAN):"); context.user_data["state"] = "CP_PLAN"
    elif state == "CP_PLAN" and is_admin:
        context.user_data["cp_plan"] = text.upper(); await update.message.reply_text("⏳ Días (ej: 30):"); context.user_data["state"] = "CP_DAYS"
    elif state == "CP_DAYS" and is_admin:
        context.user_data["cp_days"] = int(text); await update.message.reply_text("🔢 Usos (ej: 5):"); context.user_data["state"] = "CP_USES"
    elif state == "CP_USES" and is_admin:
        code = context.user_data["cp_code"]; days = context.user_data["cp_days"]
        db.data["coupons"][code] = {"plan": context.user_data["cp_plan"], "days": days, "uses": int(text), "used_by": [], "expires": (datetime.datetime.now() + relativedelta(days=days)).isoformat()}
        await db.save(); context.user_data.clear()
        await update.message.reply_text(f"✅ Cupón `{code}` forjado.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Admin", callback_data="adm_home")]]))

# =================================================================
# [8] STARS CHECKOUT
# =================================================================
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.pre_checkout_query.answer(ok=True)
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.message.from_user.id)
    pack = SupremeConfig.STARS_PACKAGES.get(update.message.successful_payment.invoice_payload.replace("stars_", ""))
    u = db.data["users"][uid]
    u["plan"] = pack["plan"]; cur_exp = parse(u["plan_expiry"]) if u.get("plan_expiry") else datetime.datetime.now()
    u["plan_expiry"] = (cur_exp + relativedelta(days=pack["days"])).isoformat()
    db.data["stats"]["stars_rev"] += update.message.successful_payment.total_amount; await db.save()
    await update.message.reply_text(f"💎 **COMPRA VERIFICADA**\nRango **{pack['name']}** activado.", parse_mode="Markdown")
    msg, kb = SupremeUI.home(u); await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")

# =================================================================
# [9] API REST DASHBOARD V900
# =================================================================
web_app = Flask("Supreme_API")
CORS(web_app)

@web_app.route('/')
def dashboard():
    return f"""
    <body style="background:#000;color:#0f0;font-family:monospace;text-align:center;padding:50px;">
        <h1>ISHAK SUPREME-MAIL V900</h1>
        <p>CEO: Ishak (@izi_1244)</p>
        <p>KERNEL STATUS: ONLINE [VEO3-ES ACTIVE]</p>
        <p>USERS: {len(db.data['users'])} | VAULTS: {db.data['stats']['emails_gen']}</p>
        <p>REVENUE: {db.data['stats']['stars_rev']} STARS</p>
    </body>
    """

def run_web():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    web_app.run(host='0.0.0.0', port=SupremeConfig.PORT)

# =================================================================
# [10] IGNICIÓN
# =================================================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"🚨 EXCEPCIÓN FATAL DETECTADA: {context.error}")

def main():
    print("=" * 80)
    print(f"🚀 [V900 SUPREME] INICIANDO NÚCLEO...")
    print(f"🔒 CREDENCIALES CARGADAS. DIRECTOR: ISHAK (ID: {SupremeConfig.ADMIN_ID})")
    print("=" * 80)
    
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token(SupremeConfig.TOKEN).build()
    
    app.job_queue.run_repeating(cron_job, interval=30, first=5)
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_machine))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    
    app.add_error_handler(error_handler)
    
    logger.info("🔄 Matriz Operativa.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
