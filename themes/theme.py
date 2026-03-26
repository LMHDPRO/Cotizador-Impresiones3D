"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Sistema de Temas          ║
╚══════════════════════════════════════════╝
"""

THEMES = {
    "dark": {
        # Fondos
        "bg":           "#0a0a0a",
        "bg_sidebar":   "#0d0d0d",
        "bg_card":      "#141414",
        "bg_card2":     "#0f0f0f",
        "bg_input":     "#0d0d0d",
        "bg_hover":     "#1a1a1a",
        "bg_selected":  "#191919",

        # Bordes
        "border":       "#222222",
        "border2":      "#2a2a2a",

        # Textos
        "text":         "#e0e0e0",
        "text_sub":     "#666666",
        "text_dim":     "#444444",
        "text_bright":  "#ffffff",

        # Acento principal
        "accent":       "#ff6b35",
        "accent_hover": "#cc5225",
        "accent_dim":   "#2a1a14",   # 👈 simula transparencia
        "accent_border":"#ff6b35",

        # Semánticos
        "green":        "#4ade80",
        "green_dim":    "#1a2a1f",
        "yellow":       "#fbbf24",
        "yellow_dim":   "#2a2414",
        "blue":         "#60a5fa",
        "blue_dim":     "#1a2230",
        "red":          "#f87171",
        "red_dim":      "#2a1a1a",
        "purple":       "#a78bfa",

        # Marcas
        "bambu":        "#4ade80",
        "creality":     "#60a5fa",
        "elegoo":       "#00d4aa",
        "anycubic":     "#fbbf24",
        "prusa":        "#f97316",
        "flashforge":   "#a78bfa",

        # CTk appearance
        "ctk_mode":     "dark",
        "ctk_theme":    "dark-blue",

        # Scrollbar
        "scrollbar":    "#2a2a2a",

        # Switch/Slider
        "switch_on":    "#ff6b35",
        "slider_accent":"#ff6b35",
        "slider_green": "#4ade80",

        # Botón ghost
        "ghost_border": "#2a2a2a",
        "ghost_text":   "#888888",
        "ghost_hover":  "#1e1e1e",
    },

    "light": {
        # Fondos
        "bg":           "#f0f0f0",
        "bg_sidebar":   "#e8e8e8",
        "bg_card":      "#ffffff",
        "bg_card2":     "#f8f8f8",
        "bg_input":     "#ffffff",
        "bg_hover":     "#eeeeee",
        "bg_selected":  "#e8e8e8",

        # Bordes
        "border":       "#d0d0d0",
        "border2":      "#c0c0c0",

        # Textos
        "text":         "#1a1a1a",
        "text_sub":     "#666666",
        "text_dim":     "#999999",
        "text_bright":  "#000000",

        # Acento principal
        "accent":       "#e85d24",
        "accent_hover": "#c44c1a",
        "accent_dim":   "#f4c2ad",   # 👈 simulado
        "accent_border":"#e85d24",

        # Semánticos
        "green":        "#16a34a",
        "green_dim":    "#d1fae5",
        "yellow":       "#d97706",
        "yellow_dim":   "#fef3c7",
        "blue":         "#2563eb",
        "blue_dim":     "#dbeafe",
        "red":          "#dc2626",
        "red_dim":      "#fee2e2",
        "purple":       "#7c3aed",

        # Marcas
        "bambu":        "#16a34a",
        "creality":     "#2563eb",
        "elegoo":       "#0891b2",
        "anycubic":     "#d97706",
        "prusa":        "#ea580c",
        "flashforge":   "#7c3aed",

        # CTk appearance
        "ctk_mode":     "light",
        "ctk_theme":    "blue",

        # Scrollbar
        "scrollbar":    "#c0c0c0",

        # Switch/Slider
        "switch_on":    "#e85d24",
        "slider_accent":"#e85d24",
        "slider_green": "#16a34a",

        # Botón ghost
        "ghost_border": "#d0d0d0",
        "ghost_text":   "#555555",
        "ghost_hover":  "#e8e8e8",
    }
}

def get_theme(name: str) -> dict:
    return THEMES.get(name, THEMES["dark"])


# ─────────────────────────────────────────
# BRAND COLORS (SIN CAMBIOS)
# ─────────────────────────────────────────

BRAND_COLORS_DARK = {
    "Bambu Lab":    "#4ade80",
    "Creality":     "#60a5fa",
    "Elegoo":       "#00d4aa",
    "Anycubic":     "#fbbf24",
    "Prusa":        "#f97316",
    "Flashforge":   "#a78bfa",
    "Sunlu":        "#60a5fa",
    "Polymaker":    "#f97316",
    "eSUN":         "#fbbf24",
    "Hatchbox":     "#4ade80",
    "Prusament":    "#f97316",
    "Overture":     "#34d399",
    "Genérico":     "#9ca3af",
    "Personalizada":"#9ca3af",
}

BRAND_COLORS_LIGHT = {
    "Bambu Lab":    "#16a34a",
    "Creality":     "#2563eb",
    "Elegoo":       "#0891b2",
    "Anycubic":     "#d97706",
    "Prusa":        "#ea580c",
    "Flashforge":   "#7c3aed",
    "Sunlu":        "#2563eb",
    "Polymaker":    "#ea580c",
    "eSUN":         "#d97706",
    "Hatchbox":     "#16a34a",
    "Prusament":    "#ea580c",
    "Overture":     "#059669",
    "Genérico":     "#6b7280",
    "Personalizada":"#6b7280",
}

def brand_color(brand: str, mode: str = "dark") -> str:
    if mode == "light":
        return BRAND_COLORS_LIGHT.get(brand, "#6b7280")
    return BRAND_COLORS_DARK.get(brand, "#9ca3af")