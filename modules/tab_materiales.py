"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Materiales        ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser
from modules.widgets import (
    Card, SubCard, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    Entry, Dropdown, BtnPrimary, BtnGhost, BtnDanger, BtnSuccess,
    CircularGauge, ColorDot, T, font, confirm
)
from data.store import fmt, new_id
from data.constants import FILAMENT_BRANDS, FILAMENT_TYPES, FILAMENT_COLORS
from themes.theme import brand_color


class MaterialesTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=T("bg"), corner_radius=0)
        self.app = app

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        Label(hdr, "Materiales & Filamentos", size=26, bold=True,
              color=T("text_bright")).pack(side="left")
        lbl_sub = Label(hdr,
                        f"{len(self.app.materials)} filamentos en inventario",
                        size=12, color=T("text_sub"))
        lbl_sub.pack(side="left", padx=14, pady=(6, 0))
        BtnPrimary(hdr, "Nuevo Material", self._add_new,
                   icon="＋", width=160).pack(side="right")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=14)

        if not self.app.materials:
            Label(scroll, "Sin materiales. Agrega tu primer filamento →",
                  size=14, color=T("text_sub")).pack(pady=60)
            return

        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        for i, m in enumerate(self.app.materials):
            row, col = divmod(i, 2)
            mc = Card(grid)
            mc.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            self._render_material_card(mc, m)

    def _render_material_card(self, parent, m):
        spool  = float(m.get("spoolWeight", 1000))
        used   = float(m.get("usedGrams", 0))
        rem    = max(0.0, spool - used)
        pct    = rem / spool if spool > 0 else 0
        col    = CircularGauge.color_for_pct(pct)
        brand  = m.get("brand", "Genérico")
        bc     = brand_color(brand, self.app.theme_mode)

        # ── Header ──────────────────────────────────────
        hr = ctk.CTkFrame(parent, fg_color="transparent")
        hr.pack(fill="x", padx=14, pady=(14, 8))

        dot_canvas = tk.Canvas(hr, width=20, height=20,
                                bg=T("bg_card"), highlightthickness=0)
        dot_canvas.pack(side="left", padx=(0, 8))
        dot_canvas.create_oval(2, 2, 18, 18,
                                fill=m.get("color", "#888"), outline="")

        name_col = ctk.CTkFrame(hr, fg_color="transparent")
        name_col.pack(side="left", fill="x", expand=True)
        Label(name_col, m["name"], size=15, bold=True).pack(anchor="w")
        # Tags: brand + type
        tag_row = ctk.CTkFrame(name_col, fg_color="transparent")
        tag_row.pack(anchor="w", pady=(2, 0))
        Tag(tag_row, brand, bc).pack(side="left")
        base = m.get("baseType", "")
        sub  = m.get("subtype", "")
        if base:
            Tag(tag_row, base, T("text_sub")).pack(side="left", padx=4)
        if sub:
            Tag(tag_row, sub, T("blue")).pack(side="left", padx=2)

        btn_col = ctk.CTkFrame(hr, fg_color="transparent")
        btn_col.pack(side="right")
        BtnSuccess(btn_col, "↺",
                   lambda mid=m["id"]: self._reset_spool(mid),
                   width=36).pack(side="left", padx=2)
        BtnGhost(btn_col, "✏️",
                 lambda mid=m["id"]: self._edit(mid), width=36).pack(side="left", padx=2)
        BtnDanger(btn_col, "🗑️",
                  lambda mid=m["id"]: self._delete(mid), width=36).pack(side="left", padx=2)

        # ── Body: gauge + info ───────────────────────────
        body = ctk.CTkFrame(parent, fg_color="transparent")
        body.pack(fill="x", padx=14, pady=(0, 10))

        gauge = CircularGauge(body, size=118)
        gauge.pack(side="left", padx=(0, 16))
        gauge.draw(pct, m["name"], rem, spool, col)

        info_col = ctk.CTkFrame(body, fg_color="transparent")
        info_col.pack(side="left", fill="x", expand=True)

        cfg = self.app.config
        infos = [
            ("Costo / gramo",  fmt(m.get("costPerGram", 0), cfg["moneda"])),
            ("Temp. impresión", f"{m.get('printTemp', 0)}°C"),
            ("Temp. cama",      f"{m.get('bedTemp', 0)}°C"),
            ("Densidad",        f"{m.get('density', 1.24)} g/cm³"),
            ("Restante",        f"{rem:.0f} / {spool:.0f} g"),
        ]
        for k, v in infos:
            r = ctk.CTkFrame(info_col, fg_color="transparent")
            r.pack(fill="x", pady=2)
            Label(r, k, size=10, color=T("text_sub")).pack(side="left", padx=(0, 6))
            Label(r, v, size=12, bold=True).pack(side="left")

        if pct < 0.20:
            Label(info_col, "⚠️ Stock bajo — reponer pronto",
                  size=11, color=T("red")).pack(anchor="w", pady=(4, 0))

        # ── Descontar ────────────────────────────────────
        disc_row = ctk.CTkFrame(parent,
                                 fg_color=T("bg_card2"),
                                 corner_radius=0)
        disc_row.pack(fill="x")

        Label(disc_row, "Descontar uso:",
              size=11, color=T("text_sub")).pack(side="left", padx=10, pady=8)

        g_var = ctk.StringVar()
        Entry(disc_row, textvariable=g_var, width=90,
              placeholder_text="gramos").pack(side="left", padx=6)

        def do_discount(mid=m["id"], v=g_var):
            try:
                g_amount = float(v.get())
                if g_amount <= 0:
                    return
                for mat in self.app.materials:
                    if mat["id"] == mid:
                        mat["usedGrams"] = min(
                            mat["spoolWeight"],
                            mat.get("usedGrams", 0) + g_amount
                        )
                self.app.save_materials()
                self.app.toast(f"✅ {g_amount:.1f}g descontados")
                self.refresh()
                if "dashboard" in self.app.frames:
                    self.app.frames["dashboard"].refresh()
            except ValueError:
                self.app.toast("⚠️ Ingresa un número válido", ok=False)

        disc_row.bind("<Return>", lambda e, mid=m["id"], v=g_var: do_discount(mid, v))
        BtnPrimary(disc_row, "− Descontar", do_discount,
                   width=120).pack(side="left", padx=6, pady=8)

        if m.get("notes"):
            Label(parent, m["notes"], size=11,
                  color=T("text_dim")).pack(anchor="w", padx=14, pady=(4, 10))

    # ─────────────────────────────────────────────────────────
    # ACCIONES
    # ─────────────────────────────────────────────────────────

    def _reset_spool(self, mid):
        if not confirm(self, "Reiniciar carrete", "¿Reiniciar al 100%? Se borrará el uso registrado."):
            return
        for m in self.app.materials:
            if m["id"] == mid:
                m["usedGrams"] = 0
        self.app.save_materials()
        self.app.toast("✅ Carrete reiniciado al 100%")
        self.refresh()
        if "dashboard" in self.app.frames:
            self.app.frames["dashboard"].refresh()

    def _delete(self, mid):
        m = next((m for m in self.app.materials if m["id"] == mid), None)
        name = m["name"] if m else "este material"
        if not confirm(self, "Eliminar material", f"¿Eliminar '{name}'? Esta acción no se puede deshacer."):
            return
        self.app.materials = [m for m in self.app.materials if m["id"] != mid]
        self.app.save_materials()
        self.app.toast("🗑️ Material eliminado")
        self.refresh()

    def _add_new(self):
        self._open_editor(None)

    def _edit(self, mid):
        m = next((m for m in self.app.materials if m["id"] == mid), None)
        if m:
            self._open_editor(m)

    # ─────────────────────────────────────────────────────────
    # EDITOR MODAL
    # ─────────────────────────────────────────────────────────

    def _open_editor(self, material):
        is_new = material is None
        if is_new:
            material = {
                "id": new_id(), "name": "", "brand": "Sunlu",
                "baseType": "PLA", "subtype": "Estándar",
                "color": "#4CAF50",
                "costPerGram": 0.35, "spoolWeight": 1000, "usedGrams": 0,
                "density": 1.24, "printTemp": 200, "bedTemp": 60, "notes": "",
            }

        dlg = ctk.CTkToplevel(self)
        dlg.title("Nuevo Material" if is_new else f"Editar — {material['name']}")
        dlg.geometry("600x680")
        dlg.configure(fg_color=T("bg"))
        dlg.grab_set()
        dlg.resizable(True, True)

        sf = ctk.CTkScrollableFrame(dlg, fg_color=T("bg"),
                                     scrollbar_button_color=T("scrollbar"),
                                     scrollbar_button_hover_color=T("text_sub"))
        sf.pack(fill="both", expand=True, padx=22, pady=18)

        Label(sf, "Nuevo Material" if is_new else "Editar Material",
              size=18, bold=True, color=T("text_bright")).pack(anchor="w", pady=(0, 16))

        # ── Marca y tipo ──────────────────────────────────
        sel_card = Card(sf)
        sel_card.pack(fill="x", pady=(0, 12))
        SectionTitle(sel_card, "🏷️  TIPO DE FILAMENTO")

        sel_grid = ctk.CTkFrame(sel_card, fg_color="transparent")
        sel_grid.pack(fill="x", padx=16, pady=(0, 14))
        for i in range(3):
            sel_grid.columnconfigure(i, weight=1)

        brand_var   = ctk.StringVar(value=material.get("brand", "Sunlu"))
        base_var    = ctk.StringVar(value=material.get("baseType", "PLA"))
        subtype_var = ctk.StringVar(value=material.get("subtype", "Estándar"))

        bf = ctk.CTkFrame(sel_grid, fg_color="transparent")
        bf.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        Label(bf, "Marca", size=11, color=T("text_sub")).pack(anchor="w")
        Dropdown(bf, list(FILAMENT_BRANDS.keys()),
                 variable=brand_var, width=170).pack(fill="x")

        btf = ctk.CTkFrame(sel_grid, fg_color="transparent")
        btf.grid(row=0, column=1, padx=(0, 8), sticky="ew")
        Label(btf, "Tipo base", size=11, color=T("text_sub")).pack(anchor="w")

        stf = ctk.CTkFrame(sel_grid, fg_color="transparent")
        stf.grid(row=0, column=2, sticky="ew")
        Label(stf, "Subtipo / Variante", size=11, color=T("text_sub")).pack(anchor="w")

        subtype_dd_holder = [None]
        specs_lbl = Label(sf, "", size=11, color=T("text_sub"))
        specs_lbl.pack(anchor="w", padx=16, pady=(0, 6))

        # Vars para specs
        cost_var   = ctk.StringVar(value=str(material.get("costPerGram", 0.35)))
        spool_var  = ctk.StringVar(value=str(material.get("spoolWeight", 1000)))
        print_var  = ctk.StringVar(value=str(material.get("printTemp", 200)))
        bed_var    = ctk.StringVar(value=str(material.get("bedTemp", 60)))
        dens_var   = ctk.StringVar(value=str(material.get("density", 1.24)))
        name_var   = ctk.StringVar(value=material.get("name", ""))
        notes_var  = ctk.StringVar(value=material.get("notes", ""))
        color_var  = ctk.StringVar(value=material.get("color", "#4CAF50"))

        def apply_subtype(base: str, sub: str):
            try:
                specs = FILAMENT_TYPES[base]["subtypes"][sub]
                cost_var.set(str(specs["costPerGram"]))
                print_var.set(str(specs["printTemp"]))
                bed_var.set(str(specs["bedTemp"]))
                dens_var.set(str(specs["density"]))
                if not name_var.get():
                    brand = brand_var.get()
                    name_var.set(f"{brand} {base} {sub}" if sub != "Estándar" else f"{brand} {base}")
                specs_lbl.configure(
                    text=f"✓ {specs['notes']}",
                    text_color=T("green"),
                )
                # Color base del tipo
                base_col = FILAMENT_TYPES.get(base, {}).get("color", "#888888")
                color_var.set(base_col)
                if hasattr(color_preview_canvas, 'itemconfigure'):
                    color_preview_canvas.itemconfigure(color_rect_id[0], fill=base_col)
            except KeyError:
                pass

        def update_subtypes(base: str):
            subs = list(FILAMENT_TYPES.get(base, {}).get("subtypes", {}).keys())
            if subtype_dd_holder[0]:
                subtype_dd_holder[0].configure(values=subs)
                if subs:
                    subtype_var.set(subs[0])
                    apply_subtype(base, subs[0])

        def on_base(ch):
            update_subtypes(ch)

        def on_sub(ch):
            apply_subtype(base_var.get(), ch)

        base_types = list(FILAMENT_TYPES.keys())
        Dropdown(btf, base_types, variable=base_var, command=on_base, width=160).pack(fill="x")

        cur_base = material.get("baseType", "PLA")
        cur_subs = list(FILAMENT_TYPES.get(cur_base, {}).get("subtypes", {}).keys())
        sub_dd = Dropdown(stf, cur_subs or ["Estándar"],
                          variable=subtype_var, command=on_sub, width=170)
        sub_dd.pack(fill="x")
        subtype_dd_holder[0] = sub_dd

        # ── Nombre personalizado ─────────────────────────
        nc_card = Card(sf)
        nc_card.pack(fill="x", pady=(0, 12))
        SectionTitle(nc_card, "✏️  NOMBRE")
        Label(nc_card, "Nombre para mostrar (auto-generado o personaliza)",
              size=11, color=T("text_sub")).pack(anchor="w", padx=16)
        Entry(nc_card, textvariable=name_var,
              placeholder_text="Ej: Sunlu PLA Silk Dorado").pack(
            fill="x", padx=16, pady=(4, 14))

        # ── Specs ────────────────────────────────────────
        sp_card = Card(sf)
        sp_card.pack(fill="x", pady=(0, 12))
        SectionTitle(sp_card, "📊  ESPECIFICACIONES (auto desde preset, editables)")

        sp_grid = ctk.CTkFrame(sp_card, fg_color="transparent")
        sp_grid.pack(fill="x", padx=16, pady=(0, 14))
        for i in range(3):
            sp_grid.columnconfigure(i, weight=1)

        spec_fields = [
            (cost_var,  "Costo / gramo ($)",       0, 0),
            (spool_var, "Peso del carrete (g)",     0, 1),
            (dens_var,  "Densidad (g/cm³)",         0, 2),
            (print_var, "Temp. impresión (°C)",     1, 0),
            (bed_var,   "Temp. cama (°C)",          1, 1),
        ]
        for var, lbl_text, row, col in spec_fields:
            f = ctk.CTkFrame(sp_grid, fg_color="transparent")
            f.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            Label(f, lbl_text, size=11, color=T("text_sub")).pack(anchor="w")
            Entry(f, textvariable=var).pack(fill="x")

        # ── Color ────────────────────────────────────────
        col_card = Card(sf)
        col_card.pack(fill="x", pady=(0, 12))
        SectionTitle(col_card, "🎨  COLOR DEL FILAMENTO")

        color_inner = ctk.CTkFrame(col_card, fg_color="transparent")
        color_inner.pack(fill="x", padx=16, pady=(0, 14))

        # Presets de color
        presets_row = ctk.CTkFrame(color_inner, fg_color="transparent")
        presets_row.pack(anchor="w", pady=(0, 10))
        Label(presets_row, "Presets: ", size=11,
              color=T("text_sub")).pack(side="left")

        color_preview_canvas = tk.Canvas(color_inner, width=44, height=36,
                                          bg=T("bg_card"), highlightthickness=0)
        color_preview_canvas.pack(side="left", padx=(0, 12))
        color_rect_id = [color_preview_canvas.create_rectangle(
            2, 2, 42, 34, fill=color_var.get(), outline="")]

        for cname, chex in list(FILAMENT_COLORS.items())[:10]:
            btn = tk.Button(presets_row, width=2, bg=chex,
                            relief="flat", cursor="hand2",
                            command=lambda h=chex: _set_color(h))
            btn.pack(side="left", padx=2)

        def _set_color(hex_color: str):
            color_var.set(hex_color)
            color_preview_canvas.itemconfigure(color_rect_id[0], fill=hex_color)

        def pick_custom():
            chosen = colorchooser.askcolor(
                color=color_var.get(), title="Color del filamento")
            if chosen[1]:
                _set_color(chosen[1])

        # También inicializar la preview con el color actual
        color_preview_canvas.itemconfigure(color_rect_id[0], fill=color_var.get())

        BtnGhost(color_inner, "🎨 Personalizado", pick_custom,
                 width=150, color=T("accent")).pack(side="left", pady=(0, 4))

        # ── Notas ────────────────────────────────────────
        nt_card = Card(sf)
        nt_card.pack(fill="x", pady=(0, 12))
        SectionTitle(nt_card, "📝  NOTAS")
        Entry(nt_card, textvariable=notes_var,
              placeholder_text="Observaciones, usos recomendados…").pack(
            fill="x", padx=16, pady=(0, 14))

        # ── Botones ──────────────────────────────────────
        btn_row = ctk.CTkFrame(sf, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))

        def save():
            try:
                data = {
                    "id":          material["id"],
                    "name":        name_var.get().strip() or
                                   f"{brand_var.get()} {base_var.get()}",
                    "brand":       brand_var.get(),
                    "baseType":    base_var.get(),
                    "subtype":     subtype_var.get(),
                    "color":       color_var.get(),
                    "costPerGram": float(cost_var.get()),
                    "spoolWeight": float(spool_var.get()),
                    "usedGrams":   material.get("usedGrams", 0),
                    "density":     float(dens_var.get()),
                    "printTemp":   float(print_var.get()),
                    "bedTemp":     float(bed_var.get()),
                    "notes":       notes_var.get(),
                }
                if is_new:
                    self.app.materials.append(data)
                else:
                    self.app.materials = [
                        data if m["id"] == data["id"] else m
                        for m in self.app.materials
                    ]
                self.app.save_materials()
                self.app.toast("✅ Material guardado")
                dlg.destroy()
                self.refresh()
                if "dashboard" in self.app.frames:
                    self.app.frames["dashboard"].refresh()
            except ValueError as e:
                self.app.toast(f"⚠️ Valor inválido: {e}", ok=False)

        BtnPrimary(btn_row, "Guardar", save, icon="💾", width=140).pack(side="left")
        BtnGhost(btn_row, "Cancelar", dlg.destroy, width=110).pack(side="left", padx=12)

        # Si es nueva, aplicar preset inicial
        if is_new:
            apply_subtype(base_var.get(), subtype_var.get())
