"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Cotizador         ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from modules.widgets import (
    Card, SubCard, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    Entry, Dropdown, BtnPrimary, BtnGhost, BtnDanger,
    T, font, confirm
)
from data.store import fmt, calc_item, new_id
from data.constants import ORDER_STATUSES
from datetime import datetime


class CotizadorTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=T("bg"), corner_radius=0)
        self.app   = app
        self.items = []
        self._total = 0.0
        self._client_vars = {}
        self._build()

    def refresh(self):
        """Refresca dropdowns al volver a la pestaña."""
        self._render_items()
        self._recalculate()

    # ─────────────────────────────────────────────────────────
    # CONSTRUCCIÓN INICIAL
    # ─────────────────────────────────────────────────────────

    def _build(self):
        # ── Header ──
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        Label(hdr, "Cotizador", size=26, bold=True,
              color=T("text_bright")).pack(side="left")

        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.pack(side="right")
        BtnGhost(btn_row, "🗑️ Limpiar", self._clear, width=110,
                 color=T("red")).pack(side="left", padx=(0, 8))
        BtnPrimary(btn_row, "Guardar Orden", self._save_order,
                   icon="💾", width=150).pack(side="left")

        # ── Scroll ──
        self.scroll = ScrollArea(self)
        self.scroll.pack(fill="both", expand=True, padx=30, pady=14)
        self._build_form()

    def _build_form(self):
        scroll = self.scroll

        # ── Cliente ──────────────────────────────────────────
        cl_card = Card(scroll)
        cl_card.pack(fill="x", pady=(0, 14))
        SectionTitle(cl_card, "👤  DATOS DEL CLIENTE")

        cl_grid = ctk.CTkFrame(cl_card, fg_color="transparent")
        cl_grid.pack(fill="x", padx=16, pady=(0, 16))
        for i in range(4):
            cl_grid.columnconfigure(i, weight=1)

        fields = [
            ("clientName",  "Nombre / Empresa"),
            ("clientEmail", "Correo electrónico"),
            ("clientPhone", "Teléfono"),
            ("notes",       "Observaciones"),
        ]
        for i, (k, lbl) in enumerate(fields):
            f = ctk.CTkFrame(cl_grid, fg_color="transparent")
            f.grid(row=0, column=i, padx=6, sticky="ew")
            Label(f, lbl, size=11, color=T("text_sub")).pack(anchor="w")
            var = ctk.StringVar()
            self._client_vars[k] = var
            Entry(f, textvariable=var, placeholder_text=lbl).pack(fill="x")

        # ── Contenedor de ítems ──
        self.items_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        self.items_frame.pack(fill="x")

        # ── Botón agregar ──
        add_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        add_frame.pack(fill="x", pady=8)

        add_btn = ctk.CTkButton(
            add_frame, text="＋  Agregar Pieza",
            command=self._add_item,
            fg_color="transparent",
            border_width=2,
            border_color=T("border"),
            text_color=T("text_sub"),
            hover_color=T("bg_hover"),
            font=font(14),
            corner_radius=10,
            height=48,
        )
        add_btn.pack(fill="x")

        def _enter(e):
            add_btn.configure(border_color=T("accent"), text_color=T("accent"))

        def _leave(e):
            add_btn.configure(border_color=T("border"), text_color=T("text_sub"))

        add_btn.bind("<Enter>", _enter)
        add_btn.bind("<Leave>", _leave)

        # ── Total ──
        self.total_card = ctk.CTkFrame(
            scroll,
            fg_color=T("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=T("accent_border"),
        )
        self.total_card.pack(fill="x", pady=(8, 14))

        tot_inner = ctk.CTkFrame(self.total_card, fg_color="transparent")
        tot_inner.pack(fill="x", padx=20, pady=16)
        left = ctk.CTkFrame(tot_inner, fg_color="transparent")
        left.pack(side="left")
        Label(left, "TOTAL DE COTIZACIÓN", size=12,
              bold=True, color=T("text_sub")).pack(anchor="w")
        cfg = self.app.config
        Label(left,
              f"Merma {cfg['merma']*100:.0f}%  ·  Margen {cfg['margen']*100:.0f}%",
              size=11, color=T("text_dim")).pack(anchor="w")

        self.total_label = Label(
            tot_inner, fmt(0, cfg["moneda"]),
            size=30, bold=True, color=T("accent"),
        )
        self.total_label.pack(side="right")

    # ─────────────────────────────────────────────────────────
    # GESTIÓN DE ÍTEMS
    # ─────────────────────────────────────────────────────────

    def _add_item(self):
        idx = len(self.items)
        self.items.append({
            "id":               new_id(),
            "name":             f"Pieza {idx + 1}",
            "materialId":       "",
            "printerId":        "",
            "weight":           100,
            "time":             6.0,
            "qty":              1,
            "multicolor":       False,
            "multicolorLayers": [],
        })
        self._render_items()
        self._recalculate()

    def _remove_item(self, idx: int):
        if idx < len(self.items):
            self.items.pop(idx)
        self._render_items()
        self._recalculate()

    def _render_items(self):
        for w in self.items_frame.winfo_children():
            w.destroy()

        mats     = self.app.materials
        printers = [p for p in self.app.printers if p.get("active", True)]
        cfg      = self.app.config

        mat_names = [f"{m['name']} — {fmt(m['costPerGram'], cfg['moneda'])}/g"
                     for m in mats]
        pr_names  = [p["name"] for p in printers]

        for idx, item in enumerate(self.items):
            self._render_item(idx, item, mats, printers, mat_names, pr_names, cfg)

    def _render_item(self, idx, item, mats, printers, mat_names, pr_names, cfg):
        item_card = ctk.CTkFrame(
            self.items_frame,
            fg_color=T("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=T("border"),
        )
        item_card.pack(fill="x", pady=6)

        # ── Cabecera del ítem ─────────────────────────────
        hr = ctk.CTkFrame(item_card, fg_color="transparent")
        hr.pack(fill="x", padx=16, pady=(14, 10))

        num = ctk.CTkLabel(hr,
                            text=f" #{idx + 1} ",
                            font=font(11, "bold"),
                            text_color=T("accent"),
                            fg_color=T("accent") + "22",
                            corner_radius=5)
        num.pack(side="left", padx=(0, 10))

        name_var = ctk.StringVar(value=item["name"])
        name_var.trace_add("write",
                           lambda *a, i=idx, v=name_var: self._update(i, "name", v.get()))
        ctk.CTkEntry(hr, textvariable=name_var,
                     fg_color="transparent",
                     border_width=0,
                     text_color=T("text_bright"),
                     font=font(15, "bold"),
                     width=240).pack(side="left")

        BtnDanger(hr, "✕", lambda i=idx: self._remove_item(i),
                  width=32).pack(side="right")

        # ── Fila de campos ────────────────────────────────
        fr = ctk.CTkFrame(item_card, fg_color="transparent")
        fr.pack(fill="x", padx=16, pady=(0, 12))

        # Material
        mf = ctk.CTkFrame(fr, fg_color="transparent")
        mf.pack(side="left", padx=(0, 10))
        Label(mf, "Material", size=11, color=T("text_sub")).pack(anchor="w")

        mat_var = ctk.StringVar()
        if mats:
            cur = next((m for m in mats if m["id"] == item["materialId"]), None)
            if cur:
                mat_var.set(f"{cur['name']} — {fmt(cur['costPerGram'], cfg['moneda'])}/g")
            else:
                mat_var.set(mat_names[0])
                self.items[idx]["materialId"] = mats[0]["id"]

        def on_mat(ch, i=idx):
            nm = ch.split(" — ")[0].strip()
            found = next((m for m in self.app.materials if m["name"] == nm), None)
            if found:
                self.items[i]["materialId"] = found["id"]
                self._recalculate()

        Dropdown(mf, mat_names or ["— Sin materiales —"],
                 variable=mat_var, command=on_mat, width=220).pack()

        # Impresora
        pf = ctk.CTkFrame(fr, fg_color="transparent")
        pf.pack(side="left", padx=(0, 10))
        Label(pf, "Impresora", size=11, color=T("text_sub")).pack(anchor="w")

        pr_var = ctk.StringVar()
        if printers:
            cur_pr = next((p for p in printers if p["id"] == item["printerId"]), None)
            pr_var.set(cur_pr["name"] if cur_pr else pr_names[0])
            if not cur_pr:
                self.items[idx]["printerId"] = printers[0]["id"]

        def on_pr(ch, i=idx):
            found = next((p for p in self.app.printers if p["name"] == ch), None)
            if found:
                self.items[i]["printerId"] = found["id"]
                self._recalculate()

        Dropdown(pf, pr_names or ["— Sin impresoras —"],
                 variable=pr_var, command=on_pr, width=200).pack()

        # Peso, Tiempo, Cantidad
        for fkey, flbl, fw in [("weight", "Peso (g)", 80),
                                 ("time",   "Tiempo (h)", 72),
                                 ("qty",    "Cant.", 56)]:
            nf = ctk.CTkFrame(fr, fg_color="transparent")
            nf.pack(side="left", padx=(0, 8))
            Label(nf, flbl, size=11, color=T("text_sub")).pack(anchor="w")
            fvar = ctk.StringVar(value=str(item[fkey]))
            fvar.trace_add("write",
                           lambda *a, i=idx, k=fkey, v=fvar:
                           self._update_num(i, k, v.get()))
            Entry(nf, textvariable=fvar, width=fw).pack()

        # Toggle multicolor
        mcf = ctk.CTkFrame(fr, fg_color="transparent")
        mcf.pack(side="left", padx=(4, 0))
        Label(mcf, "Multicolor", size=11, color=T("text_sub")).pack(anchor="w")
        mc_var = ctk.BooleanVar(value=item["multicolor"])

        def toggle_mc(i=idx, v=mc_var):
            self.items[i]["multicolor"] = v.get()
            self._render_items()
            self._recalculate()

        ctk.CTkSwitch(mcf, text="", variable=mc_var,
                      command=toggle_mc,
                      progress_color=T("accent"),
                      button_color=T("accent"),
                      button_hover_color=T("accent_hover"),
                      width=46).pack(pady=(4, 0))

        # ── Multicolor layers ─────────────────────────────
        if item["multicolor"]:
            printer = next((p for p in self.app.printers if p["id"] == item["printerId"]), None)
            max_slots = printer["colors"] if printer and printer.get("multicolor") else 2

            mc_box = ctk.CTkFrame(item_card,
                                   fg_color=T("bg_card2"),
                                   corner_radius=9,
                                   border_width=1,
                                   border_color=T("accent_border"))
            mc_box.pack(fill="x", padx=16, pady=(0, 10))
            Label(mc_box, "🎨  Capas / Colores adicionales — purga por cambio",
                  size=11, color=T("accent")).pack(anchor="w", padx=12, pady=(10, 6))

            for li, layer in enumerate(item.get("multicolorLayers", [])):
                lr = ctk.CTkFrame(mc_box, fg_color="transparent")
                lr.pack(fill="x", padx=10, pady=3)

                Label(lr, f"Color {li + 1}", size=11,
                      color=T("text_sub")).pack(side="left", padx=(0, 8))

                lm_names = [m["name"] for m in mats]
                lm_var = ctk.StringVar(value=next(
                    (m["name"] for m in mats if m["id"] == layer.get("materialId")),
                    lm_names[0] if lm_names else ""))

                def on_layer_mat(ch, i=idx, l=li):
                    found = next((m for m in self.app.materials if m["name"] == ch), None)
                    if found:
                        self.items[i]["multicolorLayers"][l]["materialId"] = found["id"]
                        self._recalculate()

                Dropdown(lr, lm_names or ["—"],
                         variable=lm_var, command=on_layer_mat,
                         width=150).pack(side="left", padx=(0, 8))

                pg_var = ctk.StringVar(value=str(layer.get("purgeGrams", 5)))
                pg_var.trace_add("write",
                                 lambda *a, i=idx, l=li, v=pg_var:
                                 self._update_layer(i, l, v.get()))
                Entry(lr, textvariable=pg_var, width=65,
                      placeholder_text="g purga").pack(side="left", padx=(0, 6))
                Label(lr, "g", size=10, color=T("text_sub")).pack(side="left")
                BtnDanger(lr, "✕",
                          lambda i=idx, l=li: self._remove_layer(i, l),
                          width=30).pack(side="left", padx=(8, 0))

            mc_btn_row = ctk.CTkFrame(mc_box, fg_color="transparent")
            mc_btn_row.pack(fill="x", padx=10, pady=(2, 10))
            if len(item.get("multicolorLayers", [])) < max_slots:
                BtnGhost(mc_btn_row, "＋ Agregar color",
                         lambda i=idx: self._add_layer(i),
                         width=140, color=T("accent")).pack(side="left")

        # ── Desglose de costos ───────────────────────────
        c = calc_item(item, self.app.materials, self.app.printers, cfg)
        if c:
            bd = ctk.CTkFrame(item_card, fg_color="transparent")
            bd.pack(fill="x", padx=16, pady=(0, 16))
            for i2, (lbl_txt, val, hi) in enumerate([
                ("Costo Material",    c["costMaterial"],           False),
                ("Costo Máquina",     c["costMachine"],            False),
                ("Electricidad",      c["costElec"],               False),
                ("Sub.+Merma",        c["subtotalMerma"],          False),
                (f"Precio ×{item['qty']}", c["precioFinal"] * item["qty"], True),
            ]):
                bc = ctk.CTkFrame(bd,
                                   fg_color=T("accent_dim") if hi else T("bg_card2"),
                                   border_width=1,
                                   border_color=T("accent_border") if hi else T("border"),
                                   corner_radius=8)
                bc.grid(row=0, column=i2, padx=4, sticky="ew")
                bd.columnconfigure(i2, weight=1)
                Label(bc, lbl_txt, size=10, color=T("text_sub")).pack(anchor="w", padx=10, pady=(8, 2))
                Label(bc, fmt(val, cfg["moneda"]), size=12, bold=True,
                      color=T("accent") if hi else T("text")).pack(anchor="w", padx=10, pady=(0, 8))

    # ─────────────────────────────────────────────────────────
    # ACTUALIZACIONES
    # ─────────────────────────────────────────────────────────

    def _update(self, idx, key, val):
        if idx < len(self.items):
            self.items[idx][key] = val

    def _update_num(self, idx, key, val):
        try:
            v = float(val) if "." in str(val) else int(val)
            if idx < len(self.items):
                self.items[idx][key] = v
            self._recalculate()
        except (ValueError, TypeError):
            pass

    def _update_layer(self, idx, layer_idx, val):
        try:
            v = float(val)
            self.items[idx]["multicolorLayers"][layer_idx]["purgeGrams"] = v
            self._recalculate()
        except (ValueError, TypeError, IndexError):
            pass

    def _add_layer(self, idx):
        mats = self.app.materials
        self.items[idx]["multicolorLayers"].append({
            "materialId": mats[0]["id"] if mats else "",
            "purgeGrams": 5,
        })
        self._render_items()
        self._recalculate()

    def _remove_layer(self, idx, layer_idx):
        try:
            self.items[idx]["multicolorLayers"].pop(layer_idx)
        except IndexError:
            pass
        self._render_items()
        self._recalculate()

    def _recalculate(self):
        cfg   = self.app.config
        total = 0.0
        for item in self.items:
            c = calc_item(item, self.app.materials, self.app.printers, cfg)
            if c:
                total += c["precioFinal"] * int(item.get("qty", 1))
        self._total = round(total, 2)
        self.total_label.configure(text=fmt(self._total, cfg["moneda"]))

    # ─────────────────────────────────────────────────────────
    # GUARDAR / LIMPIAR
    # ─────────────────────────────────────────────────────────

    def _save_order(self):
        if not self.items:
            self.app.toast("⚠️ Agrega al menos una pieza", ok=False)
            return

        cfg = self.app.config
        order = {
            "id":          new_id(),
            "folio":       f"ORD-{len(self.app.orders) + 1:04d}",
            "clientName":  self._client_vars["clientName"].get(),
            "clientEmail": self._client_vars["clientEmail"].get(),
            "clientPhone": self._client_vars["clientPhone"].get(),
            "notes":       self._client_vars["notes"].get(),
            "items":       list(self.items),
            "total":       self._total,
            "status":      "pending",
            "createdAt":   datetime.now().isoformat(),
        }
        self.app.orders.append(order)
        self.app.save_orders()
        self.app.toast("✅ Cotización guardada como orden")
        self._clear()

        for tab in ("ventas", "dashboard"):
            if tab in self.app.frames:
                self.app.frames[tab].refresh()

    def _clear(self):
        self.items = []
        for v in self._client_vars.values():
            v.set("")
        self._render_items()
        self._recalculate()
