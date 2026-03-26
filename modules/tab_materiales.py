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
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        Label(hdr, "Materiales & Filamentos", size=26, bold=True,
              color=T("text_bright")).pack(side="left")
        Label(hdr, f"{len(self.app.materials)} filamentos en inventario",
              size=12, color=T("text_sub")).pack(side="left", padx=14, pady=(6, 0))
        BtnPrimary(hdr, "Nuevo Material", self._add_new,
                   icon="＋", width=160).pack(side="right")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=14)

        if not self.app.materials:
            empty = ctk.CTkFrame(scroll, fg_color=T("bg_card"), corner_radius=12)
            empty.pack(fill="x", pady=40)
            Label(empty, "🧵", size=40).pack(pady=(30, 8))
            Label(empty, "Sin materiales todavía", size=16,
                  bold=True, color=T("text_bright")).pack()
            Label(empty, "Haz clic en «Nuevo Material» para agregar el primero",
                  size=13, color=T("text_sub")).pack(pady=(4, 30))
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
        spool = float(m.get("spoolWeight", 1000))
        used  = float(m.get("usedGrams", 0))
        rem   = max(0.0, spool - used)
        pct   = rem / spool if spool > 0 else 0
        col   = CircularGauge.color_for_pct(pct)
        brand = m.get("brand", "Genérico")
        bc    = brand_color(brand, self.app.theme_mode)

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

        body = ctk.CTkFrame(parent, fg_color="transparent")
        body.pack(fill="x", padx=14, pady=(0, 10))

        gauge = CircularGauge(body, size=118)
        gauge.pack(side="left", padx=(0, 16))
        gauge.draw(pct, m["name"], rem, spool, col)

        info_col = ctk.CTkFrame(body, fg_color="transparent")
        info_col.pack(side="left", fill="x", expand=True)

        cfg = self.app.config
        infos = [
            ("Costo / gramo",   fmt(m.get("costPerGram", 0), cfg["moneda"])),
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

        # Descontar uso
        disc_row = ctk.CTkFrame(parent, fg_color=T("bg_card2"), corner_radius=0)
        disc_row.pack(fill="x")

        Label(disc_row, "Descontar uso:", size=11,
              color=T("text_sub")).pack(side="left", padx=10, pady=8)

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

        BtnPrimary(disc_row, "− Descontar", do_discount,
                   width=120).pack(side="left", padx=6, pady=8)

        if m.get("notes"):
            Label(parent, m["notes"], size=11,
                  color=T("text_dim")).pack(anchor="w", padx=14, pady=(4, 10))

    # ─────────────────────────────────────────────────────────
    # ACCIONES
    # ─────────────────────────────────────────────────────────

    def _reset_spool(self, mid):
        if not confirm(self, "Reiniciar carrete",
                       "¿Reiniciar al 100%? Se borrará el uso registrado."):
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
        if not confirm(self, "Eliminar material",
                       f"¿Eliminar '{name}'? Esta acción no se puede deshacer."):
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
    # EDITOR MODAL — Reescrito para corregir orden de creación
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
        dlg.geometry("620x700")
        dlg.configure(fg_color=T("bg"))
        dlg.grab_set()
        dlg.resizable(True, True)
        dlg.lift()
        dlg.focus_force()

        sf = ctk.CTkScrollableFrame(
            dlg, fg_color=T("bg"),
            scrollbar_button_color=T("scrollbar"),
            scrollbar_button_hover_color=T("text_sub"))
        sf.pack(fill="both", expand=True, padx=22, pady=18)

        Label(sf, "Nuevo Material" if is_new else "Editar Material",
              size=18, bold=True, color=T("text_bright")).pack(anchor="w", pady=(0, 16))

        # ── Variables de estado ──────────────────────────────
        brand_var   = ctk.StringVar(value=material.get("brand", "Sunlu"))
        base_var    = ctk.StringVar(value=material.get("baseType", "PLA"))
        subtype_var = ctk.StringVar(value=material.get("subtype", "Estándar"))
        cost_var    = ctk.StringVar(value=str(material.get("costPerGram", 0.35)))
        spool_var   = ctk.StringVar(value=str(material.get("spoolWeight", 1000)))
        print_var   = ctk.StringVar(value=str(material.get("printTemp", 200)))
        bed_var     = ctk.StringVar(value=str(material.get("bedTemp", 60)))
        dens_var    = ctk.StringVar(value=str(material.get("density", 1.24)))
        name_var    = ctk.StringVar(value=material.get("name", ""))
        notes_var   = ctk.StringVar(value=material.get("notes", ""))
        color_var   = ctk.StringVar(value=material.get("color", "#4CAF50"))

        # ── Tipo de filamento ────────────────────────────────
        sel_card = Card(sf)
        sel_card.pack(fill="x", pady=(0, 12))
        SectionTitle(sel_card, "🏷️  TIPO DE FILAMENTO")

        sel_grid = ctk.CTkFrame(sel_card, fg_color="transparent")
        sel_grid.pack(fill="x", padx=16, pady=(0, 8))
        for i in range(3):
            sel_grid.columnconfigure(i, weight=1)

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

        specs_lbl = ctk.CTkLabel(sel_card, text="", font=font(11),
                                  text_color=T("text_sub"))
        specs_lbl.pack(anchor="w", padx=16, pady=(4, 8))

        subtype_dd_holder = [None]

        # FIX CRÍTICO: crear color_preview_canvas ANTES de apply_subtype
        # para que la función pueda acceder a él cuando se llame en on_base/on_sub
        col_card = Card(sf)  # se empaca más abajo, pero el objeto ya existe

        # Variables para el canvas de color (necesitamos crearlos antes de apply_subtype)
        _color_canvas_ref = [None]
        _color_rect_ref   = [None]

        def apply_subtype(base: str, sub: str):
            try:
                specs = FILAMENT_TYPES[base]["subtypes"][sub]
                cost_var.set(str(specs["costPerGram"]))
                print_var.set(str(specs["printTemp"]))
                bed_var.set(str(specs["bedTemp"]))
                dens_var.set(str(specs["density"]))
                if not name_var.get():
                    brand = brand_var.get()
                    name_var.set(
                        f"{brand} {base} {sub}"
                        if sub != "Estándar" else f"{brand} {base}")
                specs_lbl.configure(
                    text=f"✓ {specs['notes']}",
                    text_color=T("green"),
                )
                base_col = FILAMENT_TYPES.get(base, {}).get("color", "#888888")
                color_var.set(base_col)
                # FIX: actualizar canvas solo si ya fue creado
                if _color_canvas_ref[0] is not None and _color_rect_ref[0] is not None:
                    _color_canvas_ref[0].itemconfigure(
                        _color_rect_ref[0], fill=base_col)
            except KeyError:
                pass

        def update_subtypes(base: str):
            subs = list(FILAMENT_TYPES.get(base, {}).get("subtypes", {}).keys())
            if not subs:
                subs = ["Estándar"]
            if subtype_dd_holder[0] is not None:
                subtype_dd_holder[0].configure(values=subs)
                subtype_var.set(subs[0])
                apply_subtype(base, subs[0])

        def on_base(ch):
            base_var.set(ch)
            update_subtypes(ch)

        def on_sub(ch):
            subtype_var.set(ch)
            apply_subtype(base_var.get(), ch)

        base_types = list(FILAMENT_TYPES.keys())
        Dropdown(btf, base_types, variable=base_var,
                 command=on_base, width=160).pack(fill="x")

        cur_base = material.get("baseType", "PLA")
        cur_subs = list(FILAMENT_TYPES.get(cur_base, {}).get("subtypes", {}).keys())
        if not cur_subs:
            cur_subs = ["Estándar"]

        cur_sub = material.get("subtype", cur_subs[0])
        if cur_sub not in cur_subs:
            cur_sub = cur_subs[0]
            subtype_var.set(cur_sub)

        sub_dd = Dropdown(stf, cur_subs, variable=subtype_var,
                          command=on_sub, width=170)
        sub_dd.pack(fill="x")
        subtype_dd_holder[0] = sub_dd

        # ── Nombre ───────────────────────────────────────────
        nc_card = Card(sf)
        nc_card.pack(fill="x", pady=(0, 12))
        SectionTitle(nc_card, "✏️  NOMBRE")
        Label(nc_card, "Nombre para mostrar (auto-generado o personaliza)",
              size=11, color=T("text_sub")).pack(anchor="w", padx=16)
        Entry(nc_card, textvariable=name_var,
              placeholder_text="Ej: Sunlu PLA Silk Dorado").pack(
            fill="x", padx=16, pady=(4, 14))

        # ── Specs ────────────────────────────────────────────
        sp_card = Card(sf)
        sp_card.pack(fill="x", pady=(0, 12))
        SectionTitle(sp_card, "📊  ESPECIFICACIONES")

        sp_grid = ctk.CTkFrame(sp_card, fg_color="transparent")
        sp_grid.pack(fill="x", padx=16, pady=(0, 14))
        for i in range(3):
            sp_grid.columnconfigure(i, weight=1)

        spec_fields = [
            (cost_var,  "Costo / gramo ($)",    0, 0),
            (spool_var, "Peso del carrete (g)", 0, 1),
            (dens_var,  "Densidad (g/cm³)",     0, 2),
            (print_var, "Temp. impresión (°C)", 1, 0),
            (bed_var,   "Temp. cama (°C)",      1, 1),
        ]
        for var, lbl_text, row, col in spec_fields:
            f = ctk.CTkFrame(sp_grid, fg_color="transparent")
            f.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            Label(f, lbl_text, size=11, color=T("text_sub")).pack(anchor="w")
            Entry(f, textvariable=var).pack(fill="x")

        # ── Color ─────────────────────────────────────────────
        # FIX: col_card ya fue creado arriba; ahora sí lo empacamos y llenamos
        col_card.pack(fill="x", pady=(0, 12))
        SectionTitle(col_card, "🎨  COLOR DEL FILAMENTO")

        color_inner = ctk.CTkFrame(col_card, fg_color="transparent")
        color_inner.pack(fill="x", padx=16, pady=(0, 14))

        # Preview de color — creado ANTES de los presets para que apply_subtype pueda usarlo
        color_preview_canvas = tk.Canvas(
            color_inner, width=44, height=36,
            bg=T("bg_card"), highlightthickness=0)
        color_preview_canvas.pack(side="left", padx=(0, 12))
        color_rect_id = color_preview_canvas.create_rectangle(
            2, 2, 42, 34, fill=color_var.get(), outline="")

        # FIX: registrar referencias para que apply_subtype pueda actualizarlo
        _color_canvas_ref[0] = color_preview_canvas
        _color_rect_ref[0]   = color_rect_id

        def _set_color(hex_color: str):
            color_var.set(hex_color)
            color_preview_canvas.itemconfigure(color_rect_id, fill=hex_color)

        def pick_custom():
            chosen = colorchooser.askcolor(
                color=color_var.get(), title="Color del filamento",
                parent=dlg)
            if chosen and chosen[1]:
                _set_color(chosen[1])

        # Presets de color
        presets_row = ctk.CTkFrame(color_inner, fg_color="transparent")
        presets_row.pack(anchor="w", pady=(0, 8), side="top")
        Label(presets_row, "Presets: ", size=11,
              color=T("text_sub")).pack(side="left")

        for cname, chex in list(FILAMENT_COLORS.items())[:12]:
            btn = tk.Button(
                presets_row, width=2, bg=chex,
                relief="flat", cursor="hand2",
                command=lambda h=chex: _set_color(h))
            btn.pack(side="left", padx=2)

        BtnGhost(color_inner, "🎨 Personalizado", pick_custom,
                 width=150, color=T("accent")).pack(
            side="left", pady=(0, 4), padx=(8, 0))

        # ── Notas ────────────────────────────────────────────
        nt_card = Card(sf)
        nt_card.pack(fill="x", pady=(0, 12))
        SectionTitle(nt_card, "📝  NOTAS")
        Entry(nt_card, textvariable=notes_var,
              placeholder_text="Observaciones, usos recomendados…").pack(
            fill="x", padx=16, pady=(0, 14))

        # ── Botones ──────────────────────────────────────────
        btn_row = ctk.CTkFrame(sf, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))

        def save():
            try:
                name = name_var.get().strip()
                if not name:
                    name = f"{brand_var.get()} {base_var.get()}"

                data = {
                    "id":          material["id"],
                    "name":        name,
                    "brand":       brand_var.get(),
                    "baseType":    base_var.get(),
                    "subtype":     subtype_var.get(),
                    "color":       color_var.get(),
                    "costPerGram": float(cost_var.get() or 0),
                    "spoolWeight": float(spool_var.get() or 1000),
                    "usedGrams":   material.get("usedGrams", 0),
                    "density":     float(dens_var.get() or 1.24),
                    "printTemp":   float(print_var.get() or 0),
                    "bedTemp":     float(bed_var.get() or 0),
                    "notes":       notes_var.get().strip(),
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

        # Si es nuevo, aplicar preset inicial DESPUÉS de crear todo el UI
        if is_new:
            apply_subtype(base_var.get(), subtype_var.get())
