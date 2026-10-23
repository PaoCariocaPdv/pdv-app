import os, sys
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 220
    ANIM_STEPS      = 10   # 10 frames de animação suave
    FRAME_MS        = 14   # ~70 FPS (duração total: 140ms)

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
        super().__init__(
            parent,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS.get("sidebar_bg", "#FFFFFF"),
            border_color=COLORS.get("sidebar_border", "#E2E8F0"),
            border_width=1,
            corner_radius=0,
            **kwargs
        )
        self.pack_propagate(False)
        self.navigate_callback = navigate_callback
        self.active_page = "home"
        self._is_expanded = False
        self._anim_running = False
        self._anim_timer = None
        self._collapse_timer = None
        self._current_width = self.COLLAPSED_WIDTH

        self._rows = {}
        self._icon_lbls = {}
        self._text_lbls = {}
        self._icons = {}

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
            im_hov = Image.open(os.path.join(icons_dir, f"{k}_hover.png"))
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(20, 20)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(20, 20)),
                "hover":   ctk.CTkImage(light_image=im_hov, dark_image=im_hov, size=(20, 20)),
            }

    def _build_ui(self):
        # 1. Logotipo no topo
        self._logo_icon = ctk.CTkLabel(
            self, text="", image=self._icons["logo"]["hover"],
            width=20, height=20
        )
        self._logo_icon.place(x=25, y=24)

        self._lf = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(
            self._lf, text="Pão Carioca",
            font=get_font("sidebar_title"),
            text_color=COLORS.get("primary", "#1D4ED8")
        ).pack(anchor="w")
        ctk.CTkLabel(
            self._lf, text="Sistema PDV",
            font=get_font("small"),
            text_color=COLORS.get("sidebar_text", "#64748B")
        ).pack(anchor="w", pady=(1, 0))

        # 2. Linha divisória
        self._sep = ctk.CTkFrame(
            self, width=self.COLLAPSED_WIDTH - 18, height=1,
            fg_color=COLORS.get("sidebar_border", "#E2E8F0"),
            corner_radius=0
        )
        self._sep.place(x=9, y=66)

        # 3. Itens de navegação
        for i, item in enumerate(self.NAV_ITEMS):
            y = 80 + i * 48
            pid = item["id"]
            active = (pid == self.active_page)

            # Container arredondado da linha (CTkFrame evita o bug dos anéis do CTkButton)
            row = ctk.CTkFrame(
                self, width=self.COLLAPSED_WIDTH - 18, height=42, corner_radius=10,
                fg_color=COLORS.get("sidebar_active", "#1D4ED8") if active else "transparent",
                cursor="hand2"
            )
            row.place(x=9, y=y)
            self._rows[pid] = row

            # Ícone posicionado a 16px da esquerda da linha (centralizado no modo fechado)
            icon = ctk.CTkLabel(
                row, text="",
                image=self._icons[pid]["active" if active else "default"],
                width=20, height=20, cursor="hand2"
            )
            icon.place(x=16, y=11)
            self._icon_lbls[pid] = icon

            # Texto do item (revelado apenas quando expandido)
            text_lbl = ctk.CTkLabel(
                row, text=item["label"],
                font=get_font("sidebar_item"),
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#64748B"),
                anchor="w", cursor="hand2"
            )
            self._text_lbls[pid] = text_lbl

            # Ações de clique
            row.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            icon.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
            text_lbl.bind("<Button-1>", lambda e, x=pid: self._on_click(x))

            # Efeito Hover suave
            row.bind("<Enter>", lambda e, x=pid: self._on_hover_enter(x))
            row.bind("<Leave>", lambda e, x=pid: self._on_hover_leave(x))
            icon.bind("<Enter>", lambda e, x=pid: self._on_hover_enter(x))
            icon.bind("<Leave>", lambda e, x=pid: self._on_hover_leave(x))
            text_lbl.bind("<Enter>", lambda e, x=pid: self._on_hover_enter(x))
            text_lbl.bind("<Leave>", lambda e, x=pid: self._on_hover_leave(x))

        # 4. Rodapé da versão
        self._footer = ctk.CTkLabel(
            self, text=f"PDV  v{APP_VERSION}",
            font=get_font("small"),
            text_color="#94A3B8"
        )

    def _on_hover_enter(self, pid):
        if pid != self.active_page:
            self._rows[pid].configure(fg_color=COLORS.get("sidebar_hover", "#EFF6FF"))
            self._icon_lbls[pid].configure(image=self._icons[pid]["hover"])
            self._text_lbls[pid].configure(text_color=COLORS.get("primary", "#1D4ED8"))

    def _on_hover_leave(self, pid):
        if pid != self.active_page:
            self._rows[pid].configure(fg_color="transparent")
            self._icon_lbls[pid].configure(image=self._icons[pid]["default"])
            self._text_lbls[pid].configure(text_color=COLORS.get("sidebar_text", "#64748B"))

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        for pid, row in self._rows.items():
            active = (pid == page_id)
            row.configure(fg_color=COLORS.get("sidebar_active", "#1D4ED8") if active else "transparent")
            self._icon_lbls[pid].configure(image=self._icons[pid]["active" if active else "default"])
            self._text_lbls[pid].configure(
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#64748B")
            )

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
            if not self._is_expanded and not self._anim_running:
                self._start_animation(expanding=True)
        else:
            if self._is_expanded and not self._collapse_timer:
                self._collapse_timer = self.after(140, self._trigger_collapse)

    def _on_window_leave(self, event):
        if self._is_expanded and not self._collapse_timer:
            self._collapse_timer = self.after(80, self._trigger_collapse)

    def _trigger_collapse(self):
        self._collapse_timer = None
        if self._is_expanded and not self._anim_running:
            self._start_animation(expanding=False)

    def _start_animation(self, expanding: bool):
        if self._anim_timer:
            self.after_cancel(self._anim_timer)
            self._anim_timer = None

        self._anim_running = True
        self._anim_expanding = expanding
        self._anim_step = 0
        self._anim_start_w = self._current_width
        self._anim_target_w = self.EXPANDED_WIDTH if expanding else self.COLLAPSED_WIDTH

        if not expanding:
            self._lf.place_forget()
            for text_lbl in self._text_lbls.values():
                text_lbl.place_forget()
            self._footer.place_forget()

        self._step_animation()

    def _step_animation(self):
        self._anim_step += 1
        t = self._anim_step / self.ANIM_STEPS
        ease = 1.0 - (1.0 - t) ** 3
        w = round(self._anim_start_w + (self._anim_target_w - self._anim_start_w) * ease)
        self._current_width = w
        self.configure(width=w)

        row_w = w - 18
        self._sep.configure(width=row_w)
        for row in self._rows.values():
            row.configure(width=row_w)

        if self._anim_expanding and w >= 150:
            if not self._lf.winfo_ismapped():
                self._lf.place(x=62, y=16)
                for pid, text_lbl in self._text_lbls.items():
                    text_lbl.place(x=52, y=11)
                self._footer.place(x=25, rely=1.0, y=-32)

        if self._anim_step < self.ANIM_STEPS:
            self._anim_timer = self.after(self.FRAME_MS, self._step_animation)
        else:
            self._anim_timer = None
            self._anim_running = False
            self._is_expanded = self._anim_expanding
            self._current_width = self._anim_target_w
            self.configure(width=self._anim_target_w)
            row_w = self._anim_target_w - 18
            self._sep.configure(width=row_w)
            for row in self._rows.values():
                row.configure(width=row_w)

            if self._anim_expanding:
                if not self._lf.winfo_ismapped():
                    self._lf.place(x=62, y=16)
                    for pid, text_lbl in self._text_lbls.items():
                        text_lbl.place(x=52, y=11)
                    self._footer.place(x=25, rely=1.0, y=-32)
            else:
                self._lf.place_forget()
                for text_lbl in self._text_lbls.values():
                    text_lbl.place_forget()
                self._footer.place_forget()
