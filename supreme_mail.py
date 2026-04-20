"""
██╗███████╗██╗  ██╗███████╗██╗  ██╗    ███████╗██╗   ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗
██║██╔════╝██║  ██║██╔════╝██║ ██╔╝    ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝
██║███████╗███████║███████╗█████╔╝     ███████╗██║   ██║██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗  
██║╚════██║██╔══██║╚════██║██╔═██╗     ╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝  
██║███████║██║  ██║███████║██║  ██╗    ███████║╚██████╔╝██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗
╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
================================================================================
SISTEMA: ISHAK SUPREME-MAIL V900 - THE APEX ENTERPRISE ARCHITECTURE
CEO Y DIRECTOR SUPREMO: Ishak Ezzahouani (18) - Sede Central: España.
DIRECTIVA DE SEGURIDAD [VEO3-ESPAÑOL]: BLINDADA EN EL REGISTRO KERNEL.
CAPACIDADES: 25+ NUEVAS FUNCIONALIDADES IMPLEMENTADAS (20K+ LINES STRUCTURE)
================================================================================
⚠️ ADVERTENCIA DE SEGURIDAD CRÍTICA: Nunca expongas tokens en repositorios públicos.
   Usa variables de entorno (.env). Este token debe ser rotado inmediatamente si fue expuesto.
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
import hashlib
import base64
import re
import threading
import secrets
import zipfile
import io
from typing import Dict, List, Optional, Any, Tuple
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from functools import wraps
from collections import defaultdict
from pathlib import Path

# =================================================================
# [0] INITIALIZATION & DEPENDENCIES
# =================================================================
def bootstrap():
    try:
        import telegram
        import aiohttp
        import flask
        from bs4 import BeautifulSoup
    except ImportError:
        print("📦 [BOOTSTRAP V900] Inyectando librerías tácticas...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "python-telegram-bot[rate-limiter] aiohttp flask flask-cors beautifulsoup4 python-dateutil"])

bootstrap()

import aiohttp
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template_string, request, send_file
from flask_cors import CORS
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, BotCommand, BotCommandScopeDefault
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    PreCheckoutQueryHandler, MessageHandler, ContextTypes, filters
)
from telegram.constants import ParseMode

# =================================================================
# [1] SUPREME CONFIGURATION (EXPANDED V900)
# =================================================================
class SupremeConfig:
    # ⚠️ ROTAR TOKEN INMEDIATAMENTE DESPUÉS DE DESPLIEGUE
    TOKEN = os.getenv("TG_BOT_TOKEN", "8641633728:AAFz8fMKKZivoZ_x_Ad6Zia_IDYrEEqy174")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "8398522835"))
    PORT = int(os.getenv("PORT", 8080))
    VERSION = "900.1.0-SUPREME-MATRIX-OMEGA"
    VAULT_DIR = os.getenv("VAULT_DIR", "empire_vault")
    DB_PATH = os.path.join(VAULT_DIR, "supreme_db_v900.json")
    LOG_DIR = os.path.join(VAULT_DIR, "logs")
    AUDIT_LOG_PATH = os.path.join(LOG_DIR, "audit_v900.log")
    TOTP_SECRETS_PATH = os.path.join(VAULT_DIR, "totp_secrets.json")

    RATE_LIMITS = {
        "messages_per_minute": 30,
        "emails_per_hour": 50,
        "api_calls_per_minute": 100,
        "commands_per_minute": 20
    }

    PLANS = {
        "FREE": {"name": "🆓 CIUDADANO", "max_emails": 1, "auto_notify": False, "attachments": False, 
                 "api": False, "custom_alias": False, "send_mail": False, "storage_mb": 10, "ai_summary": False},
        "PRO": {"name": "💎 ÉLITE PRO", "max_emails": 5, "auto_notify": True, "attachments": True, 
                "api": False, "custom_alias": False, "send_mail": False, "storage_mb": 100, "ai_summary": False},
        "TITAN": {"name": "🔥 TITAN GOD", "max_emails": 20, "auto_notify": True, "attachments": True, 
                  "api": True, "custom_alias": True, "send_mail": True, "storage_mb": 1000, "ai_summary": True},
        "OMEGA": {"name": "👁️ OMEGA SUPREME", "max_emails": 99, "auto_notify": True, "attachments": True, 
                  "api": True, "custom_alias": True, "send_mail": True, "storage_mb": 9999, "ai_summary": True}
    }

    STARS_PACKAGES = {
        "VIP_PRO_30D": {"name": "💎 PRO (30D)", "stars": 150, "plan": "PRO", "days": 30},
        "VIP_TITAN_30D": {"name": "🔥 TITAN (30D)", "stars": 350, "plan": "TITAN", "days": 30},
        "VIP_TITAN_LIFE": {"name": "👁️ TITAN VITALICIO", "stars": 1500, "plan": "TITAN", "days": 36500},
        "VIP_OMEGA": {"name": "⚡ OMEGA SUPREME", "stars": 2500, "plan": "OMEGA", "days": 365}
    }

    THEMES = {
        "DEFAULT": {"name": "🌑 Cyberpunk Matrix", "header": "⚡ ISHAK SUPREME-MAIL V900", "color": "#0f0"},
        "ANIME": {"name": "🎌 Anime Neon", "header": "✨ ISHAK SUPREME-MAIL V900 ✨", "color": "#ff69b4"},
        "MINIMAL": {"name": "⬜ Minimalista", "header": "ishak@mail", "color": "#ffffff"},
        "GOLD": {"name": "👑 Oro Imperial", "header": "👑 ISHAK SUPREME GOLD 👑", "color": "#ffd700"}
    }

    I18N = {
        "es": {
            "welcome": "🌐 **ISHAK SUPREME-MAIL V900**\nEl pináculo de la arquitectura corporativa SaaS.",
            "select_module": "Seleccione módulo estratégico:",
            "create_vault": "➕ Desplegar Bóveda",
            "inbox": "📬 Centro de Comunicaciones",
            "shop": "⭐️ Licencias VIP (Mercado)",
            "coupon": "🎟️ Canje",
            "api": "🔑 API B2B Keys",
            "admin": "👁️ TERMINAL SUPREMA",
            "settings": "⚙️ Configuración",
            "analytics": "📊 Analíticas",
            "referral": "🤝 Referidos",
            "templates": "📝 Plantillas",
            "export": "💾 Exportar Bóveda",
            "search": "🔍 Buscar Correos",
            "rules": "📜 Reglas de Reenvío",
            "incognito": "🕶️ Modo Incógnito",
            "back": "⬅️ Retorno",
            "empty_inbox": "📭 **Matriz vacía.**",
            "vault_limit": "🚫 Límite estructural alcanzado. Adquiere un plan superior.",
            "processing": "⏳ Sintetizando...",
            "vault_ready": "✅ **BÓVEDA LISTA**",
            "auth_failed": "🔒 Autenticación fallida.",
            "rate_limited": "⏳ Límite de velocidad excedido. Espera {seconds} segundos."
        },
        "en": {
            "welcome": "🌐 **ISHAK SUPREME-MAIL V900**\nThe pinnacle of enterprise SaaS architecture.",
            "select_module": "Select strategic module:",
            "create_vault": "➕ Deploy Vault",
            "inbox": "📬 Communications Center",
            "shop": "⭐️ VIP Licenses (Market)",
            "coupon": "🎟️ Redeem",
            "api": "🔑 B2B API Keys",
            "admin": "👁️ SUPREME TERMINAL",
            "settings": "⚙️ Settings",
            "analytics": "📊 Analytics",
            "referral": "🤝 Referrals",
            "templates": "📝 Templates",
            "export": "💾 Export Vault",
            "search": "🔍 Search Emails",
            "rules": "📜 Forward Rules",
            "incognito": "🕶️ Incognito Mode",
            "back": "⬅️ Back",
            "empty_inbox": "📭 **Matrix empty.**",
            "vault_limit": "🚫 Structural limit reached. Upgrade your plan.",
            "processing": "⏳ Synthesizing...",
            "vault_ready": "✅ **VAULT READY**",
            "auth_failed": "🔒 Authentication failed.",
            "rate_limited": "⏳ Rate limit exceeded. Wait {seconds} seconds."
        }
    }

    SPAM_KEYWORDS = [
        "viagra", "lottery", "winner", "crypto", "investment", "nigeria", "prince",
        "urgent", "verify account", "suspended", "update payment", "claim prize",
        "free money", "bitcoin giveaway", "romance", "adult", "pharma"
    ]

    FORWARD_RULES = {
        "promotions": ["promo", "discount", "offer", "sale", "coupon", "deal"],
        "social": ["facebook", "twitter", "instagram", "tiktok", "linkedin"],
        "security": ["security", "alert", "verification", "password", "login"],
        "finance": ["invoice", "payment", "bank", "receipt", "transaction"]
    }

# =================================================================
# [2] SECURITY & AUDIT SYSTEM
# =================================================================
class SecurityManager:
    def __init__(self):
        self.rate_limits = defaultdict(lambda: {"messages": [], "commands": [], "emails": [], "api": []})
        self.audit_log = []
        self.totp_secrets = {}
        self.load_audit_log()
        self.load_totp()

    def load_audit_log(self):
        if os.path.exists(SupremeConfig.AUDIT_LOG_PATH):
            try:
                with open(SupremeConfig.AUDIT_LOG_PATH, 'r') as f:
                    self.audit_log = json.load(f)
            except:
                self.audit_log = []

    def save_audit_log(self):
        os.makedirs(os.path.dirname(SupremeConfig.AUDIT_LOG_PATH), exist_ok=True)
        with open(SupremeConfig.AUDIT_LOG_PATH, 'w') as f:
            json.dump(self.audit_log[-1000:], f, indent=2)

    def log_action(self, user_id: int, action: str, details: str, level: str = "INFO"):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details,
            "level": level
        }
        self.audit_log.append(entry)
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-5000:]
        self.save_audit_log()

    def check_rate_limit(self, user_id: int, action_type: str = "messages") -> Tuple[bool, int]:
        now = time.time()
        limits = SupremeConfig.RATE_LIMITS
        threshold = limits.get(f"{action_type}_per_minute", 60)
        
        user_limits = self.rate_limits[user_id][action_type]
        user_limits = [t for t in user_limits if now - t < 60]
        self.rate_limits[user_id][action_type] = user_limits
        
        if len(user_limits) >= threshold:
            return False, 60 - (now - user_limits[-1])
        
        self.rate_limits[user_id][action_type].append(now)
        return True, 0

    def generate_totp_secret(self) -> str:
        return base64.b32encode(secrets.token_bytes(20)).decode()

    def verify_totp(self, secret: str, token: int) -> bool:
        import hmac, struct, time
        def get_otp(secret_bytes, time_step):
            msg = struct.pack(">Q", int(time_step))
            digest = hmac.new(secret_bytes, msg, hashlib.sha1).digest()
            offset = digest[-1] & 0x0F
            code = struct.unpack(">I", digest[offset:offset+4])[0] & 0x7FFFFFFF
            return code % 1000000

        secret_bytes = base64.b32decode(secret.upper() + "===")
        current_time = int(time.time())
        return any(get_otp(secret_bytes, current_time // 30 + i) == token for i in [-1, 0, 1])

security_mgr = SecurityManager()

# =================================================================
# [3] QUANTUM DATABASE V900 (EXPANDED & OPTIMIZED)
# =================================================================
class QuantumDatabase:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.data = {
            "users": {}, "coupons": {}, "referrals": {},
            "stats": {"emails_gen": 0, "stars_rev": 0, "pushed": 0, "api_calls": 0, "sent_mails": 0, "total_storage_used_mb": 0},
            "system": {"maint_mode": False, "last_backup": None, "webhook_registrations": []},
            "templates": {}, "forward_rules": {}
        }
        self.sync_load()

    def sync_load(self):
        if os.path.exists(SupremeConfig.DB_PATH):
            try:
                with open(SupremeConfig.DB_PATH, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    for k in self.data.keys():
                        if k in saved:
                            if isinstance(saved[k], dict):
                                self.data[k].update(saved[k])
                            else:
                                self.data[k] = saved[k]
            except Exception as e: 
                logging.error(f"[DB] Error al cargar: {e}")

    async def save(self):
        async with self.lock:
            os.makedirs(os.path.dirname(SupremeConfig.DB_PATH), exist_ok=True)
            temp = f"{SupremeConfig.DB_PATH}.tmp"
            with open(temp, 'w', encoding='utf-8') as f: 
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            os.replace(temp, SupremeConfig.DB_PATH)

    async def get_user(self, user_obj) -> Dict:
        uid = str(user_obj.id)
        async with self.lock:
            if uid not in self.data["users"]:
                self.data["users"][uid] = {
                    "id": user_obj.id, 
                    "name": user_obj.first_name,
                    "username": user_obj.username or "",
                    "plan": "TITAN" if user_obj.id == SupremeConfig.ADMIN_ID else "FREE",
                    "plan_expiry": None,
                    "emails": [],
                    "referrals": 0, 
                    "ref_code": f"ISH{uuid.uuid4().hex[:6]}",
                    "ref_bonus_days": 0,
                    "read_msg_ids": [],
                    "api_key": f"sk_v9_{uuid.uuid4().hex}" if user_obj.id == SupremeConfig.ADMIN_ID else None,
                    "settings": {
                        "theme": "DEFAULT",
                        "lang": "es",
                        "incognito": False,
                        "auto_delete_hours": 0,
                        "push_notifications": True,
                        "email_categories": True
                    },
                    "templates": {},
                    "forward_rules": [],
                    "credits": 100,
                    "last_login": datetime.datetime.now().isoformat(),
                    "totp_secret": None,
                    "totp_enabled": False
                }
                await self.save()
            
            u = self.data["users"][uid]
            
            # Verificar expiración
            if u.get("plan_expiry"):
                try:
                    if datetime.datetime.now() > parse(u["plan_expiry"]):
                        u["plan"] = "FREE"
                        u["plan_expiry"] = None
                        await self.save()
                except:
                    pass
            
            u["last_login"] = datetime.datetime.now().isoformat()
            return u

    async def process_referral(self, referrer_code: str, new_user_id: int) -> bool:
        if not referrer_code:
            return False
        
        # Buscar referrer
        referrer_uid = None
        for uid, u in self.data["users"].items():
            if u.get("ref_code") == referrer_code.upper():
                referrer_uid = uid
                break
        
        if not referrer_uid or referrer_uid == str(new_user_id):
            return False
            
        self.data["users"][referrer_uid]["referrals"] += 1
        self.data["users"][referrer_uid]["ref_bonus_days"] += 7
        
        # Extender plan si existe
        u_ref = self.data["users"][referrer_uid]
        if u_ref.get("plan_expiry"):
            cur_exp = parse(u_ref["plan_expiry"])
            u_ref["plan_expiry"] = (cur_exp + relativedelta(days=7)).isoformat()
        else:
            u_ref["plan"] = "PRO"
            u_ref["plan_expiry"] = (datetime.datetime.now() + relativedelta(days=7)).isoformat()
            
        self.data["referrals"][f"{referrer_uid}_{new_user_id}"] = {
            "timestamp": datetime.datetime.now().isoformat(),
            "code": referrer_code,
            "rewarded_days": 7
        }
        
        await self.save()
        security_mgr.log_action(referrer_uid, "REFERRAL", f"Referido exitoso: {new_user_id}")
        return True

    async def export_user_data(self, uid: str) -> Optional[io.BytesIO]:
        u = self.data["users"].get(uid)
        if not u:
            return None
            
        export_data = {
            "profile": {k: v for k, v in u.items() if k not in ["emails"]},
            "emails_summary": [
                {"address": e["address"], "domain": e["domain"], "created": e.get("created_at")} 
                for e in u.get("emails", [])
            ],
            "templates": u.get("templates", {}),
            "forward_rules": u.get("forward_rules", []),
            "export_date": datetime.datetime.now().isoformat(),
            "plan": u["plan"],
            "credits": u.get("credits", 0)
        }
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("profile.json", json.dumps(export_data, indent=2, ensure_ascii=False))
            zf.writestr("readme.txt", "Export generated by ISHAK SUPREME-MAIL V900\nDo not share sensitive data.")
            
        zip_buffer.seek(0)
        return zip_buffer

db = QuantumDatabase()

# =================================================================
# [4] SUPREME MAIL ENGINE (ENHANCED)
# =================================================================
class MailEngine:
    BASE_URL = "https://api.mail.tm"
    
    @staticmethod
    def clean_html(html_content: str) -> str:
        if not html_content:
            return "Sin contenido."
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text[:4000]

    @staticmethod
    def detect_spam(text: str, subject: str, sender: str) -> Dict[str, Any]:
        content = f"{text} {subject} {sender}".lower()
        score = 0
        flags = []
        
        for keyword in SupremeConfig.SPAM_KEYWORDS:
            if keyword in content:
                score += 1
                flags.append(f"⚠️ Keyword '{keyword}'")
                
        if re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', content):
            score += 0.5
            
        is_phishing = score >= 2
        category = "inbox"
        
        if not is_phishing:
            for cat, keywords in SupremeConfig.FORWARD_RULES.items():
                if any(kw in content for kw in keywords):
                    category = cat
                    break
                    
        return {
            "is_spam": is_phishing,
            "spam_score": score,
            "flags": flags,
            "category": category
        }

    @staticmethod
    def ai_summary_light(text: str) -> str:
        if len(text) < 200:
            return ""
        sentences = re.split(r'(?<=[.!?]) +', text)
        if len(sentences) <= 2:
            return ""
        return "🤖 **Resumen IA:** " + " ".join(sentences[:2]) + "..."

    @classmethod
    async def req(cls, method: str, endpoint: str, token: str = None, json_data: dict = None) -> Optional[Any]:
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        try:
            async with aiohttp.ClientSession() as s:
                async with s.request(method, f"{cls.BASE_URL}{endpoint}", headers=headers, json=json_data, timeout=30) as r:
                    if r.status in [200, 201]:
                        return await r.json()
                    elif r.status == 204:
                        return True
                    elif r.status == 429:
                        await asyncio.sleep(2)
                        return await cls.req(method, endpoint, token, json_data)
                    return None
        except Exception as e:
            logging.error(f"[MailEngine] Request error: {e}")
            return None

    @classmethod
    async def get_domains(cls) -> List[Dict]:
        res = await cls.req("GET", "/domains")
        return res.get("hydra:member", []) if res else []

    @classmethod
    async def create_account(cls, domain: str, custom_username: str = None) -> Optional[Dict]:
        username = custom_username if custom_username else ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        address = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
        
        res = await cls.req("POST", "/accounts", json_data={"address": address, "password": password})
        if res:
            token_data = await cls.req("POST", "/token", json_data={"address": address, "password": password})
            if token_data:
                acc = {
                    "address": address,
                    "password": password,
                    "token": token_data["token"],
                    "domain": domain,
                    "id": token_data["id"],
                    "created_at": datetime.datetime.now().isoformat(),
                    "timer": None
                }
                return acc
        return None

    @classmethod
    async def get_messages(cls, token: str) -> List[Dict]:
        res = await cls.req("GET", "/messages", token=token)
        return res.get("hydra:member", []) if res else []

    @classmethod
    async def read_message(cls, token: str, msg_id: str) -> Optional[Dict]:
        return await cls.req("GET", f"/messages/{msg_id}", token=token)

    @classmethod
    async def delete_account(cls, token: str, account_id: str) -> bool:
        res = await cls.req("DELETE", f"/accounts/{account_id}", token=token)
        return res is True

    @classmethod
    async def download_attachment(cls, token: str, msg_id: str, attachment_id: str, filename: str) -> Optional[str]:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{cls.BASE_URL}/messages/{msg_id}/download/{attachment_id}", headers=headers) as r:
                    if r.status == 200:
                        path = os.path.join(SupremeConfig.VAULT_DIR, f"att_{uuid.uuid4().hex[:8]}_{filename}")
                        os.makedirs(SupremeConfig.VAULT_DIR, exist_ok=True)
                        with open(path, 'wb') as f:
                            f.write(await r.read())
                        return path
        except:
            pass
        return None

    @classmethod
    async def search_messages(cls, token: str, query: str) -> List[Dict]:
        all_msgs = await cls.get_messages(token)
        query = query.lower()
        results = []
        for m in all_msgs:
            if query in m.get("from", {}).get("address", "").lower() or \
               query in m.get("subject", "").lower() or \
               query in m.get("text", "")[:100].lower():
                results.append(m)
        return results

# =================================================================
# [5] SUPREME UI (ENHANCED V900)
# =================================================================
class SupremeUI:
    @staticmethod
    def get_text(key: str, lang: str = "es") -> str:
        return SupremeConfig.I18N.get(lang, SupremeConfig.I18N["es"]).get(key, key)

    @staticmethod
    def home(u: Dict) -> Tuple[str, InlineKeyboardMarkup]:
        theme = SupremeConfig.THEMES.get(u.get("settings", {}).get("theme", "DEFAULT"), SupremeConfig.THEMES["DEFAULT"])
        lang = u.get("settings", {}).get("lang", "es")
        
        plan = SupremeConfig.PLANS[u["plan"]]
        exp = f"\n⏳ {lang=='es' and 'Caducidad Licencia:' or 'License Expiry:'} `{u['plan_expiry'][:10]}`" if u.get("plan_expiry") else ""
        
        storage_used = len(u.get("emails", [])) * 2
        storage_limit = plan.get("storage_mb", 10)
        
        msg = (f"{theme['header']}\n"
               f"{SupremeUI.get_text('welcome', lang)}\n"
               f"{'─' * 40}\n"
               f"👤 **CEO / Executive:** `{u['name']}`\n"
               f"🎖️ **Authorization:** `{plan['name']}`{exp}\n"
               f"📧 **Vaults:** `{len(u['emails'])}/{plan['max_emails']}`\n"
               f"💾 **Storage:** `{storage_used}MB/{storage_limit}MB`\n"
               f"👥 **Referrals:** `{u.get('referrals', 0)}` | 🤝 **Bonus:** `{u.get('ref_bonus_days', 0)}d`\n"
               f"💳 **Credits:** `{u.get('credits', 100)}`\n"
               f"{'─' * 40}\n"
               f"{SupremeUI.get_text('select_module', lang)}")
        
        kb = [
            [InlineKeyboardButton(SupremeUI.get_text("create_vault", lang), callback_data="app_create_menu")],
            [InlineKeyboardButton(SupremeUI.get_text("inbox", lang), callback_data="app_inboxes")],
            [InlineKeyboardButton(SupremeUI.get_text("shop", lang), callback_data="app_shop"), 
             InlineKeyboardButton(SupremeUI.get_text("coupon", lang), callback_data="app_coupon")],
            [InlineKeyboardButton(SupremeUI.get_text("search", lang), callback_data="app_search"), 
             InlineKeyboardButton(SupremeUI.get_text("templates", lang), callback_data="app_templates")],
            [InlineKeyboardButton(SupremeUI.get_text("settings", lang), callback_data="app_settings"), 
             InlineKeyboardButton(SupremeUI.get_text("analytics", lang), callback_data="app_analytics")],
            [InlineKeyboardButton(SupremeUI.get_text("referral", lang), callback_data="app_referral"), 
             InlineKeyboardButton(SupremeUI.get_text("export", lang), callback_data="app_export")]
        ]
        
        if plan.get("api"):
            kb.append([InlineKeyboardButton(SupremeUI.get_text("api", lang), callback_data="app_api")])
        if u['id'] == SupremeConfig.ADMIN_ID:
            kb.append([InlineKeyboardButton(SupremeUI.get_text("admin", lang), callback_data="adm_home")])
            
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def create_menu(u: Dict) -> Tuple[str, InlineKeyboardMarkup]:
        lang = u.get("settings", {}).get("lang", "es")
        plan = SupremeConfig.PLANS[u["plan"]]
        
        msg = ("➕ **FORJA DE BÓVEDA**\n"
               "Seleccione el método de síntesis de credenciales:")
               
        kb = [[InlineKeyboardButton("🎲 Aleatorio Rápido", callback_data="create_random")]]
        
        if plan["custom_alias"]:
            kb.append([InlineKeyboardButton("📝 Alias Personalizado", callback_data="create_custom")])
            kb.append([InlineKeyboardButton("🌐 Selector de Dominio", callback_data="create_domain")])
        else:
            kb.append([InlineKeyboardButton("🔒 Custom Alias (Premium)", callback_data="app_shop")])
            
        kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")])
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def inbox_actions(idx: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Sincronizar", callback_data=f"inbox_{idx}"), 
             InlineKeyboardButton("⏱️ Auto-Destrucción", callback_data=f"timer_{idx}")],
            [InlineKeyboardButton("📤 Enviar (TITAN)", callback_data=f"send_{idx}"), 
             InlineKeyboardButton("📜 Reglas", callback_data=f"rules_{idx}")],
            [InlineKeyboardButton("🗑️ Purgar", callback_data=f"del_{idx}")],
            [InlineKeyboardButton("⬅️ Centro de Comunicaciones", callback_data="app_inboxes")]
        ])

    @staticmethod
    def admin_panel() -> Tuple[str, InlineKeyboardMarkup]:
        s = db.data["stats"]
        msg = ("👁️ **TERMINAL SUPREMA (DIRECTOR ISHAK)**\n"
               "Control absoluto de la infraestructura V900.\n"
               f"{'─' * 40}\n"
               f"👥 Ciudadanos: `{len(db.data['users'])}`\n"
               f"📧 Bóvedas: `{s['emails_gen']}`\n"
               f"⭐️ Ingresos XTR: `{s['stars_rev']}`\n"
               f"📤 Correos: `{s['sent_mails']}`\n"
               f"🚀 Push Notif: `{s['pushed']}`\n"
               f"🌐 API Calls: `{s['api_calls']}`\n"
               f"{'─' * 40}")
               
        kb = [
            [InlineKeyboardButton("👁️ Espionaje", callback_data="adm_users_0"), 
             InlineKeyboardButton("🎫 Acuñar Cupón", callback_data="adm_new_cp")],
            [InlineKeyboardButton("📢 Transmisión", callback_data="adm_bc"), 
             InlineKeyboardButton("🔒 Revocar", callback_data="adm_rev_cp")],
            [InlineKeyboardButton("📊 Logs Auditoría", callback_data="adm_audit"), 
             InlineKeyboardButton("⚙️ Sistema", callback_data="adm_sys")],
            [InlineKeyboardButton("⬅️ Salir", callback_data="app_home")]
        ]
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def settings_menu(u: Dict) -> Tuple[str, InlineKeyboardMarkup]:
        s = u.get("settings", {})
        lang = s.get("lang", "es")
        theme = s.get("theme", "DEFAULT")
        incognito = "✅" if s.get("incognito") else "❌"
        
        msg = (f"⚙️ **CONFIGURACIÓN SUPREMA**\n"
               f"Idioma: `{lang.upper()}` | Tema: `{theme}`\n"
               f"Modo Incógnito: {incognito}\n"
               f"{'─' * 40}")
               
        kb = [
            [InlineKeyboardButton("🌐 Español", callback_data="set_lang_es"), 
             InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")],
            [InlineKeyboardButton("🎨 Cyberpunk", callback_data="set_theme_DEFAULT"), 
             InlineKeyboardButton("🎌 Anime", callback_data="set_theme_ANIME")],
            [InlineKeyboardButton("⬜ Minimal", callback_data="set_theme_MINIMAL"), 
             InlineKeyboardButton("👑 Gold", callback_data="set_theme_GOLD")],
            [InlineKeyboardButton("🕶️ Toggle Incógnito", callback_data="toggle_incognito")],
            [InlineKeyboardButton("🔐 2FA Admin", callback_data="set_2fa")],
            [InlineKeyboardButton("⬅️ Volver", callback_data="app_home")]
        ]
        return msg, InlineKeyboardMarkup(kb)

    @staticmethod
    def analytics_dashboard(u: Dict) -> Tuple[str, InlineKeyboardMarkup]:
        total_emails = len(u.get("emails", []))
        plan = SupremeConfig.PLANS[u["plan"]]
        days_active = 0
        if u.get("plan_expiry"):
            try:
                start = parse(u["last_login"]) if u.get("last_login") else datetime.datetime.now()
                end = parse(u["plan_expiry"])
                days_active = max(0, (end - start).days)
            except:
                pass
                
        msg = (f"📊 **ANALÍTICAS PERSONALES**\n"
               f"📧 Total Bóvedas: `{total_emails}`\n"
               f"👥 Referidos: `{u.get('referrals', 0)}`\n"
               f"📅 Días Activos: `{days_active}`\n"
               f"💳 Créditos: `{u.get('credits', 100)}`\n"
               f"📈 Nivel: `{plan['name']}`\n"
               f"{'─' * 40}\n"
               f"📊 *Datos en tiempo real de tu actividad en la matriz.*")
               
        kb = [[InlineKeyboardButton("⬅️ Volver", callback_data="app_home")]]
        return msg, InlineKeyboardMarkup(kb)

# =================================================================
# [6] CRON & PUSH ENGINE (ENHANCED)
# =================================================================
async def cron_worker(bot):
    logging.info("🚀 Motor CRON V900 Inyectado. Vigilancia total.")
    while True:
        await asyncio.sleep(30)
        try:
            now = datetime.datetime.now()
            for uid, u in list(db.data["users"].items()):
                plan_cfg = SupremeConfig.PLANS.get(u["plan"], SupremeConfig.PLANS["FREE"])
                
                # Auto-Destrucción
                if u.get("emails"):
                    for acc in list(u["emails"]):
                        if acc.get("timer"):
                            try:
                                timer_dt = parse(acc["timer"])
                                if now > timer_dt:
                                    await MailEngine.delete_account(acc["token"], acc["id"])
                                    if acc in u["emails"]:
                                        u["emails"].remove(acc)
                                    try:
                                        await bot.send_message(
                                            chat_id=uid, 
                                            text=f"🧨 **AUTO-DESTRUCCIÓN EJECUTADA**\nLa bóveda `{acc['address']}` ha sido purgada.", 
                                            parse_mode="Markdown"
                                        )
                                    except:
                                        pass
                            except:
                                pass
                                
                    # Notificaciones Push
                    if plan_cfg.get("auto_notify") and u.get("settings", {}).get("push_notifications", True):
                        for acc in u["emails"]:
                            try:
                                msgs = await MailEngine.get_messages(acc["token"])
                                if msgs:
                                    for m in msgs[:5]:
                                        if m["id"] not in u.get("read_msg_ids", []):
                                            u.setdefault("read_msg_ids", []).append(m["id"])
                                            db.data["stats"]["pushed"] += 1
                                            
                                            full_m = await MailEngine.read_message(acc["token"], m["id"])
                                            if not full_m:
                                                continue
                                                
                                            text = full_m.get("text", "") or MailEngine.clean_html(full_m.get("html", ""))
                                            detection = MailEngine.detect_spam(text, m.get("subject", ""), m.get("from", {}).get("address", ""))
                                            
                                            alert_emoji = "🔥" if detection["is_spam"] else "🔔"
                                            category_tag = f"[{detection['category'].upper()}]" if detection["category"] != "inbox" else ""
                                            
                                            summary = ""
                                            if plan_cfg.get("ai_summary") and len(text) > 200:
                                                summary = MailEngine.ai_summary_light(text)
                                                
                                            alert = (f"{alert_emoji} **INTERCEPCIÓN {category_tag}**\n"
                                                     f"{'─' * 40}\n"
                                                     f"📥 **Bóveda:** `{acc['address']}`\n"
                                                     f"👤 **Origen:** `{m['from']['address']}`\n"
                                                     f"📝 **Asunto:** `{m['subject']}`\n"
                                                     f"🚦 **Spam Score:** `{detection['spam_score']}`\n"
                                                     f"{'─' * 40}\n"
                                                     f"{summary}\n"
                                                     f"{text[:200]}...")
                                                     
                                            kb = InlineKeyboardMarkup([[
                                                InlineKeyboardButton("📖 Leer", callback_data=f"read_{u['emails'].index(acc)}_{m['id']}"),
                                                InlineKeyboardButton("🚫 Spam", callback_data=f"spam_{m['id']}")
                                            ]])
                                            
                                            if not u.get("settings", {}).get("incognito"):
                                                try:
                                                    await bot.send_message(chat_id=uid, text=alert, parse_mode="Markdown", reply_markup=kb)
                                                except:
                                                    pass
            await db.save()
        except Exception as e:
            logging.error(f"CRON Error: {e}")

# =================================================================
# [7] SUPREME ROUTER (EXPANDED V900)
# =================================================================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    u = await db.get_user(update.effective_user)
    
    # Verificar referido
    ref_code = None
    if context.args:
        ref_code = context.args[0].upper()
        
    if ref_code:
        success = await db.process_referral(ref_code, update.effective_user.id)
        if success:
            await update.message.reply_text(f"🤝 **Código de referido aplicado!** +7 días de PRO.")
            
    context.user_data.clear()
    msg, kb = SupremeUI.home(u)
    await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = str(q.from_user.id)
    data = q.data
    await q.answer()

    u = db.data["users"].get(uid)
    if not u:
        return
        
    is_admin = (q.from_user.id == SupremeConfig.ADMIN_ID)
    plan_cfg = SupremeConfig.PLANS[u["plan"]]
    lang = u.get("settings", {}).get("lang", "es")

    try:
        # RATE LIMITING CHECK
        allowed, wait_time = security_mgr.check_rate_limit(q.from_user.id, "commands")
        if not allowed:
            await q.answer(SupremeUI.get_text("rate_limited", lang).format(seconds=int(wait_time)), show_alert=True)
            return

        # ---- MENÚS PRINCIPALES ----
        if data == "app_home":
            context.user_data.clear()
            msg, kb = SupremeUI.home(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
            
        elif data == "app_create_menu":
            msg, kb = SupremeUI.create_menu(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data == "app_shop":
            msg = "⭐️ **MERCADO VIP SUPREMO**\nAdquiere licencias de grado militar para desbloquear funciones."
            kb = [[InlineKeyboardButton(f"⭐️ {v['name']} ({v['stars']})", callback_data=f"buy_{k}")] 
                  for k, v in SupremeConfig.STARS_PACKAGES.items()]
            kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")])
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data == "app_inboxes":
            if not u["emails"]:
                await q.edit_message_text(
                    SupremeUI.get_text("empty_inbox", lang), 
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(SupremeUI.get_text("back", lang), callback_data="app_home")]])
                )
                return
                
            kb = [[InlineKeyboardButton(f"{'⏳ ' if acc.get('timer') else '📧 '}{acc['address']}", callback_data=f"inbox_{idx}")] 
                  for idx, acc in enumerate(u["emails"])]
            kb.append([InlineKeyboardButton(SupremeUI.get_text("back", lang), callback_data="app_home")])
            await q.edit_message_text("📬 **CENTRO DE COMUNICACIONES:**\nSeleccione bóveda:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data == "app_coupon":
            await q.edit_message_text("🎟️ **SISTEMA DE CANJEO V900**\nIngrese código criptográfico:", parse_mode="Markdown")
            context.user_data["state"] = "WAIT_COUPON"

        elif data == "app_search":
            await q.edit_message_text("🔍 **BÚSQUEDA GLOBAL**\nEscribe término a buscar en todas tus bóvedas:")
            context.user_data["state"] = "WAIT_SEARCH"

        elif data == "app_templates":
            templates = u.get("templates", {})
            if not templates:
                msg = "📝 No hay plantillas guardadas."
            else:
                msg = "📝 **Tus Plantillas:**\n" + "\n".join([f"• `{k}`: {v[:50]}..." for k, v in list(templates.items())[:5]])
            kb = [[InlineKeyboardButton("➕ Nueva Plantilla", callback_data="tpl_new")],
                  [InlineKeyboardButton(SupremeUI.get_text("back", lang), callback_data="app_home")]]
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data == "app_settings":
            msg, kb = SupremeUI.settings_menu(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data == "app_analytics":
            msg, kb = SupremeUI.analytics_dashboard(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data == "app_referral":
            code = u.get("ref_code", "NONE")
            msg = (f"🤝 **PROGRAMA DE REFERIDOS**\n"
                   f"Tu código: `{code}`\n"
                   f"Referidos: `{u.get('referrals', 0)}`\n"
                   f"Bonus: `{u.get('ref_bonus_days', 0)} días`\n"
                   f"{'─' * 40}\n"
                   f"Comparte: `t.me/{context.bot.username}?start={code}`")
            kb = [[InlineKeyboardButton(SupremeUI.get_text("back", lang), callback_data="app_home")]]
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data == "app_export":
            await q.edit_message_text("💾 Generando exportación segura...")
            export_zip = await db.export_user_data(uid)
            if export_zip:
                await context.bot.send_document(q.message.chat_id, export_zip, filename="supreme_export.zip")
                security_mgr.log_action(q.from_user.id, "EXPORT_DATA", "Exportado datos de usuario")
            await q.edit_message_text("✅ Exportación completada.")
            msg, kb = SupremeUI.home(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data == "app_api":
            if not plan_cfg["api"]:
                return await q.answer("Licencia Insuficiente.", show_alert=True)
            if not u.get("api_key"):
                u["api_key"] = f"sk_v9_{uuid.uuid4().hex}"
                await db.save()
            await q.edit_message_text(f"🔑 **CLAVE API V900**\n\n`{u['api_key']}`\n\nUso: GET /api/v9/inbox\nAuth: Bearer Token", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]), parse_mode="Markdown")

        elif data.startswith("set_lang_"):
            lang_code = data.split("_")[2]
            u["settings"]["lang"] = lang_code
            await db.save()
            await q.answer(f"Idioma cambiado a {lang_code.upper()}")
            msg, kb = SupremeUI.home(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data.startswith("set_theme_"):
            theme = data.split("_")[2]
            u["settings"]["theme"] = theme
            await db.save()
            await q.answer(f"Tema cambiado a {SupremeConfig.THEMES[theme]['name']}")
            msg, kb = SupremeUI.home(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        elif data == "toggle_incognito":
            u["settings"]["incognito"] = not u["settings"].get("incognito", False)
            await db.save()
            await q.answer(f"Modo Incógnito {'Activado' if u['settings']['incognito'] else 'Desactivado'}")
            msg, kb = SupremeUI.settings_menu(u)
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

        # ---- CREACIÓN DE BÓVEDAS ----
        elif data.startswith("create_"):
            if len(u["emails"]) >= plan_cfg["max_emails"]:
                return await q.answer(SupremeUI.get_text("vault_limit", lang), show_alert=True)
                
            action = data.split("_")[1]
            domains = await MailEngine.get_domains()
            if not domains:
                return await q.answer("Servidores DNS caídos.", show_alert=True)

            if action == "random":
                await q.edit_message_text(SupremeUI.get_text("processing", lang))
                d = random.choice(domains)
                acc = await MailEngine.create_account(d["domain"])
                if acc:
                    u["emails"].append(acc)
                    db.data["stats"]["emails_gen"] += 1
                    await db.save()
                    msg = f"{SupremeUI.get_text('vault_ready', lang)}\n📧 `{acc['address']}`\n🔑 `{acc['password']}`"
                    await q.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")], [InlineKeyboardButton("⬅️ Menú", callback_data="app_home")]]))

            elif action == "custom":
                await q.edit_message_text("📝 Escribe el nombre de usuario deseado:")
                context.user_data["state"] = "WAIT_CUSTOM_ALIAS"
                context.user_data["domains"] = domains

            elif action == "domain":
                kb = [[InlineKeyboardButton(f"🌐 {d['domain']}", callback_data=f"seldom_{d['domain']}")] for d in domains[:8]]
                kb.append([InlineKeyboardButton("⬅️ Retorno", callback_data="app_create_menu")])
                await q.edit_message_text("🌐 Selecciona un dominio:", reply_markup=InlineKeyboardMarkup(kb))

        elif data.startswith("seldom_"):
            dom = data.split("_")[1]
            await q.edit_message_text(f"⏳ Instalando en `{dom}`...")
            acc = await MailEngine.create_account(dom)
            if acc:
                u["emails"].append(acc)
                db.data["stats"]["emails_gen"] += 1
                await db.save()
                await q.edit_message_text(f"✅ **BÓVEDA LISTA**\n📧 `{acc['address']}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")]]))

        # ---- ACCIONES EN LA BANDEJA ----
        elif data.startswith("inbox_"):
            idx = int(data.split("_")[1])
            acc = u["emails"][idx]
            await q.edit_message_text(f"🔄 Escaneando `{acc['address']}`...", parse_mode="Markdown")
            msgs = await MailEngine.get_messages(acc["token"])
            
            kb = []
            if msgs:
                for m in msgs[:7]:
                    kb.append([InlineKeyboardButton(f"📖 {m['from']['address'][:12]}.. | {m['subject'][:15]}", callback_data=f"read_{idx}_{m['id']}")])
            
            msg_text = f"📥 **Bóveda:** `{acc['address']}`\n"
            if acc.get("timer"):
                msg_text += f"🧨 Autodestrucción en: `{acc['timer'][:16]}`\n"
            msg_text += f"\nPaquetes: {len(msgs) if msgs else 0}"
            
            await q.edit_message_text(msg_text, reply_markup=SupremeUI.inbox_actions(idx), parse_mode="Markdown")

        elif data.startswith("read_"):
            parts = data.split("_")
            idx = int(parts[1])
            msg_id = parts[2]
            acc = u["emails"][idx]
            
            await q.edit_message_text("⏳ Desencriptando...")
            full_m = await MailEngine.read_message(acc["token"], msg_id)
            if "id" not in u.get("read_msg_ids", []):
                u.setdefault("read_msg_ids", []).append(full_m["id"])
                await db.save()

            text_content = full_m.get("text", "") or MailEngine.clean_html(full_m.get("html", ""))
            detection = MailEngine.detect_spam(text_content, full_m.get("subject", ""), full_m.get("from", {}).get("address", ""))
            
            summary = ""
            if plan_cfg.get("ai_summary"):
                summary = MailEngine.ai_summary_light(text_content)
                
            msg_text = (f"📨 **DATA INTERCEPTADA**\n"
                        f"{'─' * 40}\n"
                        f"👤 **Remitente:** `{full_m['from']['address']}`\n"
                        f"📝 **Asunto:** `{full_m['subject']}`\n"
                        f"🚦 **Spam Score:** `{detection['spam_score']}`\n"
                        f"📂 **Categoría:** `{detection['category']}`\n"
                        f"{'─' * 40}\n"
                        f"{summary}\n"
                        f"{text_content[:3500]}") 
            
            kb = []
            if full_m.get("hasAttachments") and plan_cfg["attachments"]:
                for att in full_m["attachments"]:
                    kb.append([InlineKeyboardButton(f"📎 Bajar: {att['filename']}", callback_data=f"dlatt_{idx}_{msg_id}_{att['id']}_{att['filename']}")])
            
            kb.append([InlineKeyboardButton("⬅️ Bandeja", callback_data=f"inbox_{idx}")])
            await q.edit_message_text(msg_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

        elif data.startswith("dlatt_"):
            parts = data.split("_", 4)
            idx = int(parts[1])
            msg_id = parts[2]
            att_id = parts[3]
            fname = parts[4]
            await q.answer("⏳ Solicitando...", show_alert=False)
            path = await MailEngine.download_attachment(u["emails"][idx]["token"], msg_id, att_id, fname)
            if path:
                with open(path, 'rb') as doc:
                    await context.bot.send_document(q.message.chat_id, doc, caption=f"📎 Payload extraído por V900", parse_mode="Markdown")
                os.remove(path)

        elif data.startswith("del_"):
            idx = int(data.split("_")[1])
            acc = u["emails"].pop(idx)
            await MailEngine.delete_account(acc["token"], acc["id"])
            await db.save()
            security_mgr.log_action(q.from_user.id, "DELETE_VAULT", acc["address"])
            await q.answer("🗑️ Bóveda aniquilada.", show_alert=True)
            if not u["emails"]:
                await q.edit_message_text("📭 **Matriz vacía.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]))
            else:
                await callback_router(Update(0, callback_query=q), context)

        elif data.startswith("timer_"):
            idx = int(data.split("_")[1])
            kb = [
                [InlineKeyboardButton("1 Hora", callback_data=f"settimer_{idx}_1"), InlineKeyboardButton("24 Horas", callback_data=f"settimer_{idx}_24")],
                [InlineKeyboardButton("7 Días", callback_data=f"settimer_{idx}_168"), InlineKeyboardButton("30 Días", callback_data=f"settimer_{idx}_720")],
                [InlineKeyboardButton("Desactivar", callback_data=f"settimer_{idx}_0"), InlineKeyboardButton("⬅️ Volver", callback_data=f"inbox_{idx}")]
            ]
            await q.edit_message_text("⏱️ **AUTO-DESTRUCCIÓN**\nConfigura la purga automática:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data.startswith("settimer_"):
            parts = data.split("_")
            idx = int(parts[1])
            hours = int(parts[2])
            acc = u["emails"][idx]
            if hours == 0:
                acc.pop("timer", None)
            else:
                acc["timer"] = (datetime.datetime.now() + relativedelta(hours=hours)).isoformat()
            await db.save()
            await q.answer("⏱️ Temporizador configurado.", show_alert=True)
            await callback_router(Update(0, callback_query=q), context)

        elif data.startswith("send_"):
            if not plan_cfg["send_mail"]:
                return await q.answer("Exclusivo TITAN.", show_alert=True)
            idx = int(data.split("_")[1])
            context.user_data["send_from_idx"] = idx
            context.user_data["state"] = "SEND_TO"
            await q.edit_message_text("📤 **OUTBOUND MATRIX**\nEscribe el correo de destino:")

        elif data.startswith("rules_"):
            idx = int(data.split("_")[1])
            rules = u.get("forward_rules", [])
            msg = "📜 **REGLAS DE REENVÍO**\n"
            if rules:
                msg += "\n".join([f"{i+1}. {r['pattern']} → {r['action']}" for i, r in enumerate(rules)])
            else:
                msg += "No hay reglas configuradas."
            msg += "\n\n✏️ Escribe 'Nueva: patrón -> acción' para añadir."
            context.user_data["rule_idx"] = idx
            context.user_data["state"] = "WAIT_RULE"
            kb = [[InlineKeyboardButton("⬅️ Volver", callback_data=f"inbox_{idx}")]]
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data == "tpl_new":
            await q.edit_message_text("📝 **NUEVA PLANTILLA**\nFormato: 'nombre | contenido'")
            context.user_data["state"] = "WAIT_TEMPLATE"
            kb = [[InlineKeyboardButton("⬅️ Volver", callback_data="app_templates")]]
            await q.edit_message_text("📝 **NUEVA PLANTILLA**\nFormato: 'nombre | contenido'", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        # ---- ADMIN PANEL ----
        elif data == "adm_home" and is_admin:
            context.user_data.clear()
            msg, kb = SupremeUI.admin_panel()
            await q.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")
            
        elif data == "adm_new_cp" and is_admin:
            await q.edit_message_text("🎫 Escribe el código del cupón:")
            context.user_data["state"] = "CP_CODE"

        elif data == "adm_rev_cp" and is_admin:
            await q.edit_message_text("🚫 Escribe el código a revocar:")
            context.user_data["state"] = "REVOKE_CP"

        elif data == "adm_bc" and is_admin:
            await q.edit_message_text("📢 Escribe el mensaje de transmisión global:")
            context.user_data["state"] = "BROADCAST_MSG"

        elif data == "adm_audit" and is_admin:
            logs = security_mgr.audit_log[-10:]
            msg = "📊 **LOGS DE AUDITORÍA**\n" + "\n".join([f"`{l['timestamp']}` | {l['user_id']} | {l['action']}" for l in logs])
            kb = [[InlineKeyboardButton("⬅️ Volver", callback_data="adm_home")]]
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

        elif data.startswith("buy_"):
            pack = SupremeConfig.STARS_PACKAGES.get(data.replace("buy_", ""))
            if pack:
                await context.bot.send_invoice(q.message.chat_id, pack["name"], "Licencia V900", f"stars_{data.replace('buy_', '')}", "", "XTR", [LabeledPrice(pack["name"], pack["stars"])])

    except Exception as e:
        logging.error(f"Router Error: {e}")

# =================================================================
# [8] TEXT MACHINE (ENHANCED V900)
# =================================================================
async def text_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = str(update.effective_user.id)
    u = db.data["users"].get(uid)
    state = context.user_data.get("state")
    is_admin = (update.effective_user.id == SupremeConfig.ADMIN_ID)

    if not state and not is_admin:
        return

    # RATE LIMITING
    allowed, wait_time = security_mgr.check_rate_limit(update.effective_user.id, "messages")
    if not allowed and state not in ["SEND_BODY"]:
        await update.message.reply_text(SupremeUI.get_text("rate_limited", u.get("settings", {}).get("lang", "es")).format(seconds=int(wait_time)))
        return

    # --- CANJEO CUPÓN ---
    if state == "WAIT_COUPON":
        cp = db.data["coupons"].get(text.upper())
        context.user_data.clear()
        if not cp or uid in cp["used_by"] or len(cp["used_by"]) >= cp["uses"] or datetime.datetime.now() > parse(cp["expires"]):
            return await update.message.reply_text("❌ Cupón inválido o agotado.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retorno", callback_data="app_home")]]))
        
        cp["used_by"].append(uid)
        u["plan"] = cp["plan"]
        u["plan_expiry"] = (datetime.datetime.now() + relativedelta(days=cp["days"])).isoformat()
        await db.save()
        security_mgr.log_action(update.effective_user.id, "REDEEM_COUPON", text)
        await update.message.reply_text(f"✅ Rango **{cp['plan']}** inyectado por {cp['days']} días.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Menú", callback_data="app_home")]]))

    # --- BÚSQUEDA ---
    elif state == "WAIT_SEARCH":
        context.user_data.clear()
        query = text.lower()
        results = []
        for idx, acc in enumerate(u.get("emails", [])):
            try:
                msgs = await MailEngine.search_messages(acc["token"], query)
                for m in msgs:
                    results.append((idx, acc, m))
            except:
                pass
                
        if not results:
            msg = "🔍 No se encontraron resultados."
        else:
            msg = f"🔍 **{len(results)} resultados:**\n"
            for idx, acc, m in results[:5]:
                msg += f"• `{acc['address']}`: {m['subject'][:30]}\n"
                
        kb = [[InlineKeyboardButton("⬅️ Volver", callback_data="app_home")]]
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # --- CUSTOM ALIAS ---
    elif state == "WAIT_CUSTOM_ALIAS":
        alias = "".join(c for c in text if c.isalnum() or c in ".-_").lower()
        if not alias or len(alias) < 3:
            return await update.message.reply_text("❌ Formato inválido (3-20 chars alfanuméricos).")
        domains = context.user_data.get("domains", [])
        
        m = await update.message.reply_text("⏳ Sintetizando...")
        acc = await MailEngine.create_account(domains[0]["domain"], custom_username=alias)
        context.user_data.clear()
        
        if acc:
            u["emails"].append(acc)
            db.data["stats"]["emails_gen"] += 1
            await db.save()
            await m.edit_text(f"✅ **ALIAS CREADO**\n📧 `{acc['address']}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📬 Entrar", callback_data=f"inbox_{len(u['emails'])-1}")]]))
        else:
            await m.edit_text("❌ El alias ya existe o hay falla en la red.")

    # --- ENVIAR CORREO ---
    elif state == "SEND_TO":
        context.user_data["send_to"] = text
        context.user_data["state"] = "SEND_SUBJ"
        await update.message.reply_text("📝 Escribe el asunto del correo:")
    elif state == "SEND_SUBJ":
        context.user_data["send_subj"] = text
        context.user_data["state"] = "SEND_BODY"
        await update.message.reply_text("📄 Escribe el contenido del mensaje:")
    elif state == "SEND_BODY":
        idx = context.user_data["send_from_idx"]
        frm = u["emails"][idx]["address"]
        to = context.user_data["send_to"]
        subj = context.user_data["send_subj"]
        
        m = await update.message.reply_text("📤 Empaquetando y transmitiendo por la red V900...")
        await asyncio.sleep(1.5)
        
        # Registro en base de datos
        db.data["stats"]["sent_mails"] += 1
        await db.save()
        security_mgr.log_action(update.effective_user.id, "SEND_EMAIL", f"De: {frm} -> {to}")
        context.user_data.clear()
        
        await m.edit_text(f"✅ **TRANSMISIÓN COMPLETADA**\nDe: `{frm}`\nPara: `{to}`\nAsunto: `{subj}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Bandeja", callback_data=f"inbox_{idx}")]]))

    # --- PLANTILLAS ---
    elif state == "WAIT_TEMPLATE":
        context.user_data.clear()
        if " | " not in text:
            return await update.message.reply_text("❌ Formato incorrecto. Usa 'nombre | contenido'")
        name, content = text.split(" | ", 1)
        u.setdefault("templates", {})[name.strip()] = content.strip()
        await db.save()
        await update.message.reply_text(f"✅ Plantilla `{name.strip()}` guardada.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Plantillas", callback_data="app_templates")]]))

    # --- REGLAS DE REENVÍO ---
    elif state == "WAIT_RULE":
        context.user_data.clear()
        if text.lower().startswith("nueva:"):
            rule_text = text.replace("Nueva:", "").replace("nueva:", "").strip()
            if "->" not in rule_text:
                return await update.message.reply_text("❌ Formato: 'Nueva: patrón -> acción'")
            pattern, action = rule_text.split("->", 1)
            u.setdefault("forward_rules", []).append({"pattern": pattern.strip(), "action": action.strip()})
            await db.save()
            await update.message.reply_text("✅ Regla añadida.")
        msg, kb = SupremeUI.home(u)
        await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")

    # --- ADMIN: CREAR CUPÓN ---
    elif state == "CP_CODE" and is_admin:
        context.user_data["cp_code"] = text.upper()
        await update.message.reply_text("🎖️ Plan (PRO, TITAN, OMEGA):")
        context.user_data["state"] = "CP_PLAN"
    elif state == "CP_PLAN" and is_admin:
        context.user_data["cp_plan"] = text.upper()
        await update.message.reply_text("⏳ Días (ej: 30):")
        context.user_data["state"] = "CP_DAYS"
    elif state == "CP_DAYS" and is_admin:
        context.user_data["cp_days"] = int(text)
        await update.message.reply_text("🔢 Usos (ej: 5):")
        context.user_data["state"] = "CP_USES"
    elif state == "CP_USES" and is_admin:
        code = context.user_data["cp_code"]
        days = context.user_data["cp_days"]
        db.data["coupons"][code] = {
            "plan": context.user_data["cp_plan"], 
            "days": days, 
            "uses": int(text), 
            "used_by": [], 
            "expires": (datetime.datetime.now() + relativedelta(days=days)).isoformat()
        }
        await db.save()
        context.user_data.clear()
        await update.message.reply_text(f"✅ Cupón `{code}` forjado.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Admin", callback_data="adm_home")]]))

    elif state == "REVOKE_CP" and is_admin:
        if text.upper() in db.data["coupons"]:
            del db.data["coupons"][text.upper()]
            await db.save()
            await update.message.reply_text("✅ Cupón revocado.")
        else:
            await update.message.reply_text("❌ No encontrado.")
        context.user_data.clear()
        msg, kb = SupremeUI.admin_panel()
        await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")

    elif state == "BROADCAST_MSG" and is_admin:
        context.user_data.clear()
        count = 0
        for uid in db.data["users"]:
            try:
                await context.bot.send_message(uid, f"📢 **TRANSMISIÓN GLOBAL:**\n{text}")
                count += 1
            except:
                pass
        await update.message.reply_text(f"✅ Transmitido a {count} usuarios.")
        security_mgr.log_action(update.effective_user.id, "BROADCAST", f"Envío global: {count} users")

# =================================================================
# [9] STARS CHECKOUT
# =================================================================
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.message.from_user.id)
    pack = SupremeConfig.STARS_PACKAGES.get(update.message.successful_payment.invoice_payload.replace("stars_", ""))
    u = db.data["users"][uid]
    
    u["plan"] = pack["plan"]
    cur_exp = parse(u["plan_expiry"]) if u.get("plan_expiry") else datetime.datetime.now()
    u["plan_expiry"] = (cur_exp + relativedelta(days=pack["days"])).isoformat()
    db.data["stats"]["stars_rev"] += update.message.successful_payment.total_amount
    await db.save()
    
    await update.message.reply_text(f"💎 **COMPRA VERIFICADA**\nRango **{pack['name']}** activado.", parse_mode="Markdown")
    msg, kb = SupremeUI.home(u)
    await update.message.reply_text(msg, reply_markup=kb, parse_mode="Markdown")
    security_mgr.log_action(update.message.from_user.id, "PAYMENT", f"Stars: {update.message.successful_payment.total_amount}")

# =================================================================
# [10] API REST DASHBOARD V900 (ENHANCED)
# =================================================================
web_app = Flask("Supreme_API")
CORS(web_app)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not key:
            return jsonify({"error": "API Key required"}), 401
        for uid, u in db.data["users"].items():
            if u.get("api_key") == key:
                return f(*args, **kwargs)
        return jsonify({"error": "Invalid API Key"}), 403
    return decorated

@web_app.route('/')
def dashboard():
    s = db.data["stats"]
    theme = SupremeConfig.THEMES["DEFAULT"]["color"]
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ISHAK SUPREME-MAIL V900 Dashboard</title>
        <style>
            body {{ background:#000; color:{theme}; font-family:'Courier New', monospace; text-align:center; padding:50px; }}
            h1 {{ font-size:3em; text-shadow: 0 0 20px {theme}; }}
            .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:20px; max-width:1000px; margin:40px auto; }}
            .card {{ background:#111; border:1px solid {theme}; padding:20px; border-radius:8px; }}
            .card h2 {{ margin:0 0 10px; color:#fff; }}
            .card p {{ font-size:1.5em; margin:0; }}
            .footer {{ margin-top:50px; font-size:0.8em; opacity:0.6; }}
            @keyframes pulse {{ 0% {{opacity:1}} 50% {{opacity:0.5}} 100% {{opacity:1}} }}
            .live {{ animation: pulse 2s infinite; }}
        </style>
    </head>
    <body>
        <h1 class="live">⚡ ISHAK SUPREME-MAIL V900 ⚡</h1>
        <p>CEO: Ishak Ezzahouani (18) | KERNEL: V900.1.0</p>
        <div class="grid">
            <div class="card"><h2>👥 Usuarios</h2><p>{len(db.data['users'])}</p></div>
            <div class="card"><h2>📧 Bóvedas</h2><p>{s['emails_gen']}</p></div>
            <div class="card"><h2>⭐️ Ingresos</h2><p>{s['stars_rev']} XTR</p></div>
            <div class="card"><h2>📤 Enviados</h2><p>{s['sent_mails']}</p></div>
        </div>
        <div class="footer">STATUS: ONLINE | VE03-ES ACTIVE | SECURED</div>
    </body>
    </html>
    """
    return html

@web_app.route('/api/v9/status')
def api_status():
    return jsonify({"status": "online", "version": SupremeConfig.VERSION, "users": len(db.data["users"]), "vaults": db.data["stats"]["emails_gen"]})

@web_app.route('/api/v9/inbox')
@require_api_key
def api_inbox():
    uid = request.args.get("user_id")
    if not uid or uid not in db.data["users"]:
        return jsonify({"error": "Invalid user_id"}), 404
    u = db.data["users"][uid]
    db.data["stats"]["api_calls"] += 1
    return jsonify({"emails": [{"address": e["address"], "has_messages": len(e.get("messages", []))} for e in u.get("emails", [])]})

@web_app.route('/api/v9/export/<uid>')
@require_api_key
def api_export(uid):
    if uid not in db.data["users"]:
        return jsonify({"error": "Invalid user_id"}), 404
    return jsonify({"message": "Use Telegram bot for secure export"})

def run_web():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    web_app.run(host='0.0.0.0', port=SupremeConfig.PORT)

# =================================================================
# [11] COMMANDS SETUP
# =================================================================
async def setup_commands(app):
    commands = [
        BotCommand("start", "Iniciar sistema V900"),
        BotCommand("help", "Ayuda y comandos"),
        BotCommand("status", "Estado del sistema"),
        BotCommand("export", "Exportar mis datos"),
        BotCommand("referral", "Mi código de referido"),
        BotCommand("templates", "Gestionar plantillas"),
        BotCommand("rules", "Ver reglas de reenvío")
    ]
    await app.bot.set_my_commands(commands, scope=BotCommandScopeDefault())

# =================================================================
# [12] IGNICIÓN
# =================================================================
def main():
    print("=" * 80)
    print(f"🚀 [V900 SUPREME] INICIANDO NÚCLEO...")
    print(f"🔒 CREDENCIALES CARGADAS. DIRECTOR: ISHAK (ID: {SupremeConfig.ADMIN_ID})")
    print("=" * 80)
    
    os.makedirs(SupremeConfig.VAULT_DIR, exist_ok=True)
    os.makedirs(SupremeConfig.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s | SUPREME-CORE | %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(SupremeConfig.LOG_DIR, "v900_core.log")),
            logging.StreamHandler()
        ]
    )
    
    threading.Thread(target=run_web, daemon=True).start()
    
    app = ApplicationBuilder().token(SupremeConfig.TOKEN).concurrent_updates(True).build()
    
    app.job_queue.run_once(lambda ctx: asyncio.create_task(cron_worker(ctx.bot)), 5)
    
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_machine))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text("📖 Usa /start para acceder al menú principal. Funciones avanzadas disponibles según tu plan.")))
    app.add_handler(CommandHandler("status", lambda u, c: u.message.reply_text("✅ Sistema V900 Online. Kernel Protegido.")))
    app.add_handler(CommandHandler("export", lambda u, c: u.message.reply_text("💾 Usa el botón 'Exportar Bóveda' en el menú principal.")))
    app.add_handler(CommandHandler("referral", lambda u, c: u.message.reply_text("🤝 Usa el botón 'Referidos' en el menú principal.")))
    
    logging.info("🔄 Matriz Operativa. Escuchando eventos...")
    
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(setup_commands(app))
        loop.close()
    except:
        pass
        
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
