#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║             Print3D Pro — Cotizador Profesional          ║
║  Instalar:  pip install customtkinter                    ║
║  Ejecutar:  python main.py                               ║
╚══════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from data.constants  import DEFAULT_CONFIG
from data.store      import load, save
from themes.theme    import get_theme
import modules.widgets as W

from modules.tab_dashboard  import DashboardTab
from modules.tab_cotizador  import CotizadorTab
from modules.tab_impresoras import ImpresorasTab
from modules.tab_materiales import MaterialesTab
from modules.tab_ventas     import VentasTab
from modules.tab_config     import ConfigTab


class Print3DApp(ctk.CTk):
    def __init__(self):
        # ── Cargar datos ──
        # BUG FIX: se renombra internamente como _cfg para evitar colisión
        # con self.config() que es un método heredado de CTk
        raw_cfg         = load("config", dict(DEFAULT_CONFIG))
        self._app_cfg   = {**DEFAULT_CONFIG, **raw_cfg}   # merge seguro con defaults
        self.printers   = load("printers",  [])
        self.materials  = load("materials", [])
        self.orders     = load("orders",    [])
        self.theme_mode = self._app_cfg.get("tema", "dark")

        # ── Aplicar tema CTk antes del super().__init__() ──
        theme = get_theme(self.theme_mode)
        ctk.set_appearance_mode(theme["ctk_mode"])
        ctk.set_default_color_theme(theme["ctk_theme"])

        super().__init__()

        W.set_theme(theme)

        self.title("Print3D Pro")
        self.geometry("1340x820")
        self.minsize(1100, 680)
        self._set_window_icon()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()
        self._create_tabs()
        self.show("dashboard")

    # ── Propiedad config para que los módulos usen app.config normalmente ──
    @property
    def config(self):
        return self._app_cfg

    @config.setter
    def config(self, value):
        self._app_cfg = value

    # ─────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220,
                                    fg_color=W.T("bg_sidebar"),
                                    corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)   # FIX: mantiene ancho fijo

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(22, 6))

        ctk.CTkLabel(logo_frame, text="⬡ Print3D Pro",
                     font=ctk.CTkFont("DM Sans", 20, "bold"),
                     text_color=W.T("accent")).pack(anchor="w")

        self.biz_name_label = ctk.CTkLabel(
            logo_frame,
            text=self._app_cfg.get("negocio", "Mi Taller 3D"),
            font=ctk.CTkFont("DM Sans", 11),
            text_color=W.T("text_sub"))
        self.biz_name_label.pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color=W.T("border")).pack(fill="x", padx=10, pady=10)

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

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color=W.T("border")).pack(fill="x", padx=10, pady=6)

        # ── Toggle tema ──
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(fill="x", padx=14, pady=(0, 8))

        self._theme_icon_lbl = ctk.CTkLabel(
            theme_frame,
            text="🌙" if self.theme_mode == "dark" else "☀️",
            font=ctk.CTkFont("DM Sans", 18),
            width=32)
        self._theme_icon_lbl.pack(side="left")

        self._theme_label = ctk.CTkLabel(
            theme_frame,
            text="Tema oscuro" if self.theme_mode == "dark" else "Tema claro",
            font=ctk.CTkFont("DM Sans", 11),
            text_color=W.T("text_sub"))
        self._theme_label.pack(side="left", padx=6)

        self._theme_toggle = ctk.CTkSwitch(
            theme_frame, text="",
            command=self._toggle_theme,
            progress_color=W.T("accent"),
            button_color=W.T("accent"),
            width=46,
            onvalue=True, offvalue=False,
        )
        self._theme_toggle.pack(side="right")
        if self.theme_mode == "dark":
            self._theme_toggle.select()

        ctk.CTkLabel(self.sidebar, text="v2.0 · Print3D Pro",
                     font=ctk.CTkFont("DM Sans", 9),
                     text_color=W.T("text_dim")).pack(pady=(0, 10))

    # ─────────────────────────────────────────────────────────
    # CONTENT
    # ─────────────────────────────────────────────────────────

    def _build_content(self):
        self.container = ctk.CTkFrame(self, fg_color=W.T("bg"), corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")

    def _create_tabs(self):
        self.frames = {}
        tab_classes = {
            "dashboard":  DashboardTab,
            "cotizador":  CotizadorTab,
            "impresoras": ImpresorasTab,
            "materiales": MaterialesTab,
            "ventas":     VentasTab,
            "config":     ConfigTab,
        }
        for name, cls in tab_classes.items():
            frame = cls(self.container, self)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[name] = frame

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

        for k, btn in self.tab_buttons.items():
            if k == name:
                btn.configure(fg_color=W.T("bg_selected"),
                              text_color=W.T("accent"))
            else:
                btn.configure(fg_color="transparent",
                              text_color=W.T("text_sub"))

    # ─────────────────────────────────────────────────────────
    # TEMA
    # ─────────────────────────────────────────────────────────

    def _toggle_theme(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self._app_cfg["tema"] = self.theme_mode
        self.save_config()

        theme = get_theme(self.theme_mode)
        ctk.set_appearance_mode(theme["ctk_mode"])
        W.set_theme(theme)

        # FIX: actualizar iconos del sidebar ANTES del rebuild
        self._theme_icon_lbl.configure(
            text="☀️" if self.theme_mode == "light" else "🌙")
        self._theme_label.configure(
            text="Tema claro" if self.theme_mode == "light" else "Tema oscuro")

        self.toast("🎨 Tema cambiado — reiniciando UI…")
        self.after(400, self._full_rebuild)

    def _full_rebuild(self):
        """
        FIX CRÍTICO: destruir widgets y reconstruir completamente.
        El bug original era que self.frames seguía referenciando frames
        destruidos, causando errores de Tcl al hacer refresh().
        """
        # Limpiar referencias ANTES de destruir widgets
        self.frames = {}
        self.tab_buttons = {}

        # Destruir contenido visual
        for widget in self.winfo_children():
            widget.destroy()

        # Reconstruir todo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()
        self._create_tabs()
        self.show("dashboard")

    # ─────────────────────────────────────────────────────────
    # PERSISTENCIA
    # ─────────────────────────────────────────────────────────

    def save_config(self):
        save("config", self._app_cfg)

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

    def _set_window_icon(self):
        try:
            icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass


if __name__ == "__main__":
    app = Print3DApp()
    app.mainloop()
