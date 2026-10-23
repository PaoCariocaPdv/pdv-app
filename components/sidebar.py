import os, sys
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    COLLAPSED_WIDTH  = 70
    EXPANDED_WIDTH   = 240
    ANIM_DURATION_MS = 200
    FRAME_MS         = 10

    NAV_ITEMS = [
        {"id": "home",      "label": "In\u00edcio"},
        {"id": "caixa",     "label": "Caixa"},
        {"id": "produtos",  "label": "Produtos"},
        {"id": "vendas",    "label": "Vendas"},
        {"id": "clientes",  "label": "Clientes"},
        {"id": "relatorio", "label": "Relat\u00f3rios"},
        {"id": "config",    "label": "Configura\u00e7\u00f5es"},
    ]

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(parent, width=self.COLLAPSED_WIDTH,
                         fg_color=COLORS["sidebar_bg"], corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.navigate_callback = navigate_callback
        self.active_page = "home"
        self._is_expanded    = False
        self._anim_id        = None
        self._anim_start_w   = self.COLLAPSED_WIDTH
        self._anim_target_w  = self.COLLAPSED_WIDTH
        self._anim_elapsed   = 0
        self._collapse_timer = None
        self._current_width  = self.COLLAPSED_WIDTH
        self._row_bgs   = {}
        self._icon_lbls = {}
        self._text_lbls = {}
        self._icons     = {}
        self._load_icons()
        self._inner = ctk.CTkFrame(self, width=self.EXPANDED_WIDTH,
                                   fg_color=COLORS["sidebar_bg"], corner_radius=0)
        self._inner.place(x=0, y=0, relheight=1.0)
        self._inner.pack_propagate(False)
        self._build_ui()
        self.after(50, self._setup_mouse_tracking)

    def _load_icons(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "assets", "icons")
        from components.sidebar_icons import ensure_sidebar_icons
        ensure_sidebar_icons(icons_dir)
        for k in ["logo","home","caixa","produtos","vendas","clientes","relatorio","config"]:
            im_def = Image.open(os.path.join(icons_dir, f"{k}_default.png"))
            im_act = Image.open(os.path.join(icons_dir, f"{k}_active.png"))
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(22,22)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(22,22)),
            }

    def _build_ui(self):
        p = self._inner
        # Logo icon at fixed sidebar-x=24
        ctk.CTkLabel(p, text="", image=self._icons["logo"]["active"],
                     width=22, height=22).place(x=24, y=30)
        # Logo text at x=72 (beyond 70px clip when collapsed)
        _lf = ctk.CTkFrame(p, fg_color="transparent")
        _lf.place(x=72, y=20)
        ctk.CTkLabel(_lf, text="PDV Caixa", font=get_font("sidebar_title"),
                     text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(_lf, text="Sistema de Ponto de Venda", font=get_font("small"),
                     text_color=COLORS["sidebar_text"]).pack(anchor="w", pady=(1,0))
        # Separator
        ctk.CTkFrame(p, width=self.EXPANDED_WIDTH-24, height=1,
                     fg_color="#1D2E47", corner_radius=0).place(x=12, y=74)
        # Nav items
        for i, item in enumerate(self.NAV_ITEMS):
            y = 92 + i * 50
            pid = item["id"]
            # Full-width click/hover background button
            bg = ctk.CTkButton(p, text="", image=None,
                               width=self.EXPANDED_WIDTH-16, height=44,
                               corner_radius=10, fg_color="transparent",
                               hover_color=COLORS["sidebar_active"],
                               command=lambda x=pid: self._on_click(x))
            bg.place(x=8, y=y)
            self._row_bgs[pid] = bg
            # Icon label at fixed sidebar-x=24 (always visible when sidebar>=24)
            icon_lbl = ctk.CTkLabel(p, text="", image=self._icons[pid]["default"],
                                    width=22, height=22, cursor="hand2")
            icon_lbl.place(x=24, y=y+11)
            icon_lbl.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            self._icon_lbls[pid] = icon_lbl
            # Text label at sidebar-x=72 (hidden by clip when sidebar<=70px)
            text_lbl = ctk.CTkLabel(p, text=item["label"],
                                    font=get_font("sidebar_item"),
                                    text_color=COLORS["sidebar_text"],
                                    anchor="w", cursor="hand2")
            text_lbl.place(x=72, y=y+11)
            text_lbl.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            self._text_lbls[pid] = text_lbl
        # Version footer
        ctk.CTkLabel(p, text=f"PDV  v{APP_VERSION}", font=get_font("small"),
                     text_color="#627594", anchor="w").place(x=24, rely=1.0, y=-38)
        self._apply_active(self.active_page)

    def _setup_mouse_tracking(self):
        top = self.winfo_toplevel()
        top.bind_all("<Motion>", self._on_global_motion, add="+")
        top.bind("<Leave>", self._on_window_leave, add="+")

    def _on_global_motion(self, event):
        try:
            sx, sy = self.winfo_rootx(), self.winfo_rooty()
            sw, sh = self.winfo_width(), self.winfo_height()
            over = (sx <= event.x_root <= sx+sw and sy <= event.y_root <= sy+sh)
        except Exception:
            over = False
        if over:
            if self._collapse_timer:
                self.after_cancel(self._collapse_timer)
                self._collapse_timer = None
            if not self._is_expanded:
                self._is_expanded = True
                self._start_anim(self.EXPANDED_WIDTH)
        else:
            if self._is_expanded and not self._collapse_timer:
                self._collapse_timer = self.after(120, self._do_collapse)

    def _on_window_leave(self, event):
        if self._is_expanded and not self._collapse_timer:
            self._collapse_timer = self.after(80, self._do_collapse)

    def _do_collapse(self):
        self._collapse_timer = None
        self._is_expanded = False
        self._start_anim(self.COLLAPSED_WIDTH)

    def _ease_out_cubic(self, t):
        return 1.0 - (1.0 - t) ** 3

    def _start_anim(self, target):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_start_w  = self._current_width
        self._anim_target_w = target
        self._anim_elapsed  = 0
        self._anim_id = self.after(self.FRAME_MS, self._tick)

    def _tick(self):
        self._anim_id = None
        self._anim_elapsed += self.FRAME_MS
        t    = min(1.0, self._anim_elapsed / self.ANIM_DURATION_MS)
        ease = self._ease_out_cubic(t)
        w    = round(self._anim_start_w + (self._anim_target_w - self._anim_start_w) * ease)
        self._current_width = w
        self.configure(width=w)
        if t < 1.0:
            self._anim_id = self.after(self.FRAME_MS, self._tick)
        else:
            self._current_width = self._anim_target_w
            self.configure(width=self._anim_target_w)

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active(page_id)

    def _apply_active(self, page_id):
        for pid in self._row_bgs:
            active = (pid == page_id)
            self._row_bgs[pid].configure(
                fg_color=COLORS["primary"] if active else "transparent",
                hover_color=COLORS["primary"] if active else COLORS["sidebar_active"],
            )
            self._icon_lbls[pid].configure(
                image=self._icons[pid]["active" if active else "default"]
            )
            self._text_lbls[pid].configure(
                text_color="#FFFFFF" if active else COLORS["sidebar_text"]
            )
