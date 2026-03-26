#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║             Print3D Pro — Cotizador Profesional          ║
║                                                          ║
║  Instalar:  pip install customtkinter                    ║
║  Ejecutar:  python main.py                               ║
║                                                          ║
║  Archivos de datos (auto-generados junto al script):     ║
║    config.json   |  impresoras.json                      ║
║    materiales.json  |  ordenes.json                      ║
║                                                          ║
║  Logos de marcas (opcionales):                           ║
║    Coloca imágenes .png en:  assets/logos/               ║
║    Nombres esperados: bambu.png, creality.png,           ║
║    elegoo.png, anycubic.png, prusa.png, sunlu.png,       ║
║    esun.png, polymaker.png  (256×256 recomendado)        ║
╚══════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
import os
import sys

# ── Path setup ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ── Imports internos ─────────────────────────────────────────────
from data.constants  import DEFAULT_CONFIG
from data.store      import load, save
from themes.theme    import get_theme, THEMES
import modules.widgets as W

from modules.tab_dashboard  import DashboardTab
from modules.tab_cotizador  import CotizadorTab
from modules.tab_impresoras import ImpresorasTab
from modules.tab_materiales import MaterialesTab
from modules.tab_ventas     import VentasTab
from modules.tab_config     import ConfigTab


# ──────────────────────────────────────────────────────────────────
#  APP PRINCIPAL
# ──────────────────────────────────────────────────────────────────

class Print3DApp(ctk.CTk):
    def __init__(self):
        # ── Cargar datos antes de init ──
        self.config      = load("config",    dict(DEFAULT_CONFIG))
        self.printers    = load("printers",  [])
        self.materials   = load("materials", [])
        self.orders      = load("orders",    [])
        self.theme_mode  = self.config.get("tema", "dark")

        # ── Aplicar tema CTk ──
        theme = get_theme(self.theme_mode)
        ctk.set_appearance_mode(theme["ctk_mode"])
        ctk.set_default_color_theme(theme["ctk_theme"])

        super().__init__()

        # ── Init global widget theme ──
        W.set_theme(theme)

        # ── Ventana ──
        self.title("Print3D Pro")
        self.geometry("1340x820")
        self.minsize(1100, 680)
        self._set_window_icon()

        # ── Layout ──
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()
        self._create_tabs()

        # ── Pantalla inicial ──
        self.show("dashboard")

    # ─────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────

    def _build_sidebar(self):
        T = W.T
        self.sidebar = ctk.CTkFrame(self,
                                     width=220,
                                     fg_color=T("bg_sidebar"),
                                     corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # ── Logo / Marca ──
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(22, 6))

        ctk.CTkLabel(logo_frame,
                     text="⬡ Print3D Pro",
                     font=ctk.CTkFont("DM Sans", 20, "bold"),
                     text_color=W.T("accent")).pack(anchor="w")

        self.biz_name_label = ctk.CTkLabel(logo_frame,
                                            text=self.config.get("negocio", "Mi Taller 3D"),
                                            font=ctk.CTkFont("DM Sans", 11),
                                            text_color=W.T("text_sub"))
        self.biz_name_label.pack(anchor="w")

        # Separador
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color=W.T("border")).pack(fill="x", padx=10, pady=10)

        # ── Tabs ──
        self.tab_buttons = {}
        TABS = [
            ("dashboard",  "📊", "Dashboard"),
            ("cotizador",  "💰", "Cotizador"),
            ("impresoras", "🖨️", "Impresoras"),
            ("materiales", "🧵", "Materiales"),
            ("ventas",     "📦", "Ventas"),
            ("config",     "⚙️",  "Configuración"),
        ]

        for key, icon, label in TABS:
            b = ctk.CTkButton(
                self.sidebar,
                text=f"  {icon}  {label}",
                anchor="w",
                fg_color="transparent",
                text_color=W.T("text_sub"),
                hover_color=W.T("bg_hover"),
                font=ctk.CTkFont("DM Sans", 13),
                corner_radius=8,
                height=40,
                command=lambda k=key: self.show(k),
            )
            b.pack(fill="x", padx=10, pady=2)
            self.tab_buttons[key] = b

        # ── Spacer ──
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(
            fill="both", expand=True)

        # ── Separador inferior ──
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color=W.T("border")).pack(fill="x", padx=10, pady=6)

        # ── Tema Toggle (Sol / Luna) ──
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(fill="x", padx=14, pady=(0, 8))

        icon_lbl = ctk.CTkLabel(theme_frame,
                                 text="🌙" if self.theme_mode == "dark" else "☀️",
                                 font=ctk.CTkFont("DM Sans", 18),
                                 width=32)
        icon_lbl.pack(side="left")
        self._theme_icon_lbl = icon_lbl

        ctk.CTkLabel(theme_frame,
                     text="Tema oscuro" if self.theme_mode == "dark" else "Tema claro",
                     font=ctk.CTkFont("DM Sans", 11),
                     text_color=W.T("text_sub")).pack(side="left", padx=6)

        self._theme_toggle = ctk.CTkSwitch(
            theme_frame,
            text="",
            command=self._toggle_theme,
            progress_color=W.T("accent"),
            button_color=W.T("accent"),
            width=46,
            onvalue=True, offvalue=False,
        )
        self._theme_toggle.pack(side="right")
        if self.theme_mode == "dark":
            self._theme_toggle.select()

        # ── Versión ──
        ctk.CTkLabel(self.sidebar,
                     text="v2.0 · Print3D Pro",
                     font=ctk.CTkFont("DM Sans", 9),
                     text_color=W.T("text_dim")).pack(pady=(0, 10))

    # ─────────────────────────────────────────────────────────
    # CONTENT AREA
    # ─────────────────────────────────────────────────────────

    def _build_content(self):
        self.container = ctk.CTkFrame(self, fg_color=W.T("bg"), corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")

    def _create_tabs(self):
        self.frames = {
            "dashboard":  DashboardTab(self.container, self),
            "cotizador":  CotizadorTab(self.container, self),
            "impresoras": ImpresorasTab(self.container, self),
            "materiales": MaterialesTab(self.container, self),
            "ventas":     VentasTab(self.container, self),
            "config":     ConfigTab(self.container, self),
        }
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ─────────────────────────────────────────────────────────
    # NAVEGACIÓN
    # ─────────────────────────────────────────────────────────

    def show(self, name: str):
        frame = self.frames.get(name)
        if not frame:
            return

        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

        # Actualizar sidebar
        for k, btn in self.tab_buttons.items():
            if k == name:
                btn.configure(
                    fg_color=W.T("bg_selected"),
                    text_color=W.T("accent"),
                    border_width=0,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=W.T("text_sub"),
                )

    # ─────────────────────────────────────────────────────────
    # TEMA
    # ─────────────────────────────────────────────────────────

    def _toggle_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.config["tema"] = self.theme_mode
        self.save_config()

        # Actualizar icono
        self._theme_icon_lbl.configure(
            text="☀️" if self.theme_mode == "light" else "🌙")

        theme = get_theme(self.theme_mode)
        ctk.set_appearance_mode(theme["ctk_mode"])
        W.set_theme(theme)

        # Re-iniciar toda la UI
        self.toast("🎨 Tema cambiado — reiniciando UI…")
        self.after(400, self._full_rebuild)

    def _full_rebuild(self):
        """Reconstruye toda la UI con el nuevo tema."""
        # Destruir sidebar y contenido
        self.sidebar.destroy()
        self.container.destroy()

        # Rebuild
        self._build_sidebar()
        self._build_content()
        self._create_tabs()
        self.show("dashboard")

    # ─────────────────────────────────────────────────────────
    # PERSISTENCIA
    # ─────────────────────────────────────────────────────────

    def save_config(self):
        save("config", self.config)

    def save_printers(self):
        save("printers", self.printers)

    def save_materials(self):
        save("materials", self.materials)

    def save_orders(self):
        save("orders", self.orders)

    # ─────────────────────────────────────────────────────────
    # TOAST
    # ─────────────────────────────────────────────────────────

    def toast(self, msg: str, ok: bool = True):
        W.Toast(self, msg, ok)

    # ─────────────────────────────────────────────────────────
    # ICON
    # ─────────────────────────────────────────────────────────

    def _set_window_icon(self):
        """Intenta poner un ícono a la ventana."""
        try:
            icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass


# ──────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = Print3DApp()
    app.mainloop()
