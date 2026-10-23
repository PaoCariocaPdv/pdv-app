import os, sys
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    COLLAPSED_WIDTH  = 70
    EXPANDED_WIDTH   = 240
    ANIM_DURATION_MS = 160
    FRAME_MS         = 10

    NAV_ITEMS = [
        {"id": "home",      "label": "Início"},
        {"id": "caixa",     "label": "Caixa"},
        {"id": "produtos",  "label": "Produtos"},
        {"id": "vendas",    "label": "Vendas"},
        {"id": "clientes",  "label": "Clientes"},
        {"id": "relatorio", "label": "Relatórios"},
        {"id": "config",    "label": "Configurações"},
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
        for k in ["logo", "home", "caixa", "produtos", "vendas", "clientes", "relatorio", "config"]:
            im_def = Image.open(os.path.join(icons_dir, f"{k}_default.png"))
            im_act = Image.open(os.path.join(icons_dir, f"{k}_active.png"))
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(22, 22)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(22, 22)),
            }

    def _build_ui(self):
        # Logo icon at x=24
        self._logo_icon = ctk.CTkLabel(self, text="", image=self._icons["logo"]["active"],
                                       width=22, height=22)
        self._logo_icon.place(x=24, y=26)

        # Logo text (revealed only when width >= 130)
        self._lf = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self._lf, text="PDV Caixa", font=get_font("sidebar_title"),
                     text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(self._lf, text="Sistema de Ponto de Venda", font=get_font("small"),
                     text_color=COLORS["sidebar_text"]).pack(anchor="w", pady=(1, 0))

        # Separator (width matched to buttons)
        self._sep = ctk.CTkFrame(self, width=self.COLLAPSED_WIDTH - 16, height=1,
                                 fg_color="#1D2E47", corner_radius=0)
        self._sep.place(x=8, y=70)

        # Nav items
        for i, item in enumerate(self.NAV_ITEMS):
            y = 86 + i * 48
            pid = item["id"]

            # Background button strictly bounded to sidebar width
            bg = ctk.CTkButton(self, text="", image=None,
                               width=self.COLLAPSED_WIDTH - 16, height=42,
                               corner_radius=10, fg_color="transparent",
                               hover_color=COLORS["sidebar_active"],
                               command=lambda x=pid: self._on_click(x))
            bg.place(x=8, y=y)
            self._row_bgs[pid] = bg

            # Centered icon at x=24
            icon_lbl = ctk.CTkLabel(self, text="", image=self._icons[pid]["default"],
                                    width=22, height=22, cursor="hand2")
            icon_lbl.place(x=24, y=y + 10)
            icon_lbl.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            self._icon_lbls[pid] = icon_lbl

            # Text label at x=64 (hidden when collapsed)
            text_lbl = ctk.CTkLabel(self, text=item["label"],
                                    font=get_font("sidebar_item"),
                                    text_color=COLORS["sidebar_text"],
                                    anchor="w", cursor="hand2")
            text_lbl.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            self._text_lbls[pid] = text_lbl

            # Unified hover bindings
            bg.bind("<Enter>", lambda e, x=pid: self._on_item_enter(x))
            bg.bind("<Leave>", lambda e, x=pid: self._on_item_leave(x))
            icon_lbl.bind("<Enter>", lambda e, x=pid: self._on_item_enter(x))
            icon_lbl.bind("<Leave>", lambda e, x=pid: self._on_item_leave(x))
            text_lbl.bind("<Enter>", lambda e, x=pid: self._on_item_enter(x))
            text_lbl.bind("<Leave>", lambda e, x=pid: self._on_item_leave(x))

        # Version footer (hidden when collapsed)
        self._footer = ctk.CTkLabel(self, text=f"PDV  v{APP_VERSION}", font=get_font("small"),
                                    text_color="#627594", anchor="w")

        self._apply_active(self.active_page)

    def _on_item_enter(self, pid):
        if pid != self.active_page:
            self._row_bgs[pid].configure(fg_color=COLORS["sidebar_active"])

    def _on_item_leave(self, pid):
        if pid != self.active_page:
            self._row_bgs[pid].configure(fg_color="transparent")

    def _setup_mouse_tracking(self):
        top = self.winfo_toplevel()
        top.bind_all("<Motion>", self._on_global_motion, add="+")
        top.bind("<Leave>", self._on_window_leave, add="+")

    def _on_global_motion(self, event):
        try:
            sx, sy = self.winfo_rootx(), self.winfo_rooty()
            sw, sh = self.winfo_width(), self.winfo_height()
            over = (sx <= event.x_root <= sx + sw and sy <= event.y_root <= sy + sh)
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
        self._apply_width(w)

        if t < 1.0:
            self._anim_id = self.after(self.FRAME_MS, self._tick)
        else:
            self._apply_width(self._anim_target_w)

    def _apply_width(self, w):
        self._current_width = w
        self.configure(width=w)
        btn_w = w - 16
        self._sep.configure(width=btn_w)
        for pid, bg in self._row_bgs.items():
            bg.configure(width=btn_w)

        if w >= 130:
            if not self._lf.winfo_ismapped():
                self._lf.place(x=64, y=18)
                for i, item in enumerate(self.NAV_ITEMS):
                    y = 86 + i * 48
                    self._text_lbls[item["id"]].place(x=64, y=y + 10)
                self._footer.place(x=24, rely=1.0, y=-38)
        else:
            if self._lf.winfo_ismapped():
                self._lf.place_forget()
                for pid, text_lbl in self._text_lbls.items():
                    text_lbl.place_forget()
                self._footer.place_forget()

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
