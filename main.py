#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Backend API para pywebview║
║  pip install pywebview                   ║
║  python main.py                          ║
╚══════════════════════════════════════════╝
"""

import webview
import json
import os
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "ui", "index.html")

FILES = {
    "config":    os.path.join(BASE_DIR, "data", "config.json"),
    "printers":  os.path.join(BASE_DIR, "data", "impresoras.json"),
    "materials": os.path.join(BASE_DIR, "data", "materiales.json"),
    "orders":    os.path.join(BASE_DIR, "data", "ordenes.json"),
}

DEFAULT_CONFIG = {
    "negocio": "Mi Taller 3D",
    "contacto": "",
    "merma": 0.05,
    "margen": 0.15,
    "electricidad_kwh": 0.9,
    "moneda": "MXN",
    "tema": "dark",
    "auto_discount": True,
}

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)


def _load(key, default):
    try:
        with open(FILES[key], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save(key, data):
    with open(FILES[key], "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _calc_item(item, materials, printers, cfg):
    """Calcula costo de una pieza."""
    mat     = next((m for m in materials if m["id"] == item.get("materialId")), None)
    printer = next((p for p in printers  if p["id"] == item.get("printerId")),  None)

    if not mat or not printer:
        return None

    w  = float(item.get("weight", 0))
    t  = float(item.get("time",   0))
    cost_mat  = w * float(mat.get("costPerGram", 0))
    cost_mach = float(printer.get("costPerHour", 0)) * t
    cost_elec = (float(printer.get("avgPowerW", 200)) / 1000) * float(cfg.get("electricidad_kwh", 0.9)) * t
    
    sub   = cost_mat + cost_mach + cost_elec
    sub_m = sub   * (1 + float(cfg.get("merma",   0.05)))
    final = sub_m * (1 + float(cfg.get("margen", 0.15)))
    
    return {
        "costMaterial":  round(cost_mat,  2),
        "costMachine":   round(cost_mach, 2),
        "costElec":      round(cost_elec, 2),
        "subtotal":      round(sub,       2),
        "subtotalMerma": round(sub_m,     2),
        "precioFinal":   round(final,     2),
    }


# ══════════════════════════════════════════════════════════════════
#  API
# ══════════════════════════════════════════════════════════════════

class API:

    # ── Config ────────────────────────────────────────────────────

    def get_config(self):
        cfg = _load("config", dict(DEFAULT_CONFIG))
        return {**DEFAULT_CONFIG, **cfg}

    def save_config(self, data):
        _save("config", data)
        return {"ok": True}

    # ── Impresoras ────────────────────────────────────────────────

    def get_printers(self):
        return _load("printers", [])

    def add_printer(self, data):
        printers = _load("printers", [])
        data["id"] = str(uuid.uuid4())
        printers.append(data)
        _save("printers", printers)
        return {"ok": True, "id": data["id"]}

    def update_printer(self, data):
        printers = _load("printers", [])
        printers = [data if p["id"] == data["id"] else p for p in printers]
        _save("printers", printers)
        return {"ok": True}

    def delete_printer(self, printer_id):
        printers = [p for p in _load("printers", []) if p["id"] != printer_id]
        _save("printers", printers)
        return {"ok": True}

    def toggle_printer(self, printer_id):
        printers = _load("printers", [])
        for p in printers:
            if p["id"] == printer_id:
                p["active"] = not p.get("active", True)
        _save("printers", printers)
        return {"ok": True}

    # ── Materiales ────────────────────────────────────────────────

    def get_materials(self):
        return _load("materials", [])

    def add_material(self, data):
        materials = _load("materials", [])
        data["id"] = str(uuid.uuid4())
        materials.append(data)
        _save("materials", materials)
        return {"ok": True, "id": data["id"]}

    def update_material(self, data):
        materials = _load("materials", [])
        materials = [data if m["id"] == data["id"] else m for m in materials]
        _save("materials", materials)
        return {"ok": True}

    def delete_material(self, mat_id):
        materials = [m for m in _load("materials", []) if m["id"] != mat_id]
        _save("materials", materials)
        return {"ok": True}

    def toggle_archive_material(self, mat_id):
        materials = _load("materials", [])
        for m in materials:
            if m["id"] == mat_id:
                m["archived"] = not m.get("archived", False)
        _save("materials", materials)
        return {"ok": True}

    def discount_material(self, mat_id, grams):
        materials = _load("materials", [])
        for m in materials:
            if m["id"] == mat_id:
                m["usedGrams"] = min(
                    float(m.get("spoolWeight", 1000)),
                    float(m.get("usedGrams", 0)) + float(grams)
                )
        _save("materials", materials)
        return {"ok": True}

    def reset_spool(self, mat_id):
        materials = _load("materials", [])
        for m in materials:
            if m["id"] == mat_id:
                m["usedGrams"] = 0
        _save("materials", materials)
        return {"ok": True}

    # ── Órdenes ───────────────────────────────────────────────────

    def get_orders(self):
        return _load("orders", [])

    def save_order(self, order_data):
        orders = _load("orders", [])
        cfg    = {**DEFAULT_CONFIG, **_load("config", {})}
        order_data["id"]           = str(uuid.uuid4())
        order_data["folio"]        = f"ORD-{len(orders)+1:04d}"
        order_data["createdAt"]    = datetime.now().isoformat()
        order_data["paymentStatus"] = order_data.get("paymentStatus", "unpaid")
        order_data["fabricationStatus"] = order_data.get("fabricationStatus", "fab-pending")
        materials = _load("materials", [])
        printers  = _load("printers",  [])
        total = sum(
            (_calc_item(it, materials, printers, cfg) or {}).get("precioFinal", 0) * int(it.get("qty", 1))
            for it in order_data.get("items", [])
        )
        order_data["total"] = round(total, 2)
        orders.append(order_data)
        _save("orders", orders)
        return {"ok": True, "order": order_data}

    def update_fabrication_status(self, order_id, fab_status):
        orders = _load("orders", [])
        cfg    = {**DEFAULT_CONFIG, **_load("config", {})}
        materials = _load("materials", [])
        
        for o in orders:
            if o["id"] == order_id:
                o["fabricationStatus"] = fab_status
                
                # Descuento Automático de Filamento
                if fab_status in ["fab-done", "fab-shipped"] and cfg.get("auto_discount", True):
                    # Solo descontar si no se ha descontado antes
                    if not o.get("filamentDeducted", False):
                        for item in o.get("items", []):
                            mat_id = item.get("materialId")
                            weight = float(item.get("weight", 0)) * int(item.get("qty", 1))
                            for m in materials:
                                if m["id"] == mat_id:
                                    m["usedGrams"] = min(float(m.get("spoolWeight", 1000)), float(m.get("usedGrams", 0)) + weight)
                        
                        o["filamentDeducted"] = True
                        _save("materials", materials)

        _save("orders", orders)
        return {"ok": True}

    def update_payment_status(self, order_id, pay_status, partial_amount=0):
        orders = _load("orders", [])
        for o in orders:
            if o["id"] == order_id:
                o["paymentStatus"] = pay_status
                if pay_status == "partial":
                    o["partialAmount"] = float(partial_amount)
                else:
                    o["partialAmount"] = 0.0
                
                if pay_status == "cancelled":
                    o["fabricationStatus"] = "cancelled"
                    o["status"] = "cancelled"
                    
        _save("orders", orders)
        return {"ok": True}

    def add_order_note(self, order_id, note):
        orders = _load("orders", [])
        stamp  = f"[{datetime.now().strftime('%d/%m/%Y')}] {note}"
        for o in orders:
            if o["id"] == order_id:
                existing = o.get("notes", "")
                o["notes"] = f"{existing}\n{stamp}".strip()
        _save("orders", orders)
        return {"ok": True}

    def delete_order(self, order_id):
        orders = [o for o in _load("orders", []) if o["id"] != order_id]
        _save("orders", orders)
        return {"ok": True}

    # ── Cálculo ───────────────────────────────────────────────────

    def calc_item(self, item):
        cfg       = {**DEFAULT_CONFIG, **_load("config",    {})}
        materials = _load("materials", [])
        printers  = _load("printers",  [])
        return _calc_item(item, materials, printers, cfg) or {}

    def calc_quote(self, items):
        cfg       = {**DEFAULT_CONFIG, **_load("config",    {})}
        materials = _load("materials", [])
        printers  = _load("printers",  [])
        results = []
        total   = 0.0
        for item in items:
            c = _calc_item(item, materials, printers, cfg)
            if c:
                line_total = c["precioFinal"] * int(item.get("qty", 1))
                total += line_total
                results.append({**c, "lineTotal": round(line_total, 2)})
            else:
                results.append({})
        return {"items": results, "total": round(total, 2)}

    # ── Stats ──────────────────────────────────────────────────────

    def get_stats(self):
        orders    = _load("orders",    [])
        materials = _load("materials", [])
        printers  = _load("printers",  [])
        cfg       = {**DEFAULT_CONFIG, **_load("config", {})}
        
        paid_orders = [o for o in orders if o.get("paymentStatus") == "paid"]
        low_stock = [
            m for m in materials
            if (float(m.get("spoolWeight", 1000)) - float(m.get("usedGrams", 0)))
               / max(float(m.get("spoolWeight", 1000)), 1) < 0.20 and not m.get("archived", False)
        ]
        revenue   = sum(o.get("total", 0) for o in paid_orders)
        
        return {
            "totalOrders":    len(orders),
            "revenue":        round(revenue, 2),
            "activePrinters": sum(1 for p in printers if p.get("active", True)),
            "totalPrinters":  len(printers),
            "totalMaterials": len(materials),
            "lowStock":       len(low_stock),
            "moneda":         cfg.get("moneda", "MXN"),
        }

    # ── Catálogos ─────────────────────────────────────────────────

    def get_catalogs(self):
        from data.constants import PRINTER_BRANDS, FILAMENT_BRANDS, FILAMENT_TYPES, FILAMENT_COLORS, AMS_TYPES
        return {
            "printerBrands":  PRINTER_BRANDS,
            "filamentBrands": FILAMENT_BRANDS,
            "filamentTypes":  FILAMENT_TYPES,
            "filamentColors": FILAMENT_COLORS,
            "amsTypes":       AMS_TYPES,
        }


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    api    = API()
    window = webview.create_window(
        title            = "⬡ Print3D Pro",
        url              = HTML_FILE,
        js_api           = api,
        width            = 1440,
        height           = 900,
        min_size         = (1100, 680),
        resizable        = True,
        background_color = "#0a0a0a",
    )
    webview.start(debug=False)