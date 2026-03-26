"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Persistencia y Cálculos   ║
╚══════════════════════════════════════════╝
"""

import json
import os
import uuid
from datetime import datetime
from data.constants import DEFAULT_CONFIG

# ─── RUTAS DE ARCHIVOS ────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILES = {
    "config":    os.path.join(BASE_DIR, "config.json"),
    "printers":  os.path.join(BASE_DIR, "impresoras.json"),
    "materials": os.path.join(BASE_DIR, "materiales.json"),
    "orders":    os.path.join(BASE_DIR, "ordenes.json"),
}

# ─── CARGA / GUARDADO ─────────────────────────────────────────────

def load(key: str, default):
    """Carga datos desde JSON, regresa `default` si falla."""
    try:
        with open(DATA_FILES[key], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(key: str, data) -> bool:
    """Guarda datos a JSON. Regresa True si exitoso."""
    try:
        with open(DATA_FILES[key], "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo guardar {key}: {e}")
        return False


# ─── MOTOR DE CÁLCULO ─────────────────────────────────────────────

def calc_item(item: dict, materials: list, printers: list, cfg: dict) -> dict | None:
    """
    Calcula costos de una pieza.
    Retorna dict con desglose o None si faltan datos.
    """
    mat = next((m for m in materials if m["id"] == item.get("materialId")), None)
    printer = next((p for p in printers if p["id"] == item.get("printerId")), None)

    if not mat or not printer:
        return None

    weight = float(item.get("weight", 0))
    time_h = float(item.get("time", 0))

    cost_mat   = weight * float(mat.get("costPerGram", 0))
    cost_mach  = float(printer.get("costPerHour", 0)) * time_h
    kwh        = float(printer.get("avgPowerW", 200)) / 1000
    cost_elec  = kwh * float(cfg.get("electricidad_kwh", 0.9)) * time_h

    # Extras multicolor (purgado)
    multi_extra = 0.0
    for layer in item.get("multicolorLayers", []):
        lmat = next((m for m in materials if m["id"] == layer.get("materialId")), None)
        if lmat:
            multi_extra += float(layer.get("purgeGrams", 5)) * float(lmat.get("costPerGram", 0))

    subtotal       = cost_mat + cost_mach + multi_extra
    subtotal_merma = subtotal * (1.0 + float(cfg.get("merma", 0.05)))
    precio_final   = subtotal_merma * (1.0 + float(cfg.get("margen", 0.15)))

    return {
        "costMaterial":   round(cost_mat, 2),
        "costMachine":    round(cost_mach, 2),
        "costElec":       round(cost_elec, 2),
        "multiExtra":     round(multi_extra, 2),
        "subtotal":       round(subtotal, 2),
        "subtotalMerma":  round(subtotal_merma, 2),
        "precioFinal":    round(precio_final, 2),
    }


def calc_order_total(order: dict, materials: list, printers: list, cfg: dict) -> float:
    """Suma el total de todos los ítems de una orden."""
    total = 0.0
    for item in order.get("items", []):
        c = calc_item(item, materials, printers, cfg)
        if c:
            total += c["precioFinal"] * int(item.get("qty", 1))
    return round(total, 2)


# ─── FORMATEO ─────────────────────────────────────────────────────

def fmt(value: float, currency: str = "MXN") -> str:
    """Formatea un número como precio con moneda."""
    try:
        return f"${value:,.2f} {currency}"
    except Exception:
        return f"$0.00 {currency}"


def fmt_short(value: float) -> str:
    """Formatea número sin moneda."""
    try:
        return f"{value:,.2f}"
    except Exception:
        return "0.00"


# ─── GENERADORES DE IDs ───────────────────────────────────────────

def new_id() -> str:
    return str(uuid.uuid4())


def new_order_folio(orders: list) -> str:
    """Genera un folio legible tipo ORD-0042."""
    n = len(orders) + 1
    return f"ORD-{n:04d}"


# ─── VALIDACIÓN BÁSICA ────────────────────────────────────────────

def validate_printer(data: dict) -> list[str]:
    errors = []
    if not data.get("name", "").strip():
        errors.append("El nombre de la impresora es requerido.")
    if float(data.get("costPerHour", 0)) < 0:
        errors.append("El costo por hora no puede ser negativo.")
    return errors


def validate_material(data: dict) -> list[str]:
    errors = []
    if not data.get("name", "").strip():
        errors.append("El nombre del material es requerido.")
    if float(data.get("costPerGram", 0)) <= 0:
        errors.append("El costo por gramo debe ser mayor a 0.")
    if float(data.get("spoolWeight", 0)) <= 0:
        errors.append("El peso del carrete debe ser mayor a 0.")
    return errors


# ─── ESTADÍSTICAS RÁPIDAS ─────────────────────────────────────────

def get_stats(orders: list, materials: list, printers: list, cfg: dict) -> dict:
    """Genera estadísticas para el dashboard."""
    completed = [o for o in orders if o.get("status") == "completed"]
    pending   = [o for o in orders if o.get("status") == "pending"]
    inprog    = [o for o in orders if o.get("status") == "in-progress"]

    revenue  = sum(o.get("total", 0) for o in completed)
    expected = sum(o.get("total", 0) for o in pending + inprog)

    active_printers = sum(1 for p in printers if p.get("active", True))

    low_stock = [m for m in materials
                 if (m.get("spoolWeight", 1000) - m.get("usedGrams", 0)) / max(m.get("spoolWeight", 1000), 1) < 0.2]

    return {
        "total_orders":      len(orders),
        "pending":           len(pending),
        "in_progress":       len(inprog),
        "completed":         len(completed),
        "revenue":           revenue,
        "expected":          expected,
        "active_printers":   active_printers,
        "total_printers":    len(printers),
        "total_materials":   len(materials),
        "low_stock_mats":    len(low_stock),
    }
