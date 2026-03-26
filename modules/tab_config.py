"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Configuración     ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
from modules.widgets import (
    Card, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    Entry, Dropdown, BtnPrimary, BtnGhost,
    T, font, confirm
)
from data.constants import DEFAULT_CONFIG
from data.store import save


class ConfigTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=T("bg"), corner_radius=0)
        self.app = app

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        app = self.app
        cfg = app.config

        PageHeader(self, "Configuración",
                   "Parámetros globales que afectan todas las cotizaciones")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=16)

        # ── Negocio ──────────────────────────────────────
        biz_card = Card(scroll)
        biz_card.pack(fill="x", pady=(0, 14))
        SectionTitle(biz_card, "🏢  TU NEGOCIO")

        biz_grid = ctk.CTkFrame(biz_card, fg_color="transparent")
        biz_grid.pack(fill="x", padx=16, pady=(0, 16))
        biz_grid.columnconfigure(0, weight=1)
        biz_grid.columnconfigure(1, weight=1)

        self.negocio_var  = ctk.StringVar(value=cfg.get("negocio", ""))
        self.contacto_var = ctk.StringVar(value=cfg.get("contacto", ""))

        for col_i, (lbl_text, var) in enumerate([
            ("Nombre del taller / negocio", self.negocio_var),
            ("Email o contacto para cotizaciones", self.contacto_var),
        ]):
            f = ctk.CTkFrame(biz_grid, fg_color="transparent")
            f.grid(row=0, column=col_i, padx=6, sticky="ew")
            Label(f, lbl_text, size=11, color=T("text_sub")).pack(anchor="w")
            Entry(f, textvariable=var).pack(fill="x")

        # ── Parámetros ───────────────────────────────────
        param_card = Card(scroll)
        param_card.pack(fill="x", pady=(0, 14))
        SectionTitle(param_card, "⚙️  PARÁMETROS DE COTIZACIÓN")

        param_inner = ctk.CTkFrame(param_card, fg_color="transparent")
        param_inner.pack(fill="x", padx=16, pady=(0, 18))
        param_inner.columnconfigure(0, weight=1)
        param_inner.columnconfigure(1, weight=1)
        param_inner.columnconfigure(2, weight=1)

        # Merma
        self.merma_var = ctk.DoubleVar(value=cfg.get("merma", 0.05))
        mf = ctk.CTkFrame(param_inner, fg_color="transparent")
        mf.grid(row=0, column=0, padx=10, sticky="ew")
        Label(mf, "Merma operativa", size=12).pack(anchor="w", pady=(0, 4))
        self.merma_lbl = Label(mf, f"{cfg.get('merma', 0.05) * 100:.0f}%",
                               size=28, bold=True, color=T("accent"))
        self.merma_lbl.pack()
        ctk.CTkSlider(mf, from_=0, to=0.30,
                      variable=self.merma_var,
                      number_of_steps=30,
                      progress_color=T("accent"),
                      button_color=T("accent"),
                      button_hover_color=T("accent_hover"),
                      command=lambda v: self.merma_lbl.configure(
                          text=f"{v * 100:.0f}%")).pack(fill="x", pady=6)
        Label(mf, "desperdicios, fallas, calibración",
              size=10, color=T("text_sub")).pack()

        # Margen
        self.margen_var = ctk.DoubleVar(value=cfg.get("margen", 0.15))
        mgf = ctk.CTkFrame(param_inner, fg_color="transparent")
        mgf.grid(row=0, column=1, padx=10, sticky="ew")
        Label(mgf, "Margen de ganancia", size=12).pack(anchor="w", pady=(0, 4))
        self.margen_lbl = Label(mgf, f"{cfg.get('margen', 0.15) * 100:.0f}%",
                                size=28, bold=True, color=T("green"))
        self.margen_lbl.pack()
        ctk.CTkSlider(mgf, from_=0.05, to=1.0,
                      variable=self.margen_var,
                      number_of_steps=95,
                      progress_color=T("green"),
                      button_color=T("green"),
                      button_hover_color=T("green"),
                      command=lambda v: self.margen_lbl.configure(
                          text=f"{v * 100:.0f}%")).pack(fill="x", pady=6)
        Label(mgf, "tu ganancia final por pieza",
              size=10, color=T("text_sub")).pack()

        # Electricidad
        self.elec_var = ctk.StringVar(value=str(cfg.get("electricidad_kwh", 0.9)))
        ef = ctk.CTkFrame(param_inner, fg_color="transparent")
        ef.grid(row=0, column=2, padx=10, sticky="ew")
        Label(ef, "Costo electricidad", size=12).pack(anchor="w", pady=(0, 4))
        Entry(ef, textvariable=self.elec_var,
              font=font(22)).pack(fill="x", pady=10)
        Label(ef, f"{cfg.get('moneda', 'MXN')} / kWh",
              size=10, color=T("text_sub")).pack()

        # ── Moneda ───────────────────────────────────────
        cur_card = Card(scroll)
        cur_card.pack(fill="x", pady=(0, 14))
        SectionTitle(cur_card, "💱  MONEDA")

        self.moneda_var = ctk.StringVar(value=cfg.get("moneda", "MXN"))
        cur_row = ctk.CTkFrame(cur_card, fg_color="transparent")
        cur_row.pack(anchor="w", padx=16, pady=(0, 16))
        self._cur_buttons = {}

        for currency in ["MXN", "USD", "EUR", "COP", "ARS", "BRL"]:
            is_sel = currency == self.moneda_var.get()
            b = ctk.CTkButton(
                cur_row, text=currency, width=72,
                fg_color=T("accent") if is_sel else T("bg_card2"),
                hover_color=T("accent_hover") if is_sel else T("bg_hover"),
                text_color="#fff" if is_sel else T("text"),
                border_width=1,
                border_color=T("accent") if is_sel else T("border"),
                font=font(13, "bold"),
                corner_radius=8,
                command=lambda c=currency: self._set_currency(c, cur_row),
            )
            b.pack(side="left", padx=4)
            self._cur_buttons[currency] = b

        # ── Fórmula activa ───────────────────────────────
        form_card = Card(scroll)
        form_card.pack(fill="x", pady=(0, 14))
        SectionTitle(form_card, "📐  FÓRMULA DE COTIZACIÓN ACTIVA")

        formula_items = [
            (T("accent"),  "Costo Material",
             lambda c=cfg: f"Peso (g)  ×  Costo/gramo"),
            (T("blue"),    "Costo Máquina",
             lambda c=cfg: f"Tiempo (h)  ×  Costo/hora (por impresora)"),
            (T("green"),   "Electricidad",
             lambda c=cfg: f"kW consumo  ×  {c.get('electricidad_kwh', 0.9)} {c.get('moneda','MXN')}/kWh  ×  Tiempo"),
            (T("yellow"),  "Subtotal",
             lambda c=cfg: "Material + Máquina + Extras multicolor"),
            (T("purple"),  f"+ Merma  ({cfg.get('merma', 0.05) * 100:.0f}%)",
             lambda c=cfg: f"Subtotal  ×  {1 + c.get('merma', 0.05):.3f}"),
            (T("accent"),  f"PRECIO FINAL  (+{cfg.get('margen', 0.15) * 100:.0f}%)",
             lambda c=cfg: f"(Sub+Merma)  ×  {1 + c.get('margen', 0.15):.3f}"),
        ]

        for color, label_text, formula_fn in formula_items:
            fl = ctk.CTkFrame(form_card, fg_color="transparent")
            fl.pack(fill="x", padx=18, pady=4)
            ctk.CTkLabel(fl, text=label_text, font=font(12, "bold"),
                         text_color=color, width=260, anchor="w").pack(side="left")
            ctk.CTkLabel(fl, text=f"=  {formula_fn(cfg)}", font=font(12),
                         text_color=T("text_sub"), anchor="w").pack(side="left")

        ctk.CTkFrame(form_card, fg_color="transparent", height=8).pack()

        # ── Botones ──────────────────────────────────────
        btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 24))

        BtnPrimary(btn_row, "Guardar Configuración",
                   self._save, icon="💾", width=220).pack(side="left")
        BtnGhost(btn_row, "↺ Restablecer defaults",
                 self._reset, width=180).pack(side="left", padx=12)

    def _set_currency(self, currency: str, row):
        self.moneda_var.set(currency)
        for c, b in self._cur_buttons.items():
            is_sel = c == currency
            b.configure(
                fg_color=T("accent") if is_sel else T("bg_card2"),
                hover_color=T("accent_hover") if is_sel else T("bg_hover"),
                text_color="#fff" if is_sel else T("text"),
                border_color=T("accent") if is_sel else T("border"),
            )

    def _save(self):
        try:
            self.app.config.update({
                "negocio":          self.negocio_var.get().strip(),
                "contacto":         self.contacto_var.get().strip(),
                "merma":            round(float(self.merma_var.get()), 3),
                "margen":           round(float(self.margen_var.get()), 3),
                "electricidad_kwh": float(self.elec_var.get()),
                "moneda":           self.moneda_var.get(),
            })
            self.app.save_config()
            self.app.toast("✅ Configuración guardada")
            # Actualizar nombre en sidebar
            if hasattr(self.app, "biz_name_label"):
                self.app.biz_name_label.configure(
                    text=self.app.config.get("negocio", "Mi Taller 3D"))
            self.refresh()
        except ValueError as e:
            self.app.toast(f"⚠️ Valor inválido: {e}", ok=False)

    def _reset(self):
        if not confirm(self, "Restablecer configuración",
                       "¿Restablecer todos los parámetros a sus valores por defecto?"):
            return
        self.app.config = dict(DEFAULT_CONFIG)
        self.app.save_config()
        self.app.toast("↺ Configuración restablecida a defaults")
        self.refresh()
        if hasattr(self.app, "biz_name_label"):
            self.app.biz_name_label.configure(text=DEFAULT_CONFIG["negocio"])