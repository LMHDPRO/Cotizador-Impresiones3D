"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Librería de Widgets UI    ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
import math


# ─── REFERENCIA GLOBAL AL TEMA ACTIVO ────────────────────────────
# Se setea desde app.py al iniciar y al cambiar tema
_T: dict = {}

def set_theme(t: dict):
    global _T
    _T = t

def T(key: str) -> str:
    return _T.get(key, "#888888")


# ─── FUENTES ─────────────────────────────────────────────────────

def font(size=13, weight="normal"):
    return ctk.CTkFont("DM Sans", size, weight)

def font_mono(size=12):
    return ctk.CTkFont("Courier New", size)


# ─── CONTENEDORES ────────────────────────────────────────────────

def Card(parent, **kwargs) -> ctk.CTkFrame:
    kw = dict(fg_color=T("bg_card"), corner_radius=12)
    kw.update(kwargs)
    return ctk.CTkFrame(parent, **kw)


def SubCard(parent, **kwargs) -> ctk.CTkFrame:
    kw = dict(fg_color=T("bg_card2"), corner_radius=9,
              border_width=1, border_color=T("border"))
    kw.update(kwargs)
    return ctk.CTkFrame(parent, **kw)


def ScrollArea(parent, **kwargs) -> ctk.CTkScrollableFrame:
    kw = dict(
        fg_color=T("bg"),
        scrollbar_button_color=T("scrollbar"),
        scrollbar_button_hover_color=T("text_sub"),
    )
    kw.update(kwargs)
    return ctk.CTkScrollableFrame(parent, **kw)


def Divider(parent, orient="h") -> ctk.CTkFrame:
    if orient == "h":
        f = ctk.CTkFrame(parent, height=1, fg_color=T("border"))
        f.pack_propagate(False)
    else:
        f = ctk.CTkFrame(parent, width=1, fg_color=T("border"))
        f.pack_propagate(False)
    return f


# ─── ETIQUETAS ────────────────────────────────────────────────────

def Label(parent, text="", size=13, bold=False, color=None, **kwargs) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        parent, text=text,
        font=font(size, "bold" if bold else "normal"),
        text_color=color or T("text"),
        **kwargs,
    )


def SectionTitle(parent, text: str) -> ctk.CTkLabel:
    lbl = ctk.CTkLabel(
        parent, text=text,
        font=font(10, "bold"),
        text_color=T("text_sub"),
    )
    lbl.pack(anchor="w", padx=18, pady=(14, 6))
    return lbl


def PageHeader(parent, title: str, subtitle: str = "") -> ctk.CTkFrame:
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=30, pady=(26, 0))
    Label(f, title, size=26, bold=True, color=T("text_bright")).pack(anchor="w")
    if subtitle:
        Label(f, subtitle, size=13, color=T("text_sub")).pack(anchor="w", pady=(2, 0))
    return f


def Tag(parent, text: str, color: str, **kwargs) -> ctk.CTkLabel:
    """Pequeña etiqueta de color tipo badge."""
    bg = color + "22"
    return ctk.CTkLabel(
        parent, text=f" {text} ",
        font=font(10, "bold"),
        text_color=color,
        fg_color=bg,
        corner_radius=4,
        **kwargs,
    )


# ─── INPUTS ───────────────────────────────────────────────────────

def Entry(parent, **kwargs) -> ctk.CTkEntry:
    kw = dict(
        fg_color=T("bg_input"),
        border_color=T("border2"),
        text_color=T("text"),
        placeholder_text_color=T("text_dim"),
        font=font(12),
        corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkEntry(parent, **kw)


def Dropdown(parent, values, variable=None, command=None, **kwargs) -> ctk.CTkOptionMenu:
    kw = dict(
        fg_color=T("bg_input"),
        button_color=T("border2"),
        button_hover_color=T("bg_hover"),
        text_color=T("text"),
        dropdown_fg_color=T("bg_card"),
        dropdown_text_color=T("text"),
        dropdown_hover_color=T("bg_hover"),
        font=font(12),
        corner_radius=7,
        dynamic_resizing=False,
    )
    kw.update(kwargs)
    if variable and command:
        return ctk.CTkOptionMenu(parent, values=values, variable=variable, command=command, **kw)
    elif variable:
        return ctk.CTkOptionMenu(parent, values=values, variable=variable, **kw)
    elif command:
        return ctk.CTkOptionMenu(parent, values=values, command=command, **kw)
    return ctk.CTkOptionMenu(parent, values=values, **kw)


# ─── BOTONES ──────────────────────────────────────────────────────

def BtnPrimary(parent, text, command, width=120, icon=None, **kwargs) -> ctk.CTkButton:
    label_text = f"{icon}  {text}" if icon else text
    kw = dict(
        text=label_text,
        command=command,
        width=width,
        fg_color=T("accent"),
        hover_color=T("accent_hover"),
        text_color="#ffffff",
        font=font(13, "bold"),
        corner_radius=8,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnGhost(parent, text, command, width=100, color=None, **kwargs) -> ctk.CTkButton:
    c = color or T("ghost_text")
    kw = dict(
        text=text,
        command=command,
        width=width,
        fg_color="transparent",
        border_width=1,
        border_color=T("ghost_border"),
        text_color=c,
        hover_color=T("ghost_hover"),
        font=font(12),
        corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnDanger(parent, text, command, width=90, **kwargs) -> ctk.CTkButton:
    kw = dict(
        text=text,
        command=command,
        width=width,
        fg_color=T("red") + "22",
        hover_color=T("red") + "44",
        text_color=T("red"),
        border_width=1,
        border_color=T("red") + "40",
        font=font(12),
        corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnSuccess(parent, text, command, width=120, **kwargs) -> ctk.CTkButton:
    kw = dict(
        text=text,
        command=command,
        width=width,
        fg_color=T("green") + "22",
        hover_color=T("green") + "44",
        text_color=T("green"),
        border_width=1,
        border_color=T("green") + "40",
        font=font(12),
        corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


# ─── GAUGE CIRCULAR ───────────────────────────────────────────────

class CircularGauge(tk.Canvas):
    """
    Gauge circular animado para mostrar % de filamento.
    """
    def __init__(self, parent, size=120, **kwargs):
        bg = T("bg_card") or "#141414"
        super().__init__(parent, width=size, height=size,
                         bg=bg, highlightthickness=0, **kwargs)
        self.size = size
        self._bg = bg

    def draw(self, pct: float, label: str, remaining: float, total: float, hex_color: str):
        self.delete("all")
        s  = self.size
        cx = cy = s / 2
        r  = s / 2 - 14
        thick = 10

        # Fondo anillo
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         outline=T("border2") or "#2a2a2a", width=thick + 2)
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         outline=T("bg_card2") or "#0f0f0f", width=thick)

        # Arco de progreso
        if pct > 0.005:
            steps = max(6, int(pct * 150))
            start = math.radians(90)
            total_angle = pct * 2 * math.pi
            for i in range(steps):
                a1 = start - (i / steps) * total_angle
                a2 = start - ((i + 1) / steps) * total_angle
                for dr in range(-(thick // 2), (thick // 2) + 1):
                    rr = r + dr
                    x1 = cx + rr * math.cos(a1)
                    y1 = cy - rr * math.sin(a1)
                    x2 = cx + rr * math.cos(a2)
                    y2 = cy - rr * math.sin(a2)
                    self.create_line(x1, y1, x2, y2,
                                     fill=hex_color, width=2, capstyle=tk.ROUND)

        # Glow interior
        if pct > 0.1:
            glow_r = r - thick // 2 - 2
            self.create_oval(cx - glow_r, cy - glow_r,
                             cx + glow_r, cy + glow_r,
                             outline=hex_color + "20", width=4)

        # Texto central
        fsize_pct = max(11, int(s * 0.14))
        fsize_lbl = max(9,  int(s * 0.085))
        fsize_sub = max(8,  int(s * 0.075))

        self.create_text(cx, cy - 10,
                         text=f"{pct * 100:.0f}%",
                         fill=hex_color,
                         font=("DM Sans", fsize_pct, "bold"))
        self.create_text(cx, cy + 8,
                         text=label[:12],
                         fill=T("text") or "#e0e0e0",
                         font=("DM Sans", fsize_lbl, "bold"))
        self.create_text(cx, cy + 22,
                         text=f"{remaining:.0f}/{total:.0f}g",
                         fill=T("text_sub") or "#666666",
                         font=("DM Sans", fsize_sub))

    def update_theme(self, bg: str):
        self._bg = bg
        self.configure(bg=bg)

    @staticmethod
    def color_for_pct(pct: float) -> str:
        if pct < 0.20:
            return T("red") or "#f87171"
        if pct < 0.40:
            return T("yellow") or "#fbbf24"
        return T("green") or "#4ade80"


# ─── BARRA DE PROGRESO LINEAL ─────────────────────────────────────

class ProgressBar(tk.Canvas):
    def __init__(self, parent, height=8, **kwargs):
        bg = T("bg_card") or "#141414"
        super().__init__(parent, height=height, bg=bg, highlightthickness=0, **kwargs)
        self._h = height
        self.bind("<Configure>", self._on_resize)
        self._pct = 0
        self._color = T("green")

    def _on_resize(self, event):
        self.draw(self._pct, self._color)

    def draw(self, pct: float, color: str):
        self._pct = pct
        self._color = color
        self.delete("all")
        w = self.winfo_width() or 200
        h = self._h
        r = h // 2
        # Track
        self.create_rectangle(0, 0, w, h, fill=T("bg_hover") or "#1a1a1a", outline="")
        # Fill
        fill_w = max(0, min(int(w * pct), w))
        if fill_w > 0:
            self.create_rectangle(0, 0, fill_w, h, fill=color, outline="")
        # Glow
        if fill_w > 4:
            self.create_rectangle(0, 0, fill_w, 2,
                                  fill=color + "99", outline="")


# ─── TOAST NOTIFICATION ───────────────────────────────────────────

class Toast:
    """Notificación temporal flotante en la esquina inferior derecha."""
    def __init__(self, root, msg: str, ok: bool = True):
        self.root = root
        color  = T("green") if ok else T("red")
        bg     = T("bg_card")
        border = color + "60"

        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=bg)

        frame = tk.Frame(self.win, bg=bg, highlightbackground=border,
                         highlightthickness=1)
        frame.pack(ipadx=18, ipady=11)

        icon = "✓" if ok else "✗"
        tk.Label(frame, text=f"{icon}  {msg}", bg=bg, fg=color,
                 font=("DM Sans", 12), padx=0).pack()

        # Posicionar en esquina inferior derecha
        root.update_idletasks()
        sw = root.winfo_width()
        sh = root.winfo_height()
        rx = root.winfo_x()
        ry = root.winfo_y()

        self.win.update_idletasks()
        tw = self.win.winfo_reqwidth()
        th = self.win.winfo_reqheight()

        x = rx + sw - tw - 24
        y = ry + sh - th - 24
        self.win.geometry(f"+{x}+{y}")

        root.after(3200, self.win.destroy)


# ─── DIÁLOGO DE CONFIRMACIÓN ──────────────────────────────────────

class ConfirmDialog:
    """Diálogo de confirmación personalizado (evita el feo messagebox de Tk)."""
    def __init__(self, parent, title: str, message: str):
        self.result = False
        dlg = ctk.CTkToplevel(parent)
        dlg.title(title)
        dlg.geometry("380x160")
        dlg.configure(fg_color=T("bg_card"))
        dlg.grab_set()
        dlg.resizable(False, False)

        Label(dlg, message, size=13, color=T("text")).pack(pady=(28, 16), padx=24)

        btns = ctk.CTkFrame(dlg, fg_color="transparent")
        btns.pack(pady=8)

        def ok():
            self.result = True
            dlg.destroy()

        BtnDanger(btns, "Confirmar", ok, width=120).pack(side="left", padx=8)
        BtnGhost(btns, "Cancelar", dlg.destroy, width=100).pack(side="left", padx=8)

        dlg.wait_window()


def confirm(parent, title: str, message: str) -> bool:
    d = ConfirmDialog(parent, title, message)
    return d.result


# ─── KPI CARD ─────────────────────────────────────────────────────

def KpiCard(parent, title: str, value: str, icon: str, color: str) -> ctk.CTkFrame:
    """Tarjeta de métricas para el dashboard."""
    card = Card(parent)
    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="both", expand=True, padx=16, pady=14)

    top = ctk.CTkFrame(inner, fg_color="transparent")
    top.pack(fill="x")

    Label(top, title, size=11, color=T("text_sub")).pack(side="left")

    icon_frame = ctk.CTkFrame(top, fg_color=T("accent_dim"),
                               corner_radius=8, width=32, height=32)
    icon_frame.pack(side="right")
    icon_frame.pack_propagate(False)
    Label(icon_frame, icon, size=14, color=color).place(relx=0.5, rely=0.5, anchor="center")

    Label(inner, value, size=24 if len(value) < 8 else 18,
          bold=True, color=T("text_bright")).pack(anchor="w", pady=(8, 0))

    return card


# ─── COLOR DOT ────────────────────────────────────────────────────

def ColorDot(parent, hex_color: str, size: int = 14) -> tk.Canvas:
    bg = T("bg_card") or "#141414"
    c = tk.Canvas(parent, width=size, height=size, bg=bg, highlightthickness=0)
    pad = 2
    c.create_oval(pad, pad, size - pad, size - pad, fill=hex_color, outline="")
    return c
