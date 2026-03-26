"""
╔══════════════════════════════════════════════════════════╗
║  Print3D Pro — Base de datos de impresoras y filamentos  ║
╚══════════════════════════════════════════════════════════╝
"""

# ─── IMPRESORAS POR MARCA ──────────────────────────────────────────

PRINTER_BRANDS = {
    "Bambu Lab": {
        "logo": "bambu.png",
        "color": "#4ade80",
        "models": {
            "X1 Carbon": {
                "type": "CoreXY",
                "buildVolume": {"x": 256, "y": 256, "z": 256},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 120,
                "avgPowerW": 400,
                "costPerHour": 5.0,
                "multicolor": True,
                "colors": 4,
                "amsType": "AMS",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC"],
                "notes": "AMS hasta 4 materiales simultáneos. Cámara con AI.",
            },
            "P1S": {
                "type": "CoreXY",
                "buildVolume": {"x": 256, "y": 256, "z": 256},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 120,
                "avgPowerW": 380,
                "costPerHour": 4.5,
                "multicolor": True,
                "colors": 4,
                "amsType": "AMS",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC"],
                "notes": "Cámara cerrada, ideal para materiales técnicos.",
            },
            "P1P": {
                "type": "CoreXY",
                "buildVolume": {"x": 256, "y": 256, "z": 256},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 110,
                "avgPowerW": 350,
                "costPerHour": 4.0,
                "multicolor": True,
                "colors": 4,
                "amsType": "AMS",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU"],
                "notes": "Open frame. AMS compatible.",
            },
            "A1": {
                "type": "Cartesiana",
                "buildVolume": {"x": 256, "y": 256, "z": 256},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 80,
                "avgPowerW": 280,
                "costPerHour": 3.5,
                "multicolor": True,
                "colors": 4,
                "amsType": "AMS Lite",
                "materials": ["PLA", "PETG", "TPU"],
                "notes": "AMS Lite, 4 colores. Ideal PLA multicolor.",
            },
            "A1 Mini": {
                "type": "Cartesiana",
                "buildVolume": {"x": 180, "y": 180, "z": 180},
                "maxSpeed": 500,
                "maxTemp": 280,
                "bedTemp": 80,
                "avgPowerW": 220,
                "costPerHour": 3.0,
                "multicolor": True,
                "colors": 4,
                "amsType": "AMS Lite",
                "materials": ["PLA", "PETG", "TPU"],
                "notes": "Compacta con AMS Lite. Perfecta para escritorio.",
            },
        }
    },
    "Creality": {
        "logo": "creality.png",
        "color": "#60a5fa",
        "models": {
            "Ender 3 V3 SE": {
                "type": "Cartesiana",
                "buildVolume": {"x": 220, "y": 220, "z": 250},
                "maxSpeed": 250,
                "maxTemp": 260,
                "bedTemp": 100,
                "avgPowerW": 165,
                "costPerHour": 1.8,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "TPU"],
                "notes": "Auto-nivelación CR Touch. Entrada al mundo 3D.",
            },
            "Ender 3 S1 Pro": {
                "type": "Cartesiana",
                "buildVolume": {"x": 220, "y": 220, "z": 270},
                "maxSpeed": 150,
                "maxTemp": 300,
                "bedTemp": 100,
                "avgPowerW": 180,
                "costPerHour": 2.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA"],
                "notes": "Extrusor directo Sprite Pro. Pantalla táctil.",
            },
            "Ender 3 V3 KE": {
                "type": "CoreXY",
                "buildVolume": {"x": 220, "y": 220, "z": 240},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 90,
                "avgPowerW": 220,
                "costPerHour": 2.5,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "TPU"],
                "notes": "CoreXY compacto alta velocidad. Auto-nivelación.",
            },
            "K1 Max": {
                "type": "CoreXY",
                "buildVolume": {"x": 300, "y": 300, "z": 300},
                "maxSpeed": 600,
                "maxTemp": 300,
                "bedTemp": 120,
                "avgPowerW": 350,
                "costPerHour": 4.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA"],
                "notes": "Gran volumen, alta velocidad. Cámara cerrada.",
            },
            "K2 Plus Combo": {
                "type": "CoreXY",
                "buildVolume": {"x": 350, "y": 350, "z": 350},
                "maxSpeed": 600,
                "maxTemp": 320,
                "bedTemp": 120,
                "avgPowerW": 420,
                "costPerHour": 5.0,
                "multicolor": True,
                "colors": 4,
                "amsType": "CFS",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC"],
                "notes": "CFS 4 colores. Enorme volumen de impresión.",
            },
        }
    },
    "Elegoo": {
        "logo": "elegoo.png",
        "color": "#00d4aa",
        "models": {
            "Neptune 4 Pro": {
                "type": "Cartesiana",
                "buildVolume": {"x": 225, "y": 225, "z": 265},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 110,
                "avgPowerW": 240,
                "costPerHour": 2.5,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA"],
                "notes": "Klipper integrado. Velocidad competitiva.",
            },
            "Neptune 4 Max": {
                "type": "Cartesiana",
                "buildVolume": {"x": 420, "y": 420, "z": 480},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 110,
                "avgPowerW": 400,
                "costPerHour": 4.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU"],
                "notes": "Volumen gigante para piezas grandes.",
            },
            "Centauri 2": {
                "type": "CoreXY",
                "buildVolume": {"x": 350, "y": 350, "z": 350},
                "maxSpeed": 500,
                "maxTemp": 300,
                "bedTemp": 120,
                "avgPowerW": 380,
                "costPerHour": 4.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA"],
                "notes": "350³mm, CoreXY de alto rendimiento.",
            },
        }
    },
    "Anycubic": {
        "logo": "anycubic.png",
        "color": "#fbbf24",
        "models": {
            "Kobra 2 Pro": {
                "type": "Cartesiana",
                "buildVolume": {"x": 220, "y": 220, "z": 250},
                "maxSpeed": 500,
                "maxTemp": 260,
                "bedTemp": 90,
                "avgPowerW": 200,
                "costPerHour": 2.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "TPU"],
                "notes": "LeviQ 2.0 auto-leveling. Precio/calidad excelente.",
            },
            "Kobra 2 Max": {
                "type": "Cartesiana",
                "buildVolume": {"x": 420, "y": 420, "z": 500},
                "maxSpeed": 500,
                "maxTemp": 260,
                "bedTemp": 90,
                "avgPowerW": 380,
                "costPerHour": 3.5,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "TPU"],
                "notes": "Formato gigante para proyectos grandes.",
            },
            "Kobra 3 Combo": {
                "type": "Cartesiana",
                "buildVolume": {"x": 250, "y": 250, "z": 260},
                "maxSpeed": 600,
                "maxTemp": 260,
                "bedTemp": 90,
                "avgPowerW": 280,
                "costPerHour": 3.0,
                "multicolor": True,
                "colors": 4,
                "amsType": "ACE Pro",
                "materials": ["PLA", "PETG", "TPU"],
                "notes": "ACE Pro 4 colores simultáneos.",
            },
        }
    },
    "Prusa": {
        "logo": "prusa.png",
        "color": "#f97316",
        "models": {
            "MK4S": {
                "type": "Cartesiana",
                "buildVolume": {"x": 250, "y": 210, "z": 220},
                "maxSpeed": 200,
                "maxTemp": 290,
                "bedTemp": 100,
                "avgPowerW": 240,
                "costPerHour": 3.5,
                "multicolor": True,
                "colors": 5,
                "amsType": "MMU3",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC"],
                "notes": "MMU3 hasta 5 materiales. Confiabilidad legendaria.",
            },
            "MINI+": {
                "type": "Cartesiana",
                "buildVolume": {"x": 180, "y": 180, "z": 180},
                "maxSpeed": 180,
                "maxTemp": 280,
                "bedTemp": 100,
                "avgPowerW": 120,
                "costPerHour": 2.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU"],
                "notes": "Compacta de alta calidad. Ideal para piezas pequeñas.",
            },
            "XL": {
                "type": "CoreXY",
                "buildVolume": {"x": 360, "y": 360, "z": 360},
                "maxSpeed": 500,
                "maxTemp": 290,
                "bedTemp": 120,
                "avgPowerW": 400,
                "costPerHour": 5.5,
                "multicolor": True,
                "colors": 5,
                "amsType": "Multi-Tool",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC"],
                "notes": "Multi-tool hasta 5 cabezales. Máxima versatilidad.",
            },
        }
    },
    "Flashforge": {
        "logo": "flashforge.png",
        "color": "#a78bfa",
        "models": {
            "Adventurer 5M Pro": {
                "type": "CoreXY",
                "buildVolume": {"x": 220, "y": 220, "z": 220},
                "maxSpeed": 600,
                "maxTemp": 280,
                "bedTemp": 110,
                "avgPowerW": 300,
                "costPerHour": 3.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU"],
                "notes": "Alta velocidad con cámara cerrada.",
            },
            "Creator 4S": {
                "type": "Cartesiana",
                "buildVolume": {"x": 400, "y": 350, "z": 500},
                "maxSpeed": 150,
                "maxTemp": 360,
                "bedTemp": 120,
                "avgPowerW": 600,
                "costPerHour": 6.0,
                "multicolor": True,
                "colors": 2,
                "amsType": "IDEX",
                "materials": ["PLA", "PETG", "ABS", "ASA", "TPU", "PA", "PC", "PEI"],
                "notes": "IDEX doble extrusor. Materiales técnicos avanzados.",
            },
        }
    },
    "Personalizada": {
        "logo": None,
        "color": "#9ca3af",
        "models": {
            "Personalizada": {
                "type": "CoreXY",
                "buildVolume": {"x": 220, "y": 220, "z": 250},
                "maxSpeed": 200,
                "maxTemp": 260,
                "bedTemp": 100,
                "avgPowerW": 200,
                "costPerHour": 2.0,
                "multicolor": False,
                "colors": 1,
                "amsType": "Single",
                "materials": ["PLA", "PETG"],
                "notes": "",
            }
        }
    }
}

AMS_TYPES = ["Single", "AMS", "AMS Lite", "ACE Pro", "MMU3", "CFS", "IDEX", "Multi-Tool", "Canvas Hub"]

# ─── FILAMENTOS ───────────────────────────────────────────────────

FILAMENT_BRANDS = {
    "Bambu Lab": {
        "logo": "bambu.png",
        "color": "#4ade80",
    },
    "Sunlu": {
        "logo": "sunlu.png",
        "color": "#60a5fa",
    },
    "Polymaker": {
        "logo": "polymaker.png",
        "color": "#f97316",
    },
    "eSUN": {
        "logo": "esun.png",
        "color": "#fbbf24",
    },
    "Hatchbox": {
        "logo": "hatchbox.png",
        "color": "#a78bfa",
    },
    "Prusament": {
        "logo": "prusament.png",
        "color": "#f97316",
    },
    "Overture": {
        "logo": "overture.png",
        "color": "#34d399",
    },
    "Genérico": {
        "logo": None,
        "color": "#9ca3af",
    },
}

# Base types → subtypes with specs
FILAMENT_TYPES = {
    "PLA": {
        "color": "#4CAF50",
        "subtypes": {
            "Estándar": {
                "density": 1.24, "printTemp": 200, "bedTemp": 60,
                "costPerGram": 0.28, "notes": "Material más popular. Fácil de imprimir.",
            },
            "PLA+": {
                "density": 1.24, "printTemp": 210, "bedTemp": 60,
                "costPerGram": 0.32, "notes": "Mayor resistencia que PLA estándar.",
            },
            "PLA Silk": {
                "density": 1.24, "printTemp": 215, "bedTemp": 60,
                "costPerGram": 0.40, "notes": "Acabado satinado/nacarado decorativo.",
            },
            "PLA Silk Bicolor": {
                "density": 1.24, "printTemp": 215, "bedTemp": 60,
                "costPerGram": 0.45, "notes": "Gradiente de 2 colores en un carrete.",
            },
            "PLA Matte": {
                "density": 1.24, "printTemp": 210, "bedTemp": 60,
                "costPerGram": 0.35, "notes": "Acabado mate, oculta capas visualmente.",
            },
            "PLA Rapid / HS": {
                "density": 1.24, "printTemp": 220, "bedTemp": 60,
                "costPerGram": 0.38, "notes": "Optimizado para alta velocidad (>300mm/s).",
            },
            "PLA Glitter": {
                "density": 1.25, "printTemp": 205, "bedTemp": 60,
                "costPerGram": 0.42, "notes": "Partículas metálicas. Efecto brillante.",
            },
            "PLA Metal / Filled": {
                "density": 1.40, "printTemp": 210, "bedTemp": 60,
                "costPerGram": 0.55, "notes": "Relleno metálico. Apariencia de metal.",
            },
            "PLA Wood": {
                "density": 1.15, "printTemp": 205, "bedTemp": 60,
                "costPerGram": 0.48, "notes": "Relleno de madera. Aspecto natural.",
            },
            "PLA Marble": {
                "density": 1.30, "printTemp": 210, "bedTemp": 60,
                "costPerGram": 0.45, "notes": "Efecto mármol. Decorativo.",
            },
        }
    },
    "PETG": {
        "color": "#2196F3",
        "subtypes": {
            "Estándar": {
                "density": 1.27, "printTemp": 230, "bedTemp": 70,
                "costPerGram": 0.25, "notes": "Mayor resistencia que PLA, semitransparente.",
            },
            "PETG+": {
                "density": 1.27, "printTemp": 235, "bedTemp": 75,
                "costPerGram": 0.30, "notes": "Formulación mejorada para mayor resistencia.",
            },
            "PETG CF (Fibra Carbono)": {
                "density": 1.30, "printTemp": 250, "bedTemp": 80,
                "costPerGram": 0.65, "notes": "Fibra de carbono. Mayor rigidez y resistencia.",
            },
            "PETG Transparente": {
                "density": 1.27, "printTemp": 225, "bedTemp": 70,
                "costPerGram": 0.30, "notes": "Alta claridad óptica.",
            },
        }
    },
    "ABS": {
        "color": "#FF9800",
        "subtypes": {
            "Estándar": {
                "density": 1.04, "printTemp": 240, "bedTemp": 100,
                "costPerGram": 0.22, "notes": "Alta temperatura. Requiere cámara cerrada.",
            },
            "ABS+": {
                "density": 1.04, "printTemp": 245, "bedTemp": 100,
                "costPerGram": 0.28, "notes": "Menor warping. Formulación mejorada.",
            },
            "ABS CF": {
                "density": 1.10, "printTemp": 255, "bedTemp": 110,
                "costPerGram": 0.60, "notes": "Con fibra de carbono. Piezas técnicas.",
            },
        }
    },
    "ASA": {
        "color": "#F44336",
        "subtypes": {
            "Estándar": {
                "density": 1.07, "printTemp": 245, "bedTemp": 100,
                "costPerGram": 0.38, "notes": "Resistente UV. Ideal para exteriores.",
            },
            "ASA CF": {
                "density": 1.15, "printTemp": 255, "bedTemp": 110,
                "costPerGram": 0.70, "notes": "Fibra carbono + resistencia UV.",
            },
        }
    },
    "TPU": {
        "color": "#9C27B0",
        "subtypes": {
            "95A (Standard)": {
                "density": 1.21, "printTemp": 220, "bedTemp": 40,
                "costPerGram": 0.65, "notes": "Flexible estándar. Durómetro 95A.",
            },
            "87A (Soft)": {
                "density": 1.20, "printTemp": 215, "bedTemp": 40,
                "costPerGram": 0.75, "notes": "Más suave. Durómetro 87A.",
            },
            "TPU Rapid": {
                "density": 1.21, "printTemp": 220, "bedTemp": 40,
                "costPerGram": 0.80, "notes": "Optimizado para alta velocidad.",
            },
        }
    },
    "PA (Nylon)": {
        "color": "#607D8B",
        "subtypes": {
            "PA6": {
                "density": 1.14, "printTemp": 260, "bedTemp": 80,
                "costPerGram": 0.75, "notes": "Nylon 6. Alta resistencia mecánica.",
            },
            "PA12": {
                "density": 1.01, "printTemp": 255, "bedTemp": 70,
                "costPerGram": 0.90, "notes": "Nylon 12. Menor absorción de humedad.",
            },
            "PA CF (Fibra Carbono)": {
                "density": 1.20, "printTemp": 280, "bedTemp": 90,
                "costPerGram": 1.20, "notes": "Nylon + carbono. Piezas industriales.",
            },
            "PA GF (Fibra Vidrio)": {
                "density": 1.35, "printTemp": 275, "bedTemp": 90,
                "costPerGram": 1.00, "notes": "Nylon + fibra de vidrio. Alta rigidez.",
            },
        }
    },
    "PC (Policarbonato)": {
        "color": "#00BCD4",
        "subtypes": {
            "Estándar": {
                "density": 1.20, "printTemp": 280, "bedTemp": 110,
                "costPerGram": 0.70, "notes": "Transparente, alta temperatura.",
            },
            "PC CF": {
                "density": 1.25, "printTemp": 290, "bedTemp": 120,
                "costPerGram": 1.10, "notes": "PC + fibra de carbono. Máxima rigidez.",
            },
        }
    },
    "HIPS": {
        "color": "#8BC34A",
        "subtypes": {
            "Estándar": {
                "density": 1.03, "printTemp": 230, "bedTemp": 100,
                "costPerGram": 0.25, "notes": "Soporte soluble para ABS.",
            }
        }
    },
    "PVA": {
        "color": "#E91E63",
        "subtypes": {
            "Estándar": {
                "density": 1.19, "printTemp": 185, "bedTemp": 45,
                "costPerGram": 1.50, "notes": "Soporte soluble en agua. Multicolor/dual.",
            }
        }
    },
    "Resina (MSLA/SLA)": {
        "color": "#795548",
        "subtypes": {
            "Estándar": {
                "density": 1.10, "printTemp": 0, "bedTemp": 0,
                "costPerGram": 0.50, "notes": "Resina estándar UV. Alta resolución.",
            },
            "ABS-Like": {
                "density": 1.12, "printTemp": 0, "bedTemp": 0,
                "costPerGram": 0.60, "notes": "Resistencia similar a ABS.",
            },
            "Flexible": {
                "density": 1.10, "printTemp": 0, "bedTemp": 0,
                "costPerGram": 0.80, "notes": "Resina flexible/elastomérica.",
            },
        }
    },
}

# Color presets para filamentos
FILAMENT_COLORS = {
    "Blanco":        "#F5F5F5",
    "Negro":         "#1A1A1A",
    "Gris":          "#9E9E9E",
    "Rojo":          "#E53935",
    "Azul":          "#1E88E5",
    "Verde":         "#43A047",
    "Amarillo":      "#FDD835",
    "Naranja":       "#FB8C00",
    "Morado":        "#8E24AA",
    "Rosa":          "#E91E63",
    "Café/Marrón":   "#6D4C41",
    "Transparente":  "#E0F7FA",
    "Dorado":        "#FFD700",
    "Plateado":      "#C0C0C0",
    "Cobre":         "#B87333",
    "Azul Marino":   "#0D47A1",
    "Verde Militar": "#4E6B1F",
    "Personalizado": "#888888",
}

# ─── ESTADOS DE ÓRDENES ───────────────────────────────────────────
ORDER_STATUSES = {
    "pending":     {"label": "Pendiente",   "color": "#fbbf24"},
    "in-progress": {"label": "En proceso",  "color": "#60a5fa"},
    "completed":   {"label": "Completada",  "color": "#4ade80"},
    "cancelled":   {"label": "Cancelada",   "color": "#f87171"},
    "delivered":   {"label": "Entregada",   "color": "#a78bfa"},
}

# ─── CONFIGURACIÓN INICIAL ────────────────────────────────────────
DEFAULT_CONFIG = {
    "negocio": "Mi Taller 3D",
    "contacto": "",
    "merma": 0.05,
    "margen": 0.15,
    "electricidad_kwh": 0.9,
    "moneda": "MXN",
    "tema": "dark",
}
