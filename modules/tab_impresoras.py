"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Módulo: Impresoras        ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from modules.widgets import (
    Card, SubCard, ScrollArea, Divider,
    Label, SectionTitle, PageHeader, Tag,
    Entry, Dropdown, BtnPrimary, BtnGhost, BtnDanger, BtnSuccess,
    T, font, confirm
)
from data.store import new_id
from data.constants import PRINTER_BRANDS, AMS_TYPES
from themes.theme import brand_color


class ImpresorasTab(ctk.CTkFrame):
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
        Label(hdr, "Impresoras", size=26, bold=True,
              color=T("text_bright")).pack(side="left")
        lbl_sub = Label(hdr,
                        f"{len(self.app.printers)} perfiles  ·  {sum(1 for p in self.app.printers if p.get('active',True))} activas",
                        size=12, color=T("text_sub"))
        lbl_sub.pack(side="left", padx=14, pady=(6, 0))
        BtnPrimary(hdr, "Nueva Impresora", self._add_new,
                   icon="＋", width=170).pack(side="right")

        scroll = ScrollArea(self)
        scroll.pack(fill="both", expand=True, padx=30, pady=14)

        if not self.app.printers:
            Label(scroll, "Sin impresoras. Agrega la primera →",
                  size=14, color=T("text_sub")).pack(pady=60)
            return

        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        for i, p in enumerate(self.app.printers):
            row, col = divmod(i, 2)
            pc = Card(grid)
            pc.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            self._render_printer_card(pc, p)

    def _render_printer_card(self, parent, p):
        active = p.get("active", True)
        brand  = p.get("brand", "Personalizada")
        bc     = brand_color(brand, self.app.theme_mode)

        # Header
        hr = ctk.CTkFrame(parent, fg_color="transparent")
        hr.pack(fill="x", padx=14, pady=(14, 8))

        tag_row = ctk.CTkFrame(hr, fg_color="transparent")
        tag_row.pack(anchor="w", pady=(0, 6))
        Tag(tag_row, brand or "Custom", bc).pack(side="left")
        if p.get("multicolor"):
            Tag(tag_row, f"🎨 {p.get('amsType','AMS')}  {p.get('colors',1)} col.",
                T("accent")).pack(side="left", padx=4)
        Tag(tag_row, p.get("type", "CoreXY"), T("text_sub")).pack(side="left", padx=4)

        btn_row = ctk.CTkFrame(hr, fg_color="transparent")
        btn_row.pack(side="right")

        # Botón activa/inactiva
        act_color = T("green") if active else T("red")
        act_text  = "● Activa" if active else "○ Inactiva"
        BtnGhost(btn_row, act_text,
                 lambda pid=p["id"]: self._toggle(pid),
                 width=90, color=act_color).pack(side="left", padx=3)
        BtnGhost(btn_row, "✏️",
                 lambda pid=p["id"]: self._edit(pid), width=38).pack(side="left", padx=3)
        BtnDanger(btn_row, "🗑️",
                  lambda pid=p["id"]: self._delete(pid), width=38).pack(side="left", padx=3)

        # Nombre
        Label(hr, p.get("name", "—"), size=16, bold=True).pack(anchor="w")

        # Info grid
        bv = p.get("buildVolume", {})
        info_grid = ctk.CTkFrame(parent, fg_color="transparent")
        info_grid.pack(fill="x", padx=14, pady=(0, 14))

        infos = [
            ("Volumen",     f"{bv.get('x',0)}×{bv.get('y',0)}×{bv.get('z',0)} mm"),
            ("Vel. máx.",   f"{p.get('maxSpeed',0)} mm/s"),
            ("Costo/hora",  f"${p.get('costPerHour',0):.2f}"),
            ("Consumo avg", f"{p.get('avgPowerW',0)} W"),
            ("Temp. ext.",  f"{p.get('maxTemp',0)}°C"),
            ("Temp. cama",  f"{p.get('bedTemp',0)}°C"),
        ]
        for j, (k, v) in enumerate(infos):
            row2 = j // 3
            col2 = j % 3
            ic = ctk.CTkFrame(info_grid,
                               fg_color=T("bg_card2"),
                               corner_radius=7,
                               border_width=1,
                               border_color=T("border"))
            ic.grid(row=row2, column=col2, padx=3, pady=3, sticky="ew")
            info_grid.columnconfigure(col2, weight=1)
            Label(ic, k, size=10, color=T("text_sub")).pack(anchor="w", padx=8, pady=(6, 1))
            Label(ic, v, size=12, bold=True).pack(anchor="w", padx=8, pady=(0, 6))

        if p.get("notes"):
            Label(parent, p["notes"], size=11,
                  color=T("text_dim")).pack(anchor="w", padx=14, pady=(0, 12))

    # ─────────────────────────────────────────────────────────
    # ACCIONES
    # ─────────────────────────────────────────────────────────

    def _toggle(self, pid):
        for p in self.app.printers:
            if p["id"] == pid:
                p["active"] = not p.get("active", True)
        self.app.save_printers()
        self.refresh()
        if "dashboard" in self.app.frames:
            self.app.frames["dashboard"].refresh()

    def _delete(self, pid):
        p = next((p for p in self.app.printers if p["id"] == pid), None)
        name = p["name"] if p else "esta impresora"
        if not confirm(self, "Eliminar impresora", f"¿Eliminar '{name}'? Esta acción no se puede deshacer."):
            return
        self.app.printers = [p for p in self.app.printers if p["id"] != pid]
        self.app.save_printers()
        self.app.toast("🗑️ Impresora eliminada")
        self.refresh()

    def _add_new(self):
        self._open_editor(None)

    def _edit(self, pid):
        p = next((p for p in self.app.printers if p["id"] == pid), None)
        if p:
            self._open_editor(p)

    # ─────────────────────────────────────────────────────────
    # EDITOR MODAL
    # ─────────────────────────────────────────────────────────

    def _open_editor(self, printer):
        is_new = printer is None
        if is_new:
            printer = {
                "id": new_id(), "name": "", "brand": "Bambu Lab",
                "model": "", "type": "CoreXY",
                "buildVolume": {"x": 256, "y": 256, "z": 256},
                "maxSpeed": 500, "maxTemp": 300, "bedTemp": 120,
                "avgPowerW": 350, "costPerHour": 4.0,
                "multicolor": False, "colors": 1, "amsType": "Single",
                "materials": ["PLA", "PETG"],
                "notes": "", "active": True,
            }

        dlg = ctk.CTkToplevel(self)
        dlg.title("Nueva Impresora" if is_new else f"Editar — {printer['name']}")
        dlg.geometry("620x700")
        dlg.configure(fg_color=T("bg"))
        dlg.grab_set()
        dlg.resizable(True, True)

        sf = ctk.CTkScrollableFrame(dlg, fg_color=T("bg"),
                                     scrollbar_button_color=T("scrollbar"),
                                     scrollbar_button_hover_color=T("text_sub"))
        sf.pack(fill="both", expand=True, padx=22, pady=18)

        Label(sf, "Nueva Impresora" if is_new else "Editar Impresora",
              size=18, bold=True, color=T("text_bright")).pack(anchor="w", pady=(0, 16))

        vars_ = {}

        # ── Marca y Modelo ──────────────────────────────────
        brand_card = Card(sf)
        brand_card.pack(fill="x", pady=(0, 12))
        SectionTitle(brand_card, "🏭  MARCA Y MODELO")

        brand_row = ctk.CTkFrame(brand_card, fg_color="transparent")
        brand_row.pack(fill="x", padx=16, pady=(0, 14))
        brand_row.columnconfigure(0, weight=1)
        brand_row.columnconfigure(1, weight=2)

        # Marca
        bf = ctk.CTkFrame(brand_row, fg_color="transparent")
        bf.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        Label(bf, "Marca", size=11, color=T("text_sub")).pack(anchor="w")
        brand_names = list(PRINTER_BRANDS.keys())
        brand_var = ctk.StringVar(value=printer.get("brand", "Bambu Lab"))
        vars_["brand"] = brand_var

        # Modelo
        mf = ctk.CTkFrame(brand_row, fg_color="transparent")
        mf.grid(row=0, column=1, sticky="ew")
        Label(mf, "Modelo", size=11, color=T("text_sub")).pack(anchor="w")

        model_names_var = ctk.StringVar(value=printer.get("model", ""))
        vars_["model"] = model_names_var

        # Preview specs
        specs_label = Label(sf, "", size=11, color=T("text_sub"))
        specs_label.pack(anchor="w", padx=16, pady=(0, 8))

        # Nombre personalizado
        nc = ctk.CTkFrame(brand_card, fg_color="transparent")
        nc.pack(fill="x", padx=16, pady=(0, 14))
        Label(nc, "Nombre para mostrar (editable)", size=11, color=T("text_sub")).pack(anchor="w")
        name_var = ctk.StringVar(value=printer.get("name", ""))
        vars_["name"] = name_var
        Entry(nc, textvariable=name_var, placeholder_text="Ej: Mi X1C del taller").pack(fill="x")

        # ── Actualizar modelos al cambiar marca ──────────────
        model_dd_holder = [None]
        cost_var   = ctk.StringVar(value=str(printer.get("costPerHour", 4.0)))
        avg_pw_var = ctk.StringVar(value=str(printer.get("avgPowerW", 350)))
        bv_x = ctk.StringVar(value=str(printer.get("buildVolume", {}).get("x", 256)))
        bv_y = ctk.StringVar(value=str(printer.get("buildVolume", {}).get("y", 256)))
        bv_z = ctk.StringVar(value=str(printer.get("buildVolume", {}).get("z", 256)))
        max_speed_var  = ctk.StringVar(value=str(printer.get("maxSpeed", 500)))
        max_temp_var   = ctk.StringVar(value=str(printer.get("maxTemp", 300)))
        bed_temp_var   = ctk.StringVar(value=str(printer.get("bedTemp", 120)))
        mc_var         = ctk.BooleanVar(value=printer.get("multicolor", False))
        colors_var     = ctk.StringVar(value=str(printer.get("colors", 1)))
        ams_var        = ctk.StringVar(value=printer.get("amsType", "Single"))
        type_var       = ctk.StringVar(value=printer.get("type", "CoreXY"))
        notes_var      = ctk.StringVar(value=printer.get("notes", ""))

        vars_.update({
            "costPerHour": cost_var,
            "avgPowerW":   avg_pw_var,
            "bv_x": bv_x, "bv_y": bv_y, "bv_z": bv_z,
            "maxSpeed": max_speed_var,
            "maxTemp":  max_temp_var,
            "bedTemp":  bed_temp_var,
            "multicolor": mc_var,
            "colors":   colors_var,
            "amsType":  ams_var,
            "type":     type_var,
            "notes":    notes_var,
        })

        def apply_preset(brand: str, model: str):
            try:
                specs = PRINTER_BRANDS[brand]["models"][model]
                cost_var.set(str(specs["costPerHour"]))
                avg_pw_var.set(str(specs["avgPowerW"]))
                bv_x.set(str(specs["buildVolume"]["x"]))
                bv_y.set(str(specs["buildVolume"]["y"]))
                bv_z.set(str(specs["buildVolume"]["z"]))
                max_speed_var.set(str(specs["maxSpeed"]))
                max_temp_var.set(str(specs["maxTemp"]))
                bed_temp_var.set(str(specs["bedTemp"]))
                mc_var.set(specs["multicolor"])
                colors_var.set(str(specs["colors"]))
                ams_var.set(specs["amsType"])
                type_var.set(specs["type"])
                notes_var.set(specs["notes"])
                # Nombre auto
                if not name_var.get():
                    name_var.set(f"{brand} {model}")
                specs_label.configure(
                    text=f"✓ Specs cargadas: {specs['buildVolume']['x']}×"
                         f"{specs['buildVolume']['y']}×{specs['buildVolume']['z']}mm  "
                         f"·  {specs['maxSpeed']}mm/s  ·  {specs['avgPowerW']}W",
                    text_color=T("green"),
                )
            except KeyError:
                pass

        def update_models(brand: str):
            models = list(PRINTER_BRANDS.get(brand, {}).get("models", {}).keys())
            if model_dd_holder[0]:
                model_dd_holder[0].configure(values=models)
                if models:
                    model_names_var.set(models[0])
                    apply_preset(brand, models[0])

        def on_brand(ch):
            vars_["brand"].set(ch)
            update_models(ch)

        def on_model(ch):
            brand = vars_["brand"].get()
            apply_preset(brand, ch)

        # Crear dropdowns
        brand_dd = Dropdown(bf, brand_names, variable=brand_var, command=on_brand, width=160)
        brand_dd.pack()

        cur_brand = printer.get("brand", "Bambu Lab")
        cur_models = list(PRINTER_BRANDS.get(cur_brand, {}).get("models", {}).keys())
        model_dd = Dropdown(mf, cur_models or ["Personalizada"],
                            variable=model_names_var, command=on_model, width=210)
        model_dd.pack()
        model_dd_holder[0] = model_dd

        # Si es nueva, cargar specs del preset inicial
        if is_new and cur_models:
            apply_preset(cur_brand, cur_models[0])

        # ── Parámetros técnicos ─────────────────────────────
        tech_card = Card(sf)
        tech_card.pack(fill="x", pady=(0, 12))
        SectionTitle(tech_card, "⚙️  PARÁMETROS TÉCNICOS")

        tech_grid = ctk.CTkFrame(tech_card, fg_color="transparent")
        tech_grid.pack(fill="x", padx=16, pady=(0, 14))
        for i in range(3):
            tech_grid.columnconfigure(i, weight=1)

        tech_fields = [
            ("costPerHour",  cost_var,      "Costo / hora ($)",       0, 0),
            ("avgPowerW",    avg_pw_var,    "Consumo promedio (W)",   0, 1),
            ("type",         type_var,      "Tipo de cinemática",     0, 2),
            ("maxSpeed",     max_speed_var, "Vel. máx. (mm/s)",       1, 0),
            ("maxTemp",      max_temp_var,  "Temp. ext. máx. (°C)",   1, 1),
            ("bedTemp",      bed_temp_var,  "Temp. cama máx. (°C)",   1, 2),
        ]
        for k, v, lbl_text, row, col in tech_fields:
            f = ctk.CTkFrame(tech_grid, fg_color="transparent")
            f.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            Label(f, lbl_text, size=11, color=T("text_sub")).pack(anchor="w")
            if k == "type":
                Dropdown(f, ["CoreXY", "Cartesiana", "Delta", "SCARA", "Polar"],
                         variable=v, width=160).pack(fill="x")
            else:
                Entry(f, textvariable=v).pack(fill="x")

        # Volumen
        bv_row2 = ctk.CTkFrame(tech_card, fg_color="transparent")
        bv_row2.pack(fill="x", padx=16, pady=(0, 14))
        Label(bv_row2, "Volumen de construcción (mm)", size=11,
              color=T("text_sub")).pack(anchor="w", pady=(0, 4))
        bv_inner = ctk.CTkFrame(bv_row2, fg_color="transparent")
        bv_inner.pack(anchor="w")
        for axis, var in [("X", bv_x), ("Y", bv_y), ("Z", bv_z)]:
            af = ctk.CTkFrame(bv_inner, fg_color="transparent")
            af.pack(side="left", padx=(0, 10))
            Label(af, axis, size=11, color=T("text_sub")).pack(anchor="w")
            Entry(af, textvariable=var, width=80).pack()

        # ── Multicolor ───────────────────────────────────────
        mc_card = Card(sf)
        mc_card.pack(fill="x", pady=(0, 12))
        SectionTitle(mc_card, "🎨  SISTEMA MULTICOLOR / MULTI-MATERIAL")

        mc_inner = ctk.CTkFrame(mc_card, fg_color="transparent")
        mc_inner.pack(fill="x", padx=16, pady=(0, 14))
        mc_inner.columnconfigure(0, weight=2)
        mc_inner.columnconfigure(1, weight=1)
        mc_inner.columnconfigure(2, weight=1)

        cf = ctk.CTkFrame(mc_inner, fg_color="transparent")
        cf.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        Label(cf, "Activo", size=11, color=T("text_sub")).pack(anchor="w")
        ctk.CTkSwitch(cf, text="", variable=mc_var,
                      progress_color=T("accent"),
                      button_color=T("accent")).pack(anchor="w", pady=(4, 0))

        sf2 = ctk.CTkFrame(mc_inner, fg_color="transparent")
        sf2.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        Label(sf2, "Slots / Colores", size=11, color=T("text_sub")).pack(anchor="w")
        Entry(sf2, textvariable=colors_var, width=70).pack(anchor="w")

        af = ctk.CTkFrame(mc_inner, fg_color="transparent")
        af.grid(row=0, column=2, sticky="ew")
        Label(af, "Sistema AMS / Multi", size=11, color=T("text_sub")).pack(anchor="w")
        Dropdown(af, AMS_TYPES, variable=ams_var, width=150).pack(anchor="w")

        # ── Notas ────────────────────────────────────────────
        nt_card = Card(sf)
        nt_card.pack(fill="x", pady=(0, 12))
        SectionTitle(nt_card, "📝  NOTAS")
        Entry(nt_card, textvariable=notes_var,
              placeholder_text="Notas adicionales, características especiales…").pack(
            fill="x", padx=16, pady=(0, 14))

        # ── Botones ──────────────────────────────────────────
        btn_row = ctk.CTkFrame(sf, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))

        def save():
            try:
                data = {
                    "id":    printer["id"],
                    "name":  vars_["name"].get().strip() or f"{vars_['brand'].get()} {vars_['model'].get()}",
                    "brand": vars_["brand"].get(),
                    "model": vars_["model"].get(),
                    "type":  vars_["type"].get(),
                    "buildVolume": {
                        "x": float(vars_["bv_x"].get()),
                        "y": float(vars_["bv_y"].get()),
                        "z": float(vars_["bv_z"].get()),
                    },
                    "maxSpeed":    float(vars_["maxSpeed"].get()),
                    "maxTemp":     float(vars_["maxTemp"].get()),
                    "bedTemp":     float(vars_["bedTemp"].get()),
                    "avgPowerW":   float(vars_["avgPowerW"].get()),
                    "costPerHour": float(vars_["costPerHour"].get()),
                    "multicolor":  vars_["multicolor"].get(),
                    "colors":      int(vars_["colors"].get()),
                    "amsType":     vars_["amsType"].get(),
                    "notes":       vars_["notes"].get(),
                    "active":      printer.get("active", True),
                }
                if is_new:
                    self.app.printers.append(data)
                else:
                    self.app.printers = [
                        data if p["id"] == data["id"] else p
                        for p in self.app.printers
                    ]
                self.app.save_printers()
                self.app.toast("✅ Impresora guardada")
                dlg.destroy()
                self.refresh()
                if "dashboard" in self.app.frames:
                    self.app.frames["dashboard"].refresh()
            except ValueError as e:
                self.app.toast(f"⚠️ Valor inválido: {e}", ok=False)

        BtnPrimary(btn_row, "Guardar", save, icon="💾", width=140).pack(side="left")
        BtnGhost(btn_row, "Cancelar", dlg.destroy, width=110).pack(side="left", padx=12)
