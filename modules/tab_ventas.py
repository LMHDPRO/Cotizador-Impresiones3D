"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Ventas & Órdenes  ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from modules.widgets import (
    Card, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    Entry, Dropdown, BtnPrimary, BtnGhost, BtnDanger, BtnSuccess,
    KpiCard, T, font, confirm
)
from data.store import fmt, calc_item
from data.constants import ORDER_STATUSES


class VentasTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=T("bg"), corner_radius=0)
        self.app = app
        self._filter = "all"
        self._expanded = set()

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        app = self.app
        cfg = app.config
        orders = app.orders

        PageHeader(self, "Ventas & Órdenes", "Gestión de pedidos, seguimiento y notas")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=16)

        # ── KPIs ─────────────────────────────────────────
        kpi_row = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_row.pack(fill="x", pady=(0, 14))
        for i in range(4):
            kpi_row.columnconfigure(i, weight=1)

        kpis = [
            ("Total órdenes",  str(len(orders)),                                        "📦", T("text_sub")),
            ("Pendientes",     str(sum(1 for o in orders if o.get("status")=="pending")),"⏳", T("yellow")),
            ("En proceso",     str(sum(1 for o in orders if o.get("status")=="in-progress")), "⚡", T("blue")),
            ("Completadas",    str(sum(1 for o in orders if o.get("status")=="completed")),    "✅", T("green")),
        ]
        for i, (title, val, icon, col) in enumerate(kpis):
            card = KpiCard(kpi_row, title, val, icon, col)
            card.grid(row=0, column=i, padx=5, sticky="ew")

        # Revenue cards
        rev_row = ctk.CTkFrame(scroll, fg_color="transparent")
        rev_row.pack(fill="x", pady=(0, 14))
        rev_row.columnconfigure(0, weight=1)
        rev_row.columnconfigure(1, weight=1)

        revenue  = sum(o.get("total", 0) for o in orders if o.get("status") == "completed")
        expected = sum(o.get("total", 0) for o in orders
                       if o.get("status") in ("pending", "in-progress"))

        for col_i, (lbl_text, val, col, border_col) in enumerate([
            ("💰 Ingresos confirmados", revenue,  T("green"),  T("green")),
            ("⏳ Ingresos por cobrar",  expected, T("yellow"), T("yellow")),
        ]):
            rc = ctk.CTkFrame(rev_row,
                               fg_color=T("bg_card"),
                               border_width=1,
                               border_color=border_col + "30",
                               corner_radius=12)
            rc.grid(row=0, column=col_i, padx=5, sticky="ew")
            Label(rc, lbl_text, size=11, color=T("text_sub")).pack(anchor="w", padx=16, pady=(12, 4))
            Label(rc, fmt(val, cfg["moneda"]), size=20, bold=True, color=col).pack(anchor="w", padx=16, pady=(0, 12))

        # ── Filtros ──────────────────────────────────────
        fil_row = ctk.CTkFrame(scroll, fg_color="transparent")
        fil_row.pack(fill="x", pady=(0, 14))
        filters = [
            ("all",         "Todas"),
            ("pending",     "Pendientes"),
            ("in-progress", "En proceso"),
            ("completed",   "Completadas"),
            ("cancelled",   "Canceladas"),
            ("delivered",   "Entregadas"),
        ]
        for fid, flbl in filters:
            is_active = self._filter == fid
            ctk.CTkButton(
                fil_row, text=flbl,
                command=lambda f=fid: self._set_filter(f),
                fg_color=T("accent") + "22" if is_active else "transparent",
                border_width=1,
                border_color=T("accent") if is_active else T("border"),
                text_color=T("accent") if is_active else T("text_sub"),
                hover_color=T("bg_hover"),
                font=font(12),
                corner_radius=7,
                width=100,
            ).pack(side="left", padx=3)

        # ── Lista de órdenes ─────────────────────────────
        filtered = [
            o for o in reversed(orders)
            if self._filter == "all" or o.get("status") == self._filter
        ]

        if not filtered:
            ctk.CTkFrame(scroll,
                          fg_color=T("bg_card"),
                          corner_radius=12,
                          height=80).pack(fill="x")
            Label(scroll, "Sin órdenes en esta categoría.",
                  size=13, color=T("text_sub")).pack(pady=24)
            return

        for o in filtered:
            self._render_order(scroll, o)

    def _set_filter(self, f: str):
        self._filter = f
        self.refresh()

    def _render_order(self, parent, o):
        cfg     = self.app.config
        oid     = o["id"]
        is_open = oid in self._expanded
        st      = o.get("status", "pending")
        st_info = ORDER_STATUSES.get(st, {"label": st, "color": T("text_sub")})

        border_col = T("accent_border") if is_open else T("border")
        order_card = ctk.CTkFrame(parent,
                                   fg_color=T("bg_card"),
                                   corner_radius=12,
                                   border_width=1,
                                   border_color=border_col)
        order_card.pack(fill="x", pady=5)

        # ── Header row ───────────────────────────────────
        hr = ctk.CTkFrame(order_card, fg_color="transparent")
        hr.pack(fill="x", padx=16, pady=12)
        hr.bind("<Button-1>", lambda e: self._toggle_expand(oid))

        info = ctk.CTkFrame(hr, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        info.bind("<Button-1>", lambda e: self._toggle_expand(oid))

        folio = o.get("folio", "")
        name  = o.get("clientName", "Cliente sin nombre")
        Label(info, f"{folio}  {name}" if folio else name,
              size=14, bold=True).pack(anchor="w")
        n_items = len(o.get("items", []))
        date_str = o.get("createdAt", "")[:10]
        Label(info, f"{n_items} pza{'s' if n_items != 1 else ''}  ·  {date_str}",
              size=11, color=T("text_sub")).pack(anchor="w")

        right = ctk.CTkFrame(hr, fg_color="transparent")
        right.pack(side="right")

        # Status dropdown
        st_names = [v["label"] for v in ORDER_STATUSES.values()]
        st_var = ctk.StringVar(value=st_info["label"])

        def on_status_change(choice, oid2=oid):
            new_key = next(
                (k for k, v in ORDER_STATUSES.items() if v["label"] == choice),
                "pending"
            )
            for order in self.app.orders:
                if order["id"] == oid2:
                    order["status"] = new_key
            self.app.save_orders()
            self.app.toast("✅ Estado actualizado")
            self.refresh()
            if "dashboard" in self.app.frames:
                self.app.frames["dashboard"].refresh()

        ctk.CTkOptionMenu(
            right, values=st_names, variable=st_var,
            command=on_status_change,
            fg_color=st_info["color"] + "22",
            button_color=T("border"),
            button_hover_color=T("bg_hover"),
            text_color=st_info["color"],
            dropdown_fg_color=T("bg_card"),
            dropdown_text_color=T("text"),
            dropdown_hover_color=T("bg_hover"),
            font=font(12),
            corner_radius=7,
            width=130,
        ).pack(side="left", padx=8)

        Label(right, fmt(o.get("total", 0), cfg["moneda"]),
              size=16, bold=True, color=T("accent")).pack(side="left", padx=8)

        expand_icon = "▾" if is_open else "▸"
        Label(right, expand_icon, size=16, color=T("text_sub")).pack(side="left", padx=4)

        BtnDanger(right, "🗑️",
                  lambda oid2=oid: self._delete(oid2), width=36).pack(side="left", padx=4)

        # ── Detalle expandido ─────────────────────────────
        if is_open:
            Divider(order_card).pack(fill="x", padx=16, pady=4)

            det = ctk.CTkFrame(order_card, fg_color="transparent")
            det.pack(fill="x", padx=16, pady=(4, 12))

            # Contacto
            if o.get("clientEmail"):
                Label(det, f"✉  {o['clientEmail']}", size=12,
                      color=T("text_sub")).pack(anchor="w", pady=1)
            if o.get("clientPhone"):
                Label(det, f"📞  {o['clientPhone']}", size=12,
                      color=T("text_sub")).pack(anchor="w", pady=1)

            # Piezas
            items = o.get("items", [])
            if items:
                Label(det, "PIEZAS", size=10, bold=True,
                      color=T("text_dim")).pack(anchor="w", pady=(10, 4))
                for item in items:
                    mat = next((m for m in self.app.materials if m["id"] == item.get("materialId")), None)
                    pr  = next((p for p in self.app.printers  if p["id"] == item.get("printerId")),  None)
                    c   = calc_item(item, self.app.materials, self.app.printers, cfg)
                    item_row = ctk.CTkFrame(det,
                                             fg_color=T("bg_card2"),
                                             corner_radius=7)
                    item_row.pack(fill="x", pady=2)
                    Label(item_row,
                          f"  {item.get('name','?')}  ×{item.get('qty',1)}  —  "
                          f"{mat['name'] if mat else '?'}  ·  {pr['name'] if pr else '?'}",
                          size=12, color=T("text_sub")).pack(side="left", pady=6, padx=4)
                    if c:
                        Label(item_row,
                              fmt(c["precioFinal"] * item.get("qty", 1), cfg["moneda"]) + "  ",
                              size=12, bold=True, color=T("accent")).pack(side="right", pady=6)

            # Notas
            if o.get("notes"):
                Divider(order_card).pack(fill="x", padx=16, pady=6)
                Label(order_card, f"📝  {o['notes']}", size=12,
                      color=T("text_sub")).pack(anchor="w", padx=16, pady=(0, 6))

            # Agregar nota
            Divider(order_card).pack(fill="x", padx=16, pady=4)
            note_row = ctk.CTkFrame(order_card, fg_color=T("bg_card2"),
                                     corner_radius=0)
            note_row.pack(fill="x")
            note_var = ctk.StringVar()
            Entry(note_row, textvariable=note_var,
                  placeholder_text="Agregar nota sobre este pedido…").pack(
                side="left", padx=10, pady=8, fill="x", expand=True)

            def add_note(oid2=oid, v=note_var):
                txt = v.get().strip()
                if not txt:
                    return
                stamp = f"[{datetime.now().strftime('%d/%m/%Y')}] {txt}"
                for order in self.app.orders:
                    if order["id"] == oid2:
                        existing = order.get("notes", "")
                        order["notes"] = f"{existing}\n{stamp}".strip()
                self.app.save_orders()
                v.set("")
                self.app.toast("✅ Nota guardada")
                self.refresh()

            BtnGhost(note_row, "+ Nota", add_note,
                     width=80, color=T("accent")).pack(side="right", padx=8, pady=6)

    def _toggle_expand(self, oid: str):
        if oid in self._expanded:
            self._expanded.discard(oid)
        else:
            self._expanded.add(oid)
        self.refresh()

    def _delete(self, oid: str):
        o = next((o for o in self.app.orders if o["id"] == oid), None)
        client = o.get("clientName", "esta orden") if o else "esta orden"
        if not confirm(self, "Eliminar orden", f"¿Eliminar la orden de '{client}'? Esta acción no se puede deshacer."):
            return
        self.app.orders = [o for o in self.app.orders if o["id"] != oid]
        self.app.save_orders()
        self._expanded.discard(oid)
        self.app.toast("🗑️ Orden eliminada")
        self.refresh()
        if "dashboard" in self.app.frames:
            self.app.frames["dashboard"].refresh()
