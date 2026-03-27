# ⬡ Print3D Pro — Versión Web (pywebview)

**Sin lag. Sin redibujos. Chromium embebido.**

---

## ¿Por qué esta versión?

Tkinter/CustomTkinter redibuja todos los widgets desde cero en cada `refresh()`.
Esta versión usa **pywebview** — una ventana nativa con motor Chromium adentro.
La UI es HTML/CSS/JS puro, igual de rápido que tu navegador.

El resultado:
- ✅ Scroll fluido
- ✅ Sin freezes al abrir modales
- ✅ Animaciones CSS nativas
- ✅ Dropdowns instantáneos
- ✅ Modo claro/oscuro sin rebuild

---

## Instalación

```bash
pip install pywebview
python main.py
```

> **Requiere Python 3.9+**
> En Windows puede requerir: `pip install pywebview[cef]` para mejor compatibilidad.

---

## Estructura

```
print3d_pro_web/
├── main.py          ← Punto de entrada + API Python
├── data/
│   └── constants.py ← Catálogos de marcas, modelos, filamentos
├── ui/
│   └── index.html   ← Toda la UI (HTML + CSS + JS en un solo archivo)
│
│ (generados automáticamente)
├── data/config.json
├── data/impresoras.json
├── data/materiales.json
└── data/ordenes.json
```

---

## Cómo funciona

```
[HTML/JS]  →  window.pywebview.api.get_printers()  →  [Python]  →  lee impresoras.json
[HTML/JS]  ←  [ lista de impresoras ]              ←  [Python]
```

Cada acción del usuario llama a un método Python vía `window.pywebview.api`.
Python lee/escribe los JSON y devuelve los datos. El JS actualiza el DOM.

**Sin recarga de página. Sin redibujo de ventana.**

---

## Migrar datos de la versión Tkinter

Si ya tenías datos en la versión anterior, copia los JSON:
```
impresoras.json  →  data/impresoras.json
materiales.json  →  data/materiales.json
ordenes.json     →  data/ordenes.json
config.json      →  data/config.json
```
