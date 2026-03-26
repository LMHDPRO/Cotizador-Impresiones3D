"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Dashboard         ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from modules.widgets import (
    Card, SubCard, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    CircularGauge, KpiCard, T, font
)
from data.store import fmt, calc_item, get_stats
from data.constants import ORDER_STATUSES
from themes.theme import brand_color


class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=T("bg"), corner_radius=0)
        self.app = app
        self._gauges = []

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._gauges = []
        self._build()

    def _build(self):
        app = self.app
        cfg = app.config
        stats = get_stats(app.orders, app.materials, app.printers, cfg)

        PageHeader(self, "Dashboard", "Resumen de tu operación de impresión 3D")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=16)

        # ── KPI Row ──────────────────────────────────────────────
        kpi_row = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_row.pack(fill="x", pady=(0, 16))
        for i in range(4):
            kpi_row.columnconfigure(i, weight=1)

        kpis = [
            ("Impresoras Activas", str(stats["active_printers"]), "🖨️", T("accent")),
            ("Órdenes Pendientes", str(stats["pending"]),         "⏳", T("yellow")),
            ("En Proceso",         str(stats["in_progress"]),      "⚡", T("blue")),
            ("Ingresos Totales",   fmt(stats["revenue"], cfg["moneda"]), "💰", T("green")),
        ]
        for i, (title, val, icon, col) in enumerate(kpis):
            card = KpiCard(kpi_row, title, val, icon, col)
            card.grid(row=0, column=i, padx=5, sticky="ew")

        # ── Alertas de stock bajo ─────────────────────────────
        low_stock = [m for m in app.materials
                     if ((m.get("spoolWeight", 1000) - m.get("usedGrams", 0))
                         / max(m.get("spoolWeight", 1000), 1)) < 0.20]

        if low_stock:
            alert_card = ctk.CTkFrame(
                scroll,
                fg_color=T("yellow_dim"),
                border_width=1,
                border_color=T("yellow"),
                corner_radius=10
            )
            alert_card.pack(fill="x", pady=(0, 14))

            names = ", ".join(m["name"] for m in low_stock)
            Label(
                alert_card,
                f"⚠️  Stock bajo: {names}  —  Reponer pronto",
                size=12,
                color=T("yellow")
            ).pack(padx=16, pady=10)

        # ── Filamentos ───────────────────────────────────────
        fil_card = Card(scroll)
        fil_card.pack(fill="x", pady=(0, 16))
        SectionTitle(fil_card, "🧵  FILAMENTO DISPONIBLE")

        if not app.materials:
            Label(
                fil_card,
                "Sin materiales. Agrega en la pestaña Materiales →",
                size=12,
                color=T("text_sub")
            ).pack(padx=18, pady=(0, 16))
        else:
            gauge_row = ctk.CTkFrame(fil_card, fg_color="transparent")
            gauge_row.pack(fill="x", padx=16, pady=(0, 18))

            for i, m in enumerate(app.materials):
                spool = float(m.get("spoolWeight", 1000))
                used  = float(m.get("usedGrams", 0))
                rem   = max(0.0, spool - used)
                pct   = rem / spool if spool > 0 else 0
                col   = CircularGauge.color_for_pct(pct)

                gf = ctk.CTkFrame(gauge_row, fg_color="transparent")
                gf.grid(row=0, column=i, padx=10, pady=4, sticky="n")

                gauge = CircularGauge(gf, size=120)
                gauge.pack()
                gauge.draw(pct, m["name"], rem, spool, col)
                self._gauges.append(gauge)

                if pct < 0.20:
                    Label(gf, "⚠️ Stock bajo", size=10, color=T("red")).pack(pady=(2, 0))

        # ── Two columns ──────────────────────────────────────
        two = ctk.CTkFrame(scroll, fg_color="transparent")
        two.pack(fill="x", pady=(0, 16))
        two.columnconfigure(0, weight=1)
        two.columnconfigure(1, weight=1)

        # ── Últimas órdenes
        ord_card = Card(two)
        ord_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        SectionTitle(ord_card, "📋  ÚLTIMAS ÓRDENES")

        if not app.orders:
            Label(
                ord_card,
                "Sin órdenes. Genera tu primera cotización →",
                size=12,
                color=T("text_sub")
            ).pack(padx=18, pady=(0, 18))
        else:
            recent = list(reversed(app.orders[-6:]))

            for o in recent:
                row = ctk.CTkFrame(ord_card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=4)

                info = ctk.CTkFrame(row, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True)

                Label(info, o.get("clientName", "Sin nombre"),
                      size=13, bold=True).pack(anchor="w")

                n = len(o.get("items", []))
                d = o.get("createdAt", "")[:10]

                Label(info, f"{n} pza{'s' if n != 1 else ''} · {d}",
                      size=11, color=T("text_sub")).pack(anchor="w")

                right = ctk.CTkFrame(row, fg_color="transparent")
                right.pack(side="right")

                Label(right, fmt(o.get("total", 0), cfg["moneda"]),
                      size=13, bold=True, color=T("accent")).pack(anchor="e")

                st = o.get("status", "pending")
                st_info = ORDER_STATUSES.get(st, {"label": st, "color": T("text_sub")})

                Label(right, st_info["label"], size=10,
                      color=st_info["color"]).pack(anchor="e")

            Divider(ord_card).pack(fill="x", padx=16, pady=6)
            ctk.CTkFrame(ord_card, fg_color="transparent", height=4).pack()

        # ── Flota de impresoras
        pr_card = Card(two)
        pr_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        SectionTitle(pr_card, "🖨️  FLOTA DE IMPRESORAS")

        if not app.printers:
            Label(
                pr_card,
                "Sin impresoras. Agrega en Impresoras →",
                size=12,
                color=T("text_sub")
            ).pack(padx=18, pady=(0, 18))
        else:
            for p in app.printers:
                active = p.get("active", True)

                item = ctk.CTkFrame(
                    pr_card,
                    fg_color=T("bg_card2"),
                    corner_radius=9,
                    border_width=1,
                    border_color=T("border")
                )
                item.pack(fill="x", padx=14, pady=4)

                inner = ctk.CTkFrame(item, fg_color="transparent")
                inner.pack(fill="x", padx=10, pady=8)

                brand = p.get("brand", "Custom")
                bc = brand_color(brand, app.theme_mode)

                tag_row = ctk.CTkFrame(inner, fg_color="transparent")
                tag_row.pack(anchor="w")

                Tag(tag_row, brand, bc).pack(side="left")

                if p.get("multicolor"):
                    Tag(tag_row, f"🎨 {p.get('colors',1)} col.", T("accent")).pack(side="left", padx=4)

                if not active:
                    Tag(tag_row, "Inactiva", T("red")).pack(side="left", padx=4)

                Label(inner, p["name"], size=13, bold=True).pack(anchor="w", pady=(3, 0))

                bv = p.get("buildVolume", {})
                extras = ""

                if p.get("multicolor"):
                    extras = f"  ·  🎨 {p.get('amsType', 'AMS')}"

                Label(
                    inner,
                    f"{bv.get('x',0)}×{bv.get('y',0)}×{bv.get('z',0)}mm{extras}",
                    size=11,
                    color=T("text_sub")
                ).pack(anchor="w")

            Divider(pr_card).pack(fill="x", padx=16, pady=6)
            ctk.CTkFrame(pr_card, fg_color="transparent", height=4).pack()

        # ── Resumen financiero ─────────────────────────────────
        fin_card = Card(scroll)
        fin_card.pack(fill="x", pady=(0, 16))
        SectionTitle(fin_card, "💹  RESUMEN FINANCIERO")

        fin_grid = ctk.CTkFrame(fin_card, fg_color="transparent")
        fin_grid.pack(fill="x", padx=16, pady=(0, 18))

        for i in range(3):
            fin_grid.columnconfigure(i, weight=1)

        dim_map = {
            T("green"): T("green_dim"),
            T("yellow"): T("yellow_dim"),
            T("blue"): T("blue_dim"),
            T("red"): T("red_dim"),
            T("accent"): T("accent_dim"),
        }

        fin_items = [
            ("✅ Ingresos confirmados", stats["revenue"],   T("green")),
            ("⏳ Por cobrar",           stats["expected"],  T("yellow")),
            ("📦 Total en sistema",
             stats["revenue"] + stats["expected"], T("accent")),
        ]

        for i, (lbl, val, col) in enumerate(fin_items):
            fc = ctk.CTkFrame(
                fin_grid,
                fg_color=dim_map.get(col, T("bg_card2")),
                border_width=1,
                border_color=col,
                corner_radius=9
            )
            fc.grid(row=0, column=i, padx=5, sticky="ew")

            Label(fc, lbl, size=11, color=T("text_sub")).pack(anchor="w", padx=14, pady=(12, 4))

            Label(
                fc,
                fmt(val, cfg["moneda"]),
                size=18,
                bold=True,
                color=col
            ).pack(anchor="w", padx=14, pady=(0, 12))