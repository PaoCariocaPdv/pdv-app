import os, sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Menu lateral fiel ao Caixa Bolo (PC mode):
    - Largura recolhida: 64px — apenas ícones visíveis
    - Largura expandida: 260px — overlay suave sobre o conteúdo
    - Animação: place(width=W) atualizado a cada frame (equiv. CSS transition: width)
    - Inner frame sempre 260px; o clipping é feito pelo overflow do frame pai
    - Sem canvas, sem ghosting, sem artefatos de redimensionamento
    """
    COLLAPSED_W = 64
    EXPANDED_W  = 260
    ANIM_STEPS  = 14        # passos totais
    FRAME_MS    = 10        # ~100 FPS → duração total ~140ms

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
        # O frame raiz começa com 64px e vai crescer via place_configure(width=...)
        # IMPORTANTE: width deve ser passado no construtor para o CTkFrame aceitar
        super().__init__(
            parent,
            width=self.COLLAPSED_W,
            fg_color="#FFFFFF",
            corner_radius=0,
            **kwargs
        )
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.navigate_callback = navigate_callback
        self.active_page       = "home"
        self._is_expanded      = False
        self._anim_running     = False
        self._anim_timer       = None
        self._collapse_timer   = None
        self._current_w        = self.COLLAPSED_W

        self._row_frames = {}
        self._icon_lbls  = {}
        self._text_lbls  = {}
        self._icons      = {}

        self._load_icons()
        self._build_inner()
        self.after(80, self._setup_tracking)

    # ──────────────────────────────────────────────────────────────────────────
    # Assets
    # ──────────────────────────────────────────────────────────────────────────
    def _load_icons(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "assets", "icons")
        from components.sidebar_icons import ensure_sidebar_icons
        ensure_sidebar_icons(icons_dir)

        for k in ["logo", "home", "caixa", "produtos", "vendas",
                  "clientes", "relatorio", "config"]:
            im_def = Image.open(os.path.join(icons_dir, f"{k}_default.png"))
            im_act = Image.open(os.path.join(icons_dir, f"{k}_active.png"))
            im_hov = Image.open(os.path.join(icons_dir, f"{k}_hover.png"))
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(22, 22)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(22, 22)),
                "hover":   ctk.CTkImage(light_image=im_hov, dark_image=im_hov, size=(22, 22)),
            }

    # ──────────────────────────────────────────────────────────────────────────
    # Layout interno (sempre 260px de largura)
    # ──────────────────────────────────────────────────────────────────────────
    def _build_inner(self):
        """
        Constrói o painel interno com largura fixa de 260px.
        O frame raiz (self) clipa o conteúdo naturalmente quando estiver com < 260px.
        """
        # Painel interno fixo em 260px — NÃO muda de tamanho nunca
        inner = ctk.CTkFrame(self, width=self.EXPANDED_W, fg_color="#FFFFFF", corner_radius=0)
        inner.place(x=0, y=0, relheight=1.0)  # ocupa toda a altura; width é fixo pelo widget

        # ── Header (56px) ────────────────────────────────────────────────────
        header = ctk.CTkFrame(inner, width=self.EXPANDED_W, height=56,
                              fg_color="#FFFFFF", corner_radius=0)
        header.place(x=0, y=0)

        # Logo icon: centrado na coluna de 64px → x = (64-22)/2 = 21
        logo_icon = ctk.CTkLabel(header, text="", image=self._icons["logo"]["hover"],
                                 width=22, height=22)
        logo_icon.place(x=21, y=17)

        logo_title = ctk.CTkLabel(
            header, text="Pães Carioca",
            font=get_font("sidebar_title"),
            text_color=COLORS.get("primary", "#1D4ED8")
        )
        logo_title.place(x=58, y=16)

        # ── Separador ────────────────────────────────────────────────────────
        sep = tk.Frame(inner, height=1, bg=COLORS.get("sidebar_border", "#E2E8F0"))
        sep.place(x=0, y=56, width=self.EXPANDED_W)

        # ── Borda direita (estática, sempre em x=63) ─────────────────────────
        border = tk.Frame(self, width=1, bg=COLORS.get("sidebar_border", "#E2E8F0"))
        border.place(x=self.COLLAPSED_W - 1, y=0, relheight=1.0)

        # ── Itens de Navegação ────────────────────────────────────────────────
        nav_y = 72   # 56px header + 1px sep + 16px padding
        for item in self.NAV_ITEMS:
            pid    = item["id"]
            active = (pid == self.active_page)
            bg     = COLORS.get("primary", "#1D4ED8") if active else "transparent"

            row = ctk.CTkFrame(inner, width=240, height=42,
                               corner_radius=8, fg_color=bg, cursor="hand2")
            row.place(x=10, y=nav_y)
            self._row_frames[pid] = row

            # Ícone: x=11 dentro do row → 10+11=21 da tela → centrado em 64px
            icon = ctk.CTkLabel(row, text="",
                                image=self._icons[pid]["active" if active else "default"],
                                width=22, height=22, cursor="hand2")
            icon.place(x=11, y=10)
            self._icon_lbls[pid] = icon

            txt_color = "#FFFFFF" if active else COLORS.get("sidebar_text", "#475569")
            text_lbl = ctk.CTkLabel(row, text=item["label"],
                                    font=get_font("sidebar_item"),
                                    text_color=txt_color,
                                    anchor="w", cursor="hand2")
            text_lbl.place(x=48, y=10)
            self._text_lbls[pid] = text_lbl

            # Bindings
            for widget in (row, icon, text_lbl):
                widget.bind("<Button-1>", lambda e, x=pid: self._on_click(x))
                widget.bind("<Enter>",    lambda e, x=pid: self._on_hover_enter(x))
                widget.bind("<Leave>",    lambda e, x=pid: self._on_hover_leave(x))

            nav_y += 46   # 42px altura + 4px gap

        # ── Rodapé ───────────────────────────────────────────────────────────
        footer_y = nav_y + 8
        ver_icon = ctk.CTkLabel(inner, text="⚙", font=("Arial", 16), text_color="#94A3B8")
        ver_icon.place(x=21, y=footer_y)
        ver_lbl = ctk.CTkLabel(inner, text=f"PDV v{APP_VERSION}",
                               font=get_font("small"), text_color="#94A3B8")
        ver_lbl.place(x=58, y=footer_y + 1)

    # ──────────────────────────────────────────────────────────────────────────
    # Hover helpers
    # ──────────────────────────────────────────────────────────────────────────
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

    # ──────────────────────────────────────────────────────────────────────────
    # Rastreamento de mouse (equivalente ao :hover do CSS)
    # ──────────────────────────────────────────────────────────────────────────
    def _setup_tracking(self):
        top = self.winfo_toplevel()
        top.bind_all("<Motion>", self._on_global_motion, add="+")
        top.bind("<Leave>",      self._on_window_leave,  add="+")

    def _on_global_motion(self, event):
        try:
            sx = self.winfo_rootx()
            sy = self.winfo_rooty()
            sh = self.winfo_height()
            over = (sx <= event.x_root <= sx + self._current_w and
                    sy <= event.y_root <= sy + sh)
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
                self._collapse_timer = self.after(120, self._trigger_collapse)

    def _on_window_leave(self, event):
        if self._is_expanded and not self._collapse_timer:
            self._collapse_timer = self.after(80, self._trigger_collapse)

    def _trigger_collapse(self):
        self._collapse_timer = None
        if self._is_expanded and not self._anim_running:
            self._start_animation(expanding=False)

    # ──────────────────────────────────────────────────────────────────────────
    # Animação — atualiza place(width=W) a cada frame (equiv. CSS transition)
    # ──────────────────────────────────────────────────────────────────────────
    def _start_animation(self, expanding: bool):
        if self._anim_timer:
            self.after_cancel(self._anim_timer)
            self._anim_timer = None

        self._anim_running   = True
        self._anim_expanding = expanding
        self._anim_step      = 0
        self._anim_start_w   = self._current_w
        self._anim_target_w  = self.EXPANDED_W if expanding else self.COLLAPSED_W
        self._step_animation()


    def _step_animation(self):
        self._anim_step += 1
        t    = self._anim_step / self.ANIM_STEPS
        ease = 1.0 - (1.0 - t) ** 3          # ease-out cubic (idêntico ao CSS)
        w    = round(self._anim_start_w + (self._anim_target_w - self._anim_start_w) * ease)
        self._current_w = w

        # Equivale ao CSS `width: Wpx` — redimensiona o frame (clip window)
        # CTkFrame aceita width via configure() internamente
        self._current_width = w  # atributo interno do CTkFrame
        self.configure(width=w)
        self.update_idletasks()

        if self._anim_step < self.ANIM_STEPS:
            self._anim_timer = self.after(self.FRAME_MS, self._step_animation)
        else:
            self._anim_timer  = None
            self._anim_running = False
            self._is_expanded  = self._anim_expanding
            self._current_w    = self._anim_target_w
            self._current_width = self._anim_target_w
            self.configure(width=self._anim_target_w)
