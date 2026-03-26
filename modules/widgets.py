"""
╔══════════════════════════════════════════╗
║  Print3D Pro — Librería de Widgets UI    ║
╚══════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
import math


# ─── REFERENCIA GLOBAL AL TEMA ACTIVO ────────────────────────────
_T: dict = {}

def set_theme(t: dict):
    global _T
    _T = t

def T(key: str) -> str:
    return _T.get(key, "#888888")


# ─── UTILIDAD DE COLOR ────────────────────────────────────────────
# FIX CRÍTICO: Tkinter solo acepta colores #RRGGBB (6 dígitos).
# El código original usaba color+"22", color+"44", etc. (8 dígitos) → crash.
# blend_color() mezcla el color con el fondo del tema para simular alpha.

def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")[:6].ljust(6, "0")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def blend_color(color: str, alpha: float, bg_key: str = "bg_card") -> str:
    """
    Mezcla `color` con el fondo del tema para simular transparencia.
    alpha 0..1  (0=fondo puro, 1=color puro)
    Siempre retorna un color #RRGGBB válido para Tkinter.
    """
    try:
        fg = _hex_to_rgb(color)
        bg = _hex_to_rgb(T(bg_key) or "#141414")
        blended = tuple(
            max(0, min(255, int(bg[i] + (fg[i] - bg[i]) * alpha)))
            for i in range(3)
        )
        return _rgb_to_hex(*blended)
    except Exception:
        return T(bg_key) or "#141414"

# Atajos para los alphas más usados en la UI
def dim(color: str)      -> str: return blend_color(color, 0.13)  # ≈ opacidad "22"
def dim2(color: str)     -> str: return blend_color(color, 0.27)  # ≈ opacidad "44"
def border_a(color: str) -> str: return blend_color(color, 0.25)  # ≈ opacidad "40"
def dim_toast(color: str)-> str: return blend_color(color, 0.37)  # ≈ opacidad "60"


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
    """Badge de color. FIX: usa blend_color() en lugar de color+'22' inválido."""
    return ctk.CTkLabel(
        parent, text=f" {text} ",
        font=font(10, "bold"),
        text_color=color,
        fg_color=dim(color),
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
        text=label_text, command=command, width=width,
        fg_color=T("accent"), hover_color=T("accent_hover"),
        text_color="#ffffff", font=font(13, "bold"), corner_radius=8,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnGhost(parent, text, command, width=100, color=None, **kwargs) -> ctk.CTkButton:
    c = color or T("ghost_text")
    kw = dict(
        text=text, command=command, width=width,
        fg_color="transparent", border_width=1,
        border_color=T("ghost_border"), text_color=c,
        hover_color=T("ghost_hover"), font=font(12), corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnDanger(parent, text, command, width=90, **kwargs) -> ctk.CTkButton:
    """FIX: reemplaza T('red')+'22'/'44'/'40' con blend_color válido."""
    red = T("red")
    kw = dict(
        text=text, command=command, width=width,
        fg_color=dim(red), hover_color=dim2(red),
        text_color=red, border_width=1,
        border_color=border_a(red), font=font(12), corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


def BtnSuccess(parent, text, command, width=120, **kwargs) -> ctk.CTkButton:
    """FIX: reemplaza T('green')+'22'/'44'/'40' con blend_color válido."""
    green = T("green")
    kw = dict(
        text=text, command=command, width=width,
        fg_color=dim(green), hover_color=dim2(green),
        text_color=green, border_width=1,
        border_color=border_a(green), font=font(12), corner_radius=7,
    )
    kw.update(kwargs)
    return ctk.CTkButton(parent, **kw)


# ─── GAUGE CIRCULAR ───────────────────────────────────────────────

class CircularGauge(tk.Canvas):
    """Gauge circular para mostrar % de filamento."""
    def __init__(self, parent, size=120, **kwargs):
        bg = T("bg_card") or "#141414"
        super().__init__(parent, width=size, height=size,
                         bg=bg, highlightthickness=0, **kwargs)
        self.size = size
        self._bg  = bg

    def draw(self, pct: float, label: str, remaining: float, total: float, hex_color: str):
        # Sincronizar fondo con tema activo
        current_bg = T("bg_card") or "#141414"
        if self._bg != current_bg:
            self._bg = current_bg
            self.configure(bg=current_bg)

        self.delete("all")
        s  = self.size
        cx = cy = s / 2
        r  = s / 2 - 14
        thick = 10

        self.create_oval(cx-r, cy-r, cx+r, cy+r,
                         outline=T("border2") or "#2a2a2a", width=thick+2)
        self.create_oval(cx-r, cy-r, cx+r, cy+r,
                         outline=T("bg_card2") or "#0f0f0f", width=thick)

        if pct > 0.005:
            steps = max(6, int(pct * 150))
            start = math.radians(90)
            total_angle = pct * 2 * math.pi
            for i in range(steps):
                a1 = start - (i / steps) * total_angle
                a2 = start - ((i+1) / steps) * total_angle
                for dr in range(-(thick // 2), (thick // 2) + 1):
                    rr = r + dr
                    self.create_line(
                        cx + rr * math.cos(a1), cy - rr * math.sin(a1),
                        cx + rr * math.cos(a2), cy - rr * math.sin(a2),
                        fill=hex_color, width=2, capstyle=tk.ROUND)

        # FIX: glow usa blend_color en lugar de hex_color+"20"
        if pct > 0.1:
            glow_r = r - thick // 2 - 2
            self.create_oval(cx-glow_r, cy-glow_r, cx+glow_r, cy+glow_r,
                             outline=blend_color(hex_color, 0.12, "bg_card"), width=4)

        fsize_pct = max(11, int(s * 0.14))
        fsize_lbl = max(9,  int(s * 0.085))
        fsize_sub = max(8,  int(s * 0.075))

        self.create_text(cx, cy - 10, text=f"{pct*100:.0f}%",
                         fill=hex_color, font=("DM Sans", fsize_pct, "bold"))
        self.create_text(cx, cy + 8,  text=label[:12],
                         fill=T("text") or "#e0e0e0",
                         font=("DM Sans", fsize_lbl, "bold"))
        self.create_text(cx, cy + 22, text=f"{remaining:.0f}/{total:.0f}g",
                         fill=T("text_sub") or "#666666",
                         font=("DM Sans", fsize_sub))

    def update_theme(self, new_bg: str):
        self._bg = new_bg
        self.configure(bg=new_bg)

    @staticmethod
    def color_for_pct(pct: float) -> str:
        if pct < 0.20: return T("red")    or "#f87171"
        if pct < 0.40: return T("yellow") or "#fbbf24"
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
        self._pct   = pct
        self._color = color
        self.delete("all")
        w = self.winfo_width() or 200
        h = self._h
        self.create_rectangle(0, 0, w, h, fill=T("bg_hover") or "#1a1a1a", outline="")
        fill_w = max(0, min(int(w * pct), w))
        if fill_w > 0:
            self.create_rectangle(0, 0, fill_w, h, fill=color, outline="")
        # FIX: glow usa blend_color en lugar de color+"99"
        if fill_w > 4:
            self.create_rectangle(0, 0, fill_w, 2,
                                  fill=blend_color(color, 0.6, "bg_card"), outline="")


# ─── TOAST NOTIFICATION ───────────────────────────────────────────

class Toast:
    """Notificación temporal flotante en la esquina inferior derecha."""
    def __init__(self, root, msg: str, ok: bool = True):
        self.root  = root
        color  = T("green") if ok else T("red")
        bg     = T("bg_card")
        border = blend_color(color, 0.37, "bg_card")  # FIX: era color+"60"

        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=bg)

        frame = tk.Frame(self.win, bg=bg,
                         highlightbackground=border, highlightthickness=1)
        frame.pack(ipadx=18, ipady=11)
        icon = "✓" if ok else "✗"
        tk.Label(frame, text=f"{icon}  {msg}", bg=bg, fg=color,
                 font=("DM Sans", 12), padx=0).pack()

        root.update_idletasks()
        sw, sh = root.winfo_width(), root.winfo_height()
        rx, ry = root.winfo_x(), root.winfo_y()
        self.win.update_idletasks()
        tw, th = self.win.winfo_reqwidth(), self.win.winfo_reqheight()
        self.win.geometry(f"+{rx+sw-tw-24}+{ry+sh-th-24}")
        root.after(3200, self._safe_destroy)

    def _safe_destroy(self):
        try:
            self.win.destroy()
        except Exception:
            pass


# ─── DIÁLOGO DE CONFIRMACIÓN ──────────────────────────────────────

class ConfirmDialog:
    def __init__(self, parent, title: str, message: str):
        self.result = False
        dlg = ctk.CTkToplevel(parent)
        dlg.title(title)
        dlg.geometry("380x160")
        dlg.configure(fg_color=T("bg_card"))
        dlg.grab_set()
        dlg.resizable(False, False)
        dlg.lift()

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
    return ConfirmDialog(parent, title, message).result


# ─── KPI CARD ─────────────────────────────────────────────────────

def KpiCard(parent, title: str, value: str, icon: str, color: str) -> ctk.CTkFrame:
    card  = Card(parent)
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
    c  = tk.Canvas(parent, width=size, height=size, bg=bg, highlightthickness=0)
    c.create_oval(2, 2, size-2, size-2, fill=hex_color, outline="")
    return c
