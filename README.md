# ⬡ Print3D Pro — Cotizador Profesional v2.0

Sistema de gestión y cotización para talleres de impresión 3D.
Arquitectura modular, modo claro/oscuro, dropdowns inteligentes con specs precargadas.

---

## 🚀 Instalación rápida

```bash
# 1. Instalar dependencia
pip install customtkinter

# 2. Ejecutar
python main.py
```

> **Requiere Python 3.10+** (por el uso de `dict | None` en type hints)

---

## 📂 Estructura del proyecto

```
print3d_pro/
│
├── main.py                  ← PUNTO DE ENTRADA (ejecuta esto)
│
├── data/
│   ├── constants.py         ← Marcas, modelos, filamentos presets
│   └── store.py             ← Persistencia JSON + cálculo de costos
│
├── themes/
│   └── theme.py             ← Paletas dark/light + colores de marca
│
├── modules/
│   ├── widgets.py           ← Librería de componentes UI compartidos
│   ├── tab_dashboard.py     ← Pestaña Dashboard
│   ├── tab_cotizador.py     ← Pestaña Cotizador
│   ├── tab_impresoras.py    ← Pestaña Impresoras
│   ├── tab_materiales.py    ← Pestaña Materiales
│   ├── tab_ventas.py        ← Pestaña Ventas & Órdenes
│   └── tab_config.py        ← Pestaña Configuración
│
├── assets/
│   └── logos/               ← Coloca aquí los logos de marcas (PNG)
│
│   (generados automáticamente al usar la app)
├── config.json
├── impresoras.json
├── materiales.json
└── ordenes.json
```

---

## 🖼️ Logos de marcas (opcional)

Para que se vean los logos de marcas en la app, coloca imágenes `.png`
en la carpeta `assets/logos/` con estos nombres exactos:

| Archivo         | Marca         | Resolución recomendada |
|-----------------|---------------|------------------------|
| `bambu.png`     | Bambu Lab     | 256 × 256 px           |
| `creality.png`  | Creality      | 256 × 256 px           |
| `elegoo.png`    | Elegoo        | 256 × 256 px           |
| `anycubic.png`  | Anycubic      | 256 × 256 px           |
| `prusa.png`     | Prusa         | 256 × 256 px           |
| `flashforge.png`| Flashforge    | 256 × 256 px           |
| `sunlu.png`     | Sunlu         | 256 × 256 px           |
| `esun.png`      | eSUN          | 256 × 256 px           |
| `polymaker.png` | Polymaker     | 256 × 256 px           |
| `prusament.png` | Prusament     | 256 × 256 px           |
| `icon.ico`      | Ícono app     | 64 × 64 px (ICO)       |

> Los logos son opcionales. La app funciona perfectamente sin ellos.

---

## 🧠 Características principales

### 🖨️ Impresoras
- Dropdowns por **marca → modelo** con specs precargadas automáticamente
- Marcas incluidas: **Bambu Lab, Creality, Elegoo, Anycubic, Prusa, Flashforge**
- Configuración manual de costo/hora, consumo eléctrico, volumen de impresión
- Soporte para sistemas **AMS, AMS Lite, ACE Pro, MMU3, CFS, IDEX, Multi-Tool**

### 🧵 Materiales
- Dropdowns por **marca → tipo → subtipo** con specs auto-cargadas
- Tipos incluidos: PLA (10 variantes), PETG, ABS, ASA, TPU, PA/Nylon, PC, HIPS, PVA, Resina
- Medidor circular de filamento restante con alertas de stock bajo
- Paleta de colores predefinidos + selector personalizado

### 💰 Cotizador
- Múltiples piezas por cotización
- Selección de material e impresora por dropdown
- Soporte multicolor con configuración de purga por color
- Desglose de costos: material / máquina / electricidad / merma / margen
- Guardado directo como orden

### 📦 Ventas
- Gestión de estados: Pendiente / En proceso / Completada / Cancelada / Entregada
- Expandir órdenes para ver detalle de piezas
- Sistema de notas con timestamp
- Filtros por estado

### ⚙️ Configuración
- Sliders para merma y margen de ganancia
- Selector de moneda: MXN, USD, EUR, COP, ARS, BRL
- Vista previa de la fórmula de cotización en tiempo real

### 🌙/☀️ Modo claro/oscuro
- Toggle en la barra lateral
- Recarga completa de la UI al cambiar

---

## 💡 Fórmula de cotización

```
Costo Material   = Peso (g) × Costo/gramo
Costo Máquina    = Tiempo (h) × Costo/hora (por impresora)
Electricidad     = kW consumo × kWh precio × Tiempo (h)
Subtotal         = Material + Máquina + Extras multicolor
+ Merma          = Subtotal × (1 + merma%)
PRECIO FINAL     = (Subtotal + Merma) × (1 + margen%)
```

---

## 📄 Licencia

Uso personal y comercial libre.
Desarrollado con ❤️ para la comunidad de makers.
