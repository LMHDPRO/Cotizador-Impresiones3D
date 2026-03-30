<div align="center">

# ⬡ Print3D Pro — Cotizador Profesional

### Sistema de gestión y cotización para talleres de impresión 3D

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-blue?style=for-the-badge&logo=python&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-Libre-brightgreen?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-Activo-success?style=for-the-badge)
![Version](https://img.shields.io/badge/Versión-2.0-orange?style=for-the-badge)

*Arquitectura modular · Modo claro/oscuro · Dropdowns con specs precargadas*

</div>

---

## 📋 Índice

- [✨ Características](#-características)
- [🚀 Instalación](#-instalación)
- [📂 Estructura del proyecto](#-estructura-del-proyecto)
- [💡 Fórmula de cotización](#-fórmula-de-cotización)
- [🖼️ Logos de marcas](#️-logos-de-marcas-opcional)
- [📄 Licencia](#-licencia)

---

## ✨ Características

<table>
<tr>
<td width="50%">

### 🖨️ Impresoras
- Dropdowns **marca → modelo** con specs auto-cargadas
- Marcas: Bambu Lab, Creality, Elegoo, Anycubic, Prusa, Flashforge
- Costo/hora, consumo eléctrico y volumen configurables
- Soporte AMS, MMU3, IDEX, Multi-Tool y más

</td>
<td width="50%">

### 🧵 Materiales
- Dropdowns **marca → tipo → subtipo** inteligentes
- PLA (10 variantes), PETG, ABS, ASA, TPU, PA/Nylon, PC, PVA, Resina
- Medidor de filamento restante con alertas de stock bajo
- Paleta de colores + selector personalizado

</td>
</tr>
<tr>
<td width="50%">

### 💰 Cotizador
- Múltiples piezas por cotización
- Soporte **multicolor** con configuración de purga
- Desglose detallado: material, máquina, electricidad, merma y margen
- Guardado directo como orden

</td>
<td width="50%">

### 📦 Ventas & Órdenes
- Estados: `Pendiente` · `En proceso` · `Completada` · `Cancelada` · `Entregada`
- Detalle expandible por orden
- Sistema de notas con timestamp
- Filtros por estado

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Configuración
- Sliders para merma y margen de ganancia
- Monedas: MXN, USD, EUR, COP, ARS, BRL
- Vista previa de la fórmula en tiempo real

</td>
<td width="50%">

### 🌙 Modo claro / oscuro
- Toggle en la barra lateral
- Recarga completa de la UI al cambiar
- Paletas diseñadas para largas jornadas de trabajo

</td>
</tr>
</table>

---

## 🚀 Instalación

**Prerrequisito:** Python 3.10 o superior

```bash
# 1. Clona el repositorio
git clone https://github.com/LMHDPRO/Cotizador-Impresiones3D.git
cd Cotizador-Impresiones3D

# 2. Instala la dependencia
pip install customtkinter

# 3. ¡Ejecuta la app!
python main.py
```

> **Nota:** Los archivos `config.json`, `impresoras.json`, `materiales.json` y `ordenes.json` se generan automáticamente al usar la app por primera vez.

---

## 📂 Estructura del proyecto

```
Cotizador-Impresiones3D/
│
├── 📄 main.py                  ← PUNTO DE ENTRADA (ejecuta esto)
│
├── 📁 data/
│   ├── constants.py            ← Marcas, modelos, filamentos presets
│   └── store.py                ← Persistencia JSON + cálculo de costos
│
├── 📁 themes/
│   └── theme.py                ← Paletas dark/light + colores de marca
│
├── 📁 modules/
│   ├── widgets.py              ← Librería de componentes UI compartidos
│   ├── tab_dashboard.py        ← Pestaña Dashboard
│   ├── tab_cotizador.py        ← Pestaña Cotizador
│   ├── tab_impresoras.py       ← Pestaña Impresoras
│   ├── tab_materiales.py       ← Pestaña Materiales
│   ├── tab_ventas.py           ← Pestaña Ventas & Órdenes
│   └── tab_config.py           ← Pestaña Configuración
│
├── 📁 assets/
│   └── logos/                  ← Logos de marcas (PNG, opcional)
│
│   (generados automáticamente)
├── config.json
├── impresoras.json
├── materiales.json
└── ordenes.json
```

---

## 💡 Fórmula de cotización

La app calcula el precio final de cada pieza usando esta fórmula transparente:

```
Costo Material  =  Peso (g)  ×  Costo por gramo
Costo Máquina   =  Tiempo (h) × Costo/hora de la impresora
Electricidad    =  kW consumo × Precio kWh × Tiempo (h)
─────────────────────────────────────────────────────────
Subtotal        =  Material + Máquina + Extras multicolor
+ Merma         =  Subtotal × (1 + merma %)
─────────────────────────────────────────────────────────
PRECIO FINAL    =  (Subtotal + Merma) × (1 + margen %)
```

Todos los parámetros (merma, margen, precio kWh) son configurables desde la pestaña **Configuración**.

---

## 🖼️ Logos de marcas (opcional)

Para mostrar logos en la app, coloca imágenes `.png` en `assets/logos/`:

| Archivo | Marca | Resolución recomendada |
|---|---|:---:|
| `bambu.png` | Bambu Lab | 256 × 256 px |
| `creality.png` | Creality | 256 × 256 px |
| `elegoo.png` | Elegoo | 256 × 256 px |
| `anycubic.png` | Anycubic | 256 × 256 px |
| `prusa.png` | Prusa | 256 × 256 px |
| `flashforge.png` | Flashforge | 256 × 256 px |
| `sunlu.png` | Sunlu | 256 × 256 px |
| `esun.png` | eSUN | 256 × 256 px |
| `polymaker.png` | Polymaker | 256 × 256 px |
| `prusament.png` | Prusament | 256 × 256 px |
| `icon.ico` | Ícono de la app | 64 × 64 px |

> Los logos son completamente opcionales — la app funciona perfectamente sin ellos.

---

## 📄 Licencia

Uso personal y comercial libre. Sin restricciones.

---

<div align="center">

Desarrollado con ❤️ para la comunidad maker de habla hispana

⭐ Si te es útil, ¡dale una estrella al repo!

</div>
