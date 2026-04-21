"""
██╗███████╗██╗  ██╗███████╗██╗  ██╗    ███████╗██╗   ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗
██║██╔════╝██║  ██║██╔════╝██║ ██╔╝    ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝
██║███████╗███████║███████╗█████╔╝     ███████╗██║   ██║██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗  
██║╚════██║██╔══██║╚════██║██╔═██╗     ╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝  
██║███████║██║  ██║███████║██║  ██╗    ███████║╚██████╔╝██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗
╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
================================================================================
SISTEMA: ISHAK SUPREME-MAIL V900.7 - THE APEX ENTERPRISE ARCHITECTURE
CEO Y DIRECTOR SUPREMO: Ishak (@izi_1244) - Sede Central: España.
DIRECTIVA VEO3 [ESPAÑOL]: ACTIVA.
ESTADO: 100% REAL. CERO SIMULACIONES. MOTOR MAIL.GW INTEGRADO.
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

def bootstrap():
    try:
        import telegram
        import aiohttp
        import flask
        from bs4 import BeautifulSoup
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])

bootstrap()

import aiohttp
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    PreCheckoutQueryHandler, MessageHandler, ContextTypes, filters
)

class SupremeConfig:
    TOKEN = "8641633728:AAHgoeh4cEWS8o7_46l1b4-6xj3GCGvev_s"
    ADMIN_ID = 8398522835
    PORT = int(os.getenv("PORT", 8080))
    VERSION = "900.7.0-REAL-MATRIX"
    
    VAULT_DIR = "empire_vault"
    DB_PATH = os.path.join(VAULT_DIR, "supreme_db.json")

    # Eliminada la capacidad 'send_mail' por ser técnicamente imposible en APIs gratuitas.
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

# =================================================================
# [3] REAL MAIL ENGINE (Mail.gw API - Bypass Render limits safely)
# =================================================================
class MailEngine:
    BASE_URL = "https://api.mail.gw"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    @staticmethod
    def parse_email_html(html_content):
        if not html_content: return "Sin contenido.", [], []
        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        for a in soup.find_all('a', href=True):
            if len(links) < 8: links.append(f"🔗 [{a.text.strip() or 'Enlace'}]({a['href']})")
        images = []
        for img in soup.find_all('img', src=True):
            if img['src'].startswith('http') and len(images) < 5: images.append(img['src'])
        text = soup.get_text(separator="\n", strip=True)
        return text, links, images

    @classmethod
    async def req(cls, method, endpoint, token=None, json_data=None):
        headers = cls.HEADERS.copy()
        if token: headers["Authorization"] = f"Bearer {token}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.request(method, f"{cls.BASE_URL}{endpoint}", headers=headers, json=json_data) as r:
                    if r.status in [200, 201]: return await r.json()
                    elif r.status == 204: return True
                    else:
                        logger.error(f"Mail.gw API Error {r.status} en {endpoint}")
                        return None
        except Exception as e:
            logger.error(f"MailEngine Request Exception: {e}")
            return None

    @classmethod
    async def get_domains(cls):
        res = await cls.req("GET", "/domains")
        return res.get("hydra:member", []) if res else []

    @classmethod
    async def create_account(cls, domain, custom_username=None):
        username = custom_username if custom_username else ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + "X!"
        
        acc_data = await cls.req("POST", "/accounts", json_data={"address": address, "password": password})
        if acc_data:
            token_data = await cls.req("POST", "/token", json_data={"address": address, "password": password})
            if token_data:
                return {
                    "address": address, "password": password, 
                    "token": token_data["token"], "domain": domain, 
                    "id": acc_data["id"]
                }
        return None

    @classmethod
    async def get_messages(cls, token):
        res = await cls.req("GET", "/messages", token=token)
        return res.get("hydra:member", []) if res else []

    @classmethod
    async def read_message(cls, token, msg_id):
        return await cls.req("GET", f"/messages/{msg_id}", token=token)

    @classmethod
    async def delete_account(cls, token, account_id):
        return await cls.req("DELETE", f"/accounts/{account_id}", token=token)

    @classmethod
    async def download_attachment(cls, token, msg_id, attachment_id, filename):
        headers = cls.HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}/messages/{msg_id}/download/{attachment_id}", headers=headers) as r:
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
                                
                                text = full_m.get("intro", "")
                                alert = (f"🔔 **NUEVO PAQUETE INTERCEPTADO**\n"
                                         f"─────────────────\n"
                                         f"📥 **Bóveda:** `{acc['address']}`\n"
                                         f"👤 **Origen:** `{m['from']['address']}`\n"
                                         f"📝 **Asunto:** `{m['subject'].replace('`', '')}`\n"
                                         f"─────────────────\n"
                                         f"📄 **Extracto:**\n{text[:200]}...")
                                         
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
        msg = (f"🌐 **ISHAK SUPREME-MAIL V900.7**\n"
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
        msg = ("➕ **FORJA DE BÓVEDA REAL**\nSeleccione el método de síntesis de credenciales:")
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
            [InlineKeyboardButton("🔄 Sincronizar Bandeja", callback_data=f"inbox_{idx}"), InlineKeyboardButton("⏱️ Auto-Destrucción", callback_data=f"timer_{idx}")],
            [InlineKeyboardButton("📄 Exportar TXT (VIP)", callback_data=f"export_{idx}"), InlineKeyboardButton("🗑️ Purgar", callback_data=f"del_{idx}")],
            [InlineKeyboardButton("⬅️ Centro de Comunicaciones", callback_data="app_inboxes")]
        ])

    @staticmethod
    def admin_panel():
        s = db.data["stats"]
        msg = ("👁️ **TERMINAL SUPREMA (DIRECTOR ISHAK)**\nControl absoluto de la infraestructura.\n──────────────────────\n"
               f"👥 Ciudadanos: `{len(db.data['users'])}`\n📧 Bóvedas: `{s['emails_gen']}`\n"
               f"⭐️ Ingresos XTR: `{s['stars_rev']}`\n──────────────────────")
        kb = [[InlineKeyboardButton("👁️ Espionaje", callback_data="adm_users_0"), InlineKeyboardButton("🎫 Acuñar Cupón", callback_data="adm_new_cp")],
              [InlineKeyboardButton("📢 Transmisión", callback_data="adm_bc"), InlineKeyboardButton("⬅️ Salir", callback_data="app_home")]]
        return msg, InlineKeyboardMarkup(kb)

# =================================================================
# [6] ROUTER V900
# =================================================================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📥 [RADAR V900] ¡COMANDO /START RECIBIDO!")
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
            msg = "⭐️ **MERCADO VIP SUPREMO**\nAdquiere licencias de grado militar (TITAN) para desbloquear Custom Alias, Extracción TXT, Adjuntos y API."
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
            
            await q.edit_message_text("⏳ Pidiendo datos a la red Mail.gw...")
            domains = await MailEngine.get_domains()
            if not domains: return await q.edit_message_text("❌ Servidores de la API caídos.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_create_menu")]]))

            if action == "random":
                await q.edit_message_text("⏳ Creando cuenta real en el servidor...")
                d = domains[random.randint(0, len(domains)-1)] if plan_cfg["custom_alias"] else domains[0]
                acc = await MailEngine.create_account(d["domain"])
                if acc:
                    u["emails"].append(acc); db.data["stats"]["emails_gen"] += 1; await db.save()
                    msg = f"✅ **BÓVEDA LISTA Y REAL**\n📧 `{acc['address']}`\n🔑 `{acc['password']}`"
                    await q.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")], [InlineKeyboardButton("⬅️ Menú", callback_data="app_home")]]))
                else: await q.edit_message_text("❌ La API denegó la creación.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_create_menu")]]))
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
            await q.edit_message_text(f"🔄 Consultando a la red Mail.gw por `{acc['address']}`...", parse_mode="Markdown")
            msgs = await MailEngine.get_messages(acc["token"])
            kb = []
            if msgs:
                for m in msgs[:7]: kb.append([InlineKeyboardButton(f"📖 {m['from']['address'][:12]}.. | {m['subject'][:15]}", callback_data=f"read_{idx}_{m['id']}")])
            
            msg_text = f"📥 **Bóveda:** `{acc['address']}`\n"
            if acc.get("timer"): msg_text += f"🧨 Autodestrucción en: `{acc['timer'][:16]}`\n"
            
            if not msgs:
                msg_text += "\n📭 _La bandeja está vacía. Envía un correo a esta dirección para probar._\n"
            else:
                msg_text += f"\nPaquetes interceptados reales: {len(msgs)}\n"
            
            msg_text += f"\n🔄 Última actualización: `{datetime.datetime.now().strftime('%H:%M:%S')}`"
            await q.edit_message_text(msg_text, reply_markup=SupremeUI.inbox_actions(idx), parse_mode="Markdown")
        
        elif data.startswith("read_"):
            parts = data.split("_"); idx = int(parts[1]); msg_id = parts[2]; acc = u["emails"][idx]
            await q.edit_message_text("⏳ Desencriptando Deep-Scan...")
            
            full_m = await MailEngine.read_message(acc["token"], msg_id)
            if not full_m: return await q.answer("❌ Error al leer el mensaje.", show_alert=True)
            
            if "id" not in u.get("read_msg_ids", []): u.setdefault("read_msg_ids", []).append(full_m["id"]); await db.save()
            
            text_body = full_m.get("text", "").strip()
            html_body = full_m.get("html", [])[0] if isinstance(full_m.get("html"), list) else full_m.get("html", "")
            parsed_text, links, images = MailEngine.parse_email_html(html_body)
            
            final_body = text_body if text_body else parsed_text
            body_safe = final_body[:3000].replace("`", "'") 
            
            msg_text = (f"📨 **DATA INTERCEPTADA**\n"
                        f"─────────────────\n"
                        f"👤 **De:** `{full_m['from']['address']}`\n"
                        f"📝 **Asunto:** `{full_m['subject'].replace('`', '')}`\n"
                        f"─────────────────\n\n"
                        f"📄 **Cuerpo del Mensaje:**\n{body_safe}") 
            
            if links: msg_text += "\n\n🔗 **ENLACES:**\n" + "\n".join(links)
            if images: msg_text += "\n\n🖼 **IMÁGENES:**\n" + "\n".join([f"• [Abrir Imagen]({img})" for img in images])

            kb = []
            if full_m.get("hasAttachments") and plan_cfg["attachments"]:
                kb.append([InlineKeyboardButton(f"📎 Bajar Adjuntos ({len(full_m['attachments'])})", callback_data=f"dlall_{idx}_{msg_id}")])
            
            kb.append([InlineKeyboardButton("⬅️ Bandeja", callback_data=f"inbox_{idx}")])
            await q.edit_message_text(msg_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
            
        elif data.startswith("dlall_"):
            parts = data.split("_"); idx = int(parts[1]); msg_id = parts[2]; acc = u["emails"][idx]
            await q.answer("⏳ Extrayendo adjuntos de la red...", show_alert=False)
            full_m = await MailEngine.read_message(acc["token"], msg_id)
            if not full_m or not full_m.get("attachments"):
                return await q.answer("❌ Sin adjuntos.", show_alert=True)
            for att in full_m["attachments"]:
                path = await MailEngine.download_attachment(acc["token"], msg_id, att["id"], att["name"])
                if path:
                    with open(path, 'rb') as doc: await context.bot.send_document(q.message.chat_id, doc, caption=f"📎 `{att['name']}`", parse_mode="Markdown")
                    os.remove(path)

        elif data.startswith("del_"):
            idx = int(data.split("_")[1])
            acc = u["emails"].pop(idx)
            await MailEngine.delete_account(acc["token"], acc["id"]); await db.save()
            await q.answer("🗑️ Bóveda aniquilada en la red real.", show_alert=True)
            msg, kb = SupremeUI.inboxes(u); await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
            
        elif data.startswith("export_"):
            if not plan_cfg["export_txt"]: return await q.answer("Exclusivo VIP.", show_alert=True)
            idx = int(data.split("_")[1]); acc = u["emails"][idx]
            await q.answer("⏳ Exportando bóveda a TXT...", show_alert=False)
            msgs = await MailEngine.get_messages(acc["token"])
            if not msgs: return await q.answer("Bandeja vacía.", show_alert=True)
            
            content = f"--- EXPORTACIÓN B2B REAL: {acc['address']} ---\n\n"
            for m in msgs:
                full_m = await MailEngine.read_message(acc["token"], m["id"])
                if full_m:
                    text_body = full_m.get("text", "") or MailEngine.parse_email_html(full_m.get("html", ""))[0]
                    content += f"De: {full_m['from']['address']}\nFecha: {full_m['createdAt']}\nAsunto: {full_m['subject']}\n\n{text_body}\n"
                    content += "-" * 50 + "\n"
            
            path = os.path.join(SupremeConfig.VAULT_DIR, f"exp_{uuid.uuid4().hex[:8]}.txt")
            with open(path, "w", encoding="utf-8") as f: f.write(content)
            with open(path, "rb") as doc: await context.bot.send_document(q.message.chat_id, doc, caption=f"📄 **Respaldo Corporativo:** `{acc['address']}`", parse_mode="Markdown")
            os.remove(path); db.data["stats"]["exports"] += 1; await db.save()

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
        m = await update.message.reply_text("⏳ Sintetizando cuenta real...")
        acc = await MailEngine.create_account(domains[0]["domain"], custom_username=alias)
        context.user_data.clear()
        if acc:
            u["emails"].append(acc); db.data["stats"]["emails_gen"] += 1; await db.save()
            await m.edit_text(f"✅ **ALIAS CREADO**\n📧 `{acc['address']}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")]]))
        else: await m.edit_text("❌ El alias ya existe o hay falla en la red de la API.")

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
        <h1>ISHAK SUPREME-MAIL V900.7</h1>
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
    print(f"🚀 [V900.7 SUPREME] INICIANDO NÚCLEO...")
    print(f"🔒 CREDENCIALES CARGADAS. DIRECTOR: ISHAK (ID: {SupremeConfig.ADMIN_ID})")
    print("=" * 80)
    
    threading.Thread(target=run_web, daemon=True).start()
    app = ApplicationBuilder().token(SupremeConfig.TOKEN).build()
    
    app.job_queue.run_repeating(cron_job, interval=30, first=5)
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_machine))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_error_handler(error_handler)
    
    logger.info("🔄 Matriz Operativa.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
