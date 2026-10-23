import os, sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Menu lateral fiel ao Caixa Bolo:
    - Baseado no código oficial de C:\\Users\\escri\\OneDrive\\Desktop\\Caixa Bolo
    - Largura recolhida: 64px (ícones centralizados)
    - Largura expandida: 260px (overlay suave sobre o conteúdo)
    - Hardware clipping nativo via Canvas para transição a 80 FPS sem nenhum rastro
    - Efeito Hover com fundo suave e item ativo em pílula azul da marca
    """
    COLLAPSED_WIDTH = 64
    EXPANDED_WIDTH  = 260
    ANIM_STEPS      = 12
    FRAME_MS        = 12  # ~80 FPS (duração de 144ms com desaceleração cúbica)

    NAV_ITEMS = [
        {"id": "home",      "label": "Início"},
        {"id": "caixa",     "label": "Caixa / PDV"},
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
            fg_color="transparent",
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

        # 1. Canvas Clipper de alta performance (recorta o conteúdo perfeitamente)
        self.canvas = tk.Canvas(
            self,
            width=self.COLLAPSED_WIDTH,
            bg="#FFFFFF",
            highlightthickness=0,
            bd=0
        )
        self.canvas.place(x=0, y=0, relheight=1.0)

        # Borda direita sutil (#E2E8F0)
        self._border_line = self.canvas.create_line(
            self.COLLAPSED_WIDTH - 1, 0, self.COLLAPSED_WIDTH - 1, 3000,
            fill=COLORS.get("sidebar_border", "#E2E8F0"), width=1
        )

        # 2. Painel interno de largura fixa (260px) NUNCA redimensionado durante a animação
        self.inner = ctk.CTkFrame(
            self.canvas,
            width=self.EXPANDED_WIDTH,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        self.canvas.create_window(0, 0, window=self.inner, anchor="nw")

        self._row_frames = {}
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
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(22, 22)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(22, 22)),
                "hover":   ctk.CTkImage(light_image=im_hov, dark_image=im_hov, size=(22, 22)),
            }

    def _build_ui(self):
        # Header (56px) idêntico ao Caixa Bolo
        header = ctk.CTkFrame(self.inner, width=self.EXPANDED_WIDTH, height=56, fg_color="#FFFFFF", corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo Icon exatamente a 21px da borda (centralizado na coluna de 64px: 64/2 - 22/2 = 21)
        logo_icon = ctk.CTkLabel(
            header, text="", image=self._icons["logo"]["hover"],
            width=22, height=22
        )
        logo_icon.place(x=21, y=17)

        logo_title = ctk.CTkLabel(
            header, text="Pães Carioca",
            font=get_font("sidebar_title"),
            text_color=COLORS.get("primary", "#1D4ED8")
        )
        logo_title.place(x=58, y=16)

        # Divisória sutil
        sep = ctk.CTkFrame(self.inner, width=self.EXPANDED_WIDTH, height=1,
                             fg_color=COLORS.get("sidebar_border", "#E2E8F0"), corner_radius=0)
        sep.pack(fill="x", side="top")

        # Itens de Navegação (padding 10px das bordas)
        nav_container = ctk.CTkFrame(self.inner, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, padx=10, pady=16)

        for item in self.NAV_ITEMS:
            pid = item["id"]
            active = (pid == self.active_page)

            # Botão linha de 240px de largura fixa (raio de 8px)
            row = ctk.CTkFrame(
                nav_container,
                width=240, height=42,
                corner_radius=8,
                fg_color=COLORS.get("primary", "#1D4ED8") if active else "transparent",
                cursor="hand2"
            )
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            self._row_frames[pid] = row

            # Ícone a 11px da esquerda do botão (10 + 11 = 21px da borda da tela -> centralizado em 64px)
            icon = ctk.CTkLabel(
                row, text="",
                image=self._icons[pid]["active" if active else "default"],
                width=22, height=22, cursor="hand2"
            )
            icon.place(x=11, y=10)
            self._icon_lbls[pid] = icon

            # Texto a 48px da esquerda
            text_lbl = ctk.CTkLabel(
                row, text=item["label"],
                font=get_font("sidebar_item"),
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#475569"),
                anchor="w", cursor="hand2"
            )
            text_lbl.place(x=48, y=10)
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

        # Rodapé com versão
        footer = ctk.CTkFrame(self.inner, height=40, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=10, pady=(0, 12))
        footer.pack_propagate(False)

        ver_icon = ctk.CTkLabel(footer, text="⚙", font=("Arial", 16), text_color="#94A3B8")
        ver_icon.place(x=11, y=8)
        ver_lbl = ctk.CTkLabel(footer, text=f"PDV v{APP_VERSION}", font=get_font("small"), text_color="#94A3B8")
        ver_lbl.place(x=48, y=8)

    def _on_hover_enter(self, pid):
        if pid != self.active_page:
            self._row_frames[pid].configure(fg_color=COLORS.get("sidebar_hover", "#EFF6FF"))
            self._icon_lbls[pid].configure(image=self._icons[pid]["hover"])
            self._text_lbls[pid].configure(text_color=COLORS.get("primary", "#1D4ED8"))

    def _on_hover_leave(self, pid):
        if pid != self.active_page:
            self._row_frames[pid].configure(fg_color="transparent")
            self._icon_lbls[pid].configure(image=self._icons[pid]["default"])
            self._text_lbls[pid].configure(text_color=COLORS.get("sidebar_text", "#475569"))

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        for pid, row in self._row_frames.items():
            active = (pid == page_id)
            row.configure(fg_color=COLORS.get("primary", "#1D4ED8") if active else "transparent")
            self._icon_lbls[pid].configure(image=self._icons[pid]["active" if active else "default"])
            self._text_lbls[pid].configure(
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#475569"),
                font=get_font("sidebar_item")
            )

    def _setup_mouse_tracking(self):
        top = self.winfo_toplevel()
        top.bind_all("<Motion>", self._on_global_motion, add="+")
        top.bind("<Leave>", self._on_window_leave, add="+")

    def _on_global_motion(self, event):
        try:
            sx, sy = self.winfo_rootx(), self.winfo_rooty()
            sw = self._current_width
            sh = self.winfo_height()
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
        self._step_animation()

    def _step_animation(self):
        self._anim_step += 1
        t = self._anim_step / self.ANIM_STEPS
        ease = 1.0 - (1.0 - t) ** 3
        w = round(self._anim_start_w + (self._anim_target_w - self._anim_start_w) * ease)
        self._current_width = w

        # Atualiza apenas a largura do Canvas (hardware clipping nativo)
        self.canvas.configure(width=w)
        self.canvas.coords(self._border_line, w - 1, 0, w - 1, 3000)

        if self._anim_step < self.ANIM_STEPS:
            self._anim_timer = self.after(self.FRAME_MS, self._step_animation)
        else:
            self._anim_timer = None
            self._anim_running = False
            self._is_expanded = self._anim_expanding
            self._current_width = self._anim_target_w
            self.canvas.configure(width=self._anim_target_w)
            self.canvas.coords(self._border_line, self._anim_target_w - 1, 0, self._anim_target_w - 1, 3000)
